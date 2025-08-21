"""CLI entrypoint for the interactive voice tutoring session.

Runs a microphone-driven loop that:
- prompts for `user_id` and language selection
- captures speech and transcribes it via Google STT
- streams tutor responses via Gemini with memory
- plays synthesized audio via ElevenLabs TTS
- saves transcripts to SQLite and vector DB, and generates a report
"""

import re

from conversational_tutor import converse

from analyzer_tutor import add_document, create_report

from tts_service import speak

from langchain_core.messages import AIMessage

from stt_service import transcribe

from datetime import datetime

from utils import db_manager

import random

def select_lang():
    """Prompt the user to select a target language for the session.

    Returns:
        tuple[str, str]: A pair of (language_name, bcp47_code).
    """
    languages = {
        1: ("English", "en-UK"), 
        2: ("French", "fr-FR"), 
        3: ("Spanish", "es-ES"), 
        4: ("Mandarin", "cmn-HANS-CN"), 
        5: ("Japanese", "ja-JP"), 
        6: ("German", "de-DE"), 
        7: ("Italian", "it-IT")
    }
    lang_id = int(input(""" Please select the right number for the language you wish to practice. 
    [1] English
    [2] French
    [3] Spanish
    [4] Mandarin
    [5] Japanese
    [6] German
    [7] Italian
    """))
    return languages[lang_id]


def session():
    """Run an interactive voice tutoring session in the terminal.

    Flow:
    1) Ask for `user_id` and language selection
    2) Loop: transcribe user speech, stream tutor reply, and TTS playback
    3) On "stop", persist transcript, generate an analysis report, and exit

    Side effects:
        - Saves conversation into SQLite
        - Indexes transcript and report into the vector database
    """
    print("====================== WELCOME TO AUDIO TUTOR CLI! ======================= ")
    print("\n \n")
    speak("Hi there! Please state your user ID.")
    user_id  = str(input("Hi there! Please state your user ID. \n")).strip() or random.randint(300,2000)
    config = {"configurable": {"thread_id": user_id}}
    language_tpl = select_lang()
    today = datetime.now().date()
    long_transcript = f"{today} \n"
    while True:
            transcript = transcribe(language_tpl[1])
            long_transcript += f"USERMESSAGE: {transcript} \n"
            response = ""
            chunk_response = ""
            if transcript.strip().lower() == "stop":
                break
            for chunk, _ in converse(query = transcript, language = language_tpl[0], config = config):
                if isinstance(chunk, AIMessage):
                    chunk_response += chunk.content
                    response += chunk.content
                    if re.search(r'[.!?:;]$', response): 
                        print(f"Tutor response:  {chunk_response}")
                        speak(chunk_response, language_tpl[0])
                        chunk_response = ""
            long_transcript += f"AIMESSAGE: {response} \n"
    print(long_transcript)
    conversation_id = db_manager.save_conversation(user_id, today, long_transcript)
    add_document(long_transcript, user_id)
    report = create_report(user_id)
    print(report)
    add_document(report, user_id)
    print(f"Conversation saved with ID: {conversation_id}")

if __name__ == "__main__":
    session()