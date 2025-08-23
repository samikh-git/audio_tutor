# Audio Tutor Server

A Python-based backend server for the Audio Tutor language learning platform. Provides AI-powered conversation tutoring, speech-to-text conversion, text-to-speech synthesis, and comprehensive conversation analysis.

## Overview

The Audio Tutor server is built with FastAPI and provides:
- **Interactive CLI tutor sessions** with real-time voice conversation
- **Speech-to-Text conversion** using Google Cloud Speech-to-Text
- **Text-to-Speech synthesis** using ElevenLabs
- **AI-powered conversations** using Google Gemini 2.0 Flash
- **Conversation storage and retrieval** with SQLite database
- **Vector database integration** with Milvus for semantic search
- **Learning analytics** with AI-powered progress reports
- **REST API endpoints** for mobile client integration

## Project Structure

```
server/
├── database/                    # Database management
│   ├── database.py             # SQLite database operations
│   ├── setup_database.py       # Database initialization
│   ├── DATABASE_README.md      # Database documentation
│   ├── conversation_history.db # SQLite database file
│   └── vector_database.db      # Milvus vector database
├── services/                   # Core services
│   ├── conversational_tutor.py # Main CLI tutor application
│   ├── stt_service.py         # Speech-to-Text service
│   ├── tts_service.py         # Text-to-Speech service
│   ├── analyzer_tutor.py      # Conversation analysis
│   ├── utils.py               # Utility functions
│   └── CLI.py                 # Command-line interface
├── server.py                  # FastAPI web server
├── requirements.txt           # Python dependencies
├── view_conversations.py      # Conversation viewing utility
└── README.md                  # This file
```

## Technology Stack

### Core Framework
- **Python 3.11+** - Main programming language
- **FastAPI** - Modern web framework for APIs
- **Uvicorn** - ASGI server for FastAPI

### AI & ML Services
- **Google Gemini 2.0 Flash** - AI conversation model
- **LangChain & LangGraph** - Conversation management
- **Google Cloud Speech-to-Text** - Real-time speech recognition
- **ElevenLabs** - Natural-sounding text-to-speech

### Database & Storage
- **SQLite** - Primary database for conversation storage
- **Milvus (milvus-lite)** - Vector database for semantic search
- **LangChain Milvus** - Vector database integration

### Development Tools
- **Python-dotenv** - Environment variable management
- **PyAudio** - Audio input/output handling
- **Pydantic** - Data validation and settings

## Prerequisites

### System Requirements
- **Python 3.11 or higher**
- **macOS/Linux** with microphone support
- **Audio input/output** capabilities

### API Keys Required
- **Google Cloud Speech-to-Text** - Service account JSON file
- **Google Generative AI** - API key for Gemini
- **ElevenLabs** - API key for text-to-speech

### macOS Specific Setup
```bash
# Install PortAudio for PyAudio
brew install portaudio

# Install Python dependencies
pip install -r requirements.txt
```

## Installation & Setup

### 1. Clone and Navigate
```bash
cd server
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the `services/` directory:

```env
# ElevenLabs API Key
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Google Generative AI API Key
GOOGLE_API_KEY=your_google_genai_api_key_here

# Google Cloud Speech-to-Text Service Account
GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/service-account.json
```

### 4. Initialize Database
```bash
python database/setup_database.py
```

This creates:
- SQLite database with conversation tables
- Vector database for semantic search
- Required indexes and constraints

## Usage

### CLI Tutor Session
Run an interactive voice conversation with the AI tutor:

```bash
python services/conversational_tutor.py
```

### Web API Server
Start the FastAPI server for mobile client integration:

```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

**Available Endpoints:**
- `GET /` - Health check
- `GET /docs` - Interactive API documentation
- `GET /redoc` - Alternative API documentation

### Conversation Management
View and manage conversation history:

```bash
# List all conversations
python view_conversations.py list

# View specific conversation details
python view_conversations.py detail <conversation_id>

# View conversations for specific user
python view_conversations.py user <user_id>
```

## API Endpoints

### Current Endpoints
- `GET /` - Root endpoint with basic info
- `GET /health` - Health check endpoint
- `GET /docs` - Swagger UI documentation

## Database Schema

### Conversations Table
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    language TEXT NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    transcript TEXT,
    analysis_report TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Vector Database
- **Collection**: `conversations`
- **Partitioning**: By user_id
- **Embeddings**: Conversation transcripts
- **Search**: Semantic similarity for analysis

## Services Architecture

### Conversational Tutor (`conversational_tutor.py`)
- **Purpose**: Main CLI application for voice conversations
- **Features**: Real-time audio processing, AI responses, session management
- **Dependencies**: STT, TTS, AI model, database

### Speech-to-Text (`stt_service.py`)
- **Purpose**: Convert speech to text using Google Cloud
- **Features**: Real-time streaming, voice activity detection
- **Configuration**: Service account credentials

### Text-to-Speech (`tts_service.py`)
- **Purpose**: Convert text to speech using ElevenLabs
- **Features**: Language-specific voices, streaming playback
- **Configuration**: API key and voice settings

### Analyzer (`analyzer_tutor.py`)
- **Purpose**: Analyze conversations and generate reports
- **Features**: Progress tracking, learning insights, recommendations
- **Dependencies**: Vector database, AI model

### Database (`database.py`)
- **Purpose**: Database operations and management
- **Features**: CRUD operations, conversation storage, statistics
- **Dependencies**: SQLite, Milvus

## Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `ELEVENLABS_API_KEY` | ElevenLabs API key for TTS | Yes |
| `GOOGLE_API_KEY` | Google Generative AI key | Yes |
| `GOOGLE_APPLICATION_CREDENTIALS` | Google Cloud service account path | Yes |

### Audio Configuration
- **Sample Rate**: 16000 Hz
- **Channels**: 1 (mono)
- **Format**: 16-bit PCM
- **Chunk Size**: 1024 bytes

### AI Model Configuration
- **Model**: Gemini 2.0 Flash
- **Temperature**: 0.7
- **Max Tokens**: 1000
- **Memory**: Per-user conversation history
