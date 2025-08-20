import re

from numpy import true_divide 

from conversational_tutor import converse

from analyzer_tutor import add_document, create_report

from tts_service import speak

from langchain_core.messages import AIMessage

from stt_service import transcribe

from datetime import datetime

from utils import db_manager

import random

def select_lang():
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
    #speak("Hi there! Please state your user ID.")
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