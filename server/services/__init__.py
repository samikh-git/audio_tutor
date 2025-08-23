# Services package for Audio Tutor

# Import main functions from conversational tutor
from .conversational_tutor import converse

# Import main functions from analyzer tutor
from .analyzer_tutor import add_document, create_report, remove_document

# Import main functions from STT service
from .stt_service import ws_transcribe, cli_transcribe

# Import main functions from TTS service
from .tts_service import ws_speak, cli_speak, language_codes

# Import utility functions
try:
    from .utils import *
except ImportError:
    pass

# Import CLI functions if available
try:
    from .CLI import *
except ImportError:
    pass

__all__ = [
    'converse',
    'add_document', 
    'create_report',
    'remove_document',
    'ws_transcribe',
    'cli_transcribe',
    'ws_speak',
    'cli_speak',
    'language_codes'
]
