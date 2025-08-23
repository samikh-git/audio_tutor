"""Audio Tutor FastAPI application.

This module exposes a minimal FastAPI app as a placeholder. The interactive
voice tutoring experience currently runs via the CLI in
`server/services/app.py`. Future work may wire REST/WebSocket endpoints here.
"""
from fastapi import FastAPI, WebSocket, Form 

from typing import Annotated

from .services.stt_service import ws_transcribe
from .services.conversational_tutor import converse 
from .services.analyzer_tutor import add_document, create_report
from .services.tts_service import language_codes, ws_speak

from .database.database import db_manager

from langchain_core.messages import AIMessage

from datetime import datetime

import re 
import logging

app = FastAPI()

FORMAT = '%(asctime)s %(levelname)s %(message)s'

logging.basicConfig(filename='logs/server.log', format=FORMAT, level=logging.INFO)

@app.post("/sign_up/")
def create_user(user_id: Annotated[str, Form()], password: Annotated[str, Form()], first_name: str, last_name: str):
    if db_manager.user_id_already_exists(user_id):
        return {"response": "ERROR: USER ID ALREADY EXISTS"}
    else: 
        db_manager.log_new_user(user_id, password, first_name, last_name)
        return {"response": f"USER {user_id} SUCCESFULLY SIGNED UP"}

@app.websocket("/ws/{user_id}")
async def streaming_audio(websocket: WebSocket, language_code: str, user_id: str):
    """Handle real-time audio streaming for interactive language tutoring sessions.
    
    This WebSocket endpoint manages bidirectional audio communication for language
    learning. It processes incoming audio from the client, transcribes speech to text,
    generates AI tutor responses, converts responses to speech, and streams audio back
    to the client. The entire conversation is logged and analyzed for learning insights.
    
    Args:
        websocket (WebSocket): The WebSocket connection for bidirectional communication
        language_code (str): BCP-47 language code for speech recognition and synthesis
        user_id (str): Unique identifier for the user session
    
    Flow:
        1. Accept WebSocket connection and initialize conversation tracking
        2. Transcribe incoming audio stream to text using Google STT
        3. Generate AI tutor response using conversational AI with memory
        4. Stream response audio back to client in real-time chunks
        5. Save complete conversation transcript to database
        6. Generate learning analysis report and send to client
        7. Index conversation and report in vector database for future reference
    
    Side effects:
        - Saves conversation transcript to SQLite database
        - Indexes conversation and analysis report in vector database
        - Logs conversation metadata to server logs
    
    Returns:
        None. Communication occurs through the WebSocket connection.
    """
    websocket.accept()
    today = datetime.now().date()
    print("Websocket connected")
    long_transcript = f"{today} \n"
    
    # Collect audio bytes from the WebSocket
    audio_bytes = b""
    async for audio_chunk in websocket.iter_bytes():
        audio_bytes += audio_chunk
    
    query = ws_transcribe(audio_stream=audio_bytes, language_code=language_code)
    print(f"Query receieved from user {user_id}")
    
    config = {"configurable": {"thread_id": user_id}}
    long_transcript += f"USERMESSAGE: {query} \n"
    response = ""
    chunk_response = ""
    
    async for chunk, _ in converse(query = query, language = language_codes[language_code], config = config):
        if isinstance(chunk, AIMessage):
            chunk_response += chunk.content
            response += chunk.content
            if re.search(r'[.!?:;]$', response): 
                print(f"Tutor response:  {chunk_response}")
                await websocket.send_bytes(ws_speak(chunk_response, language_code))
                chunk_response = ""
    
    long_transcript += f"AIMESSAGE: {response} \n"
    conversation_id = db_manager.save_conversation(user_id, today, long_transcript)
    add_document(long_transcript, user_id)
    
    report = create_report(user_id)
    print(f"Report generated for user: {user_id}")
    await websocket.send_text(report)
    add_document(report, user_id)
    
    logging.info(f"Conversation saved with ID: {conversation_id}")
    
        