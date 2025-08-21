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
- **Internet connection** for API services
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

**Features:**
- Real-time microphone input
- Speech-to-text conversion
- AI-powered responses
- Text-to-speech playback
- Conversation memory
- Automatic session saving

**Session Flow:**
1. Enter user ID (or auto-generate)
2. Select language by number
3. Speak naturally with the tutor
4. Say "stop" to end session
5. View analysis report

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

### Planned Endpoints
- `POST /conversations/start` - Start new conversation
- `POST /conversations/{id}/audio` - Send audio message
- `GET /conversations/{id}` - Get conversation details
- `GET /conversations/user/{user_id}` - Get user conversations
- `POST /users/register` - User registration
- `POST /users/login` - User authentication

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

## Development

### Adding New Features
1. **Create service module** in `services/` directory
2. **Add database schema** if needed
3. **Update requirements.txt** for new dependencies
4. **Add API endpoints** in `server.py`
5. **Update documentation** and tests

### Testing
```bash
# Run basic tests
python -m pytest tests/

# Test specific service
python -c "from services.stt_service import STTService; print('STT Service OK')"
```

### Debugging
- **Enable debug logging** in service modules
- **Check API key validity** for external services
- **Verify audio device** configuration
- **Monitor database** connections and queries

## Troubleshooting

### Common Issues

#### Audio Input Problems
```bash
# Check audio devices
python -c "import pyaudio; p = pyaudio.PyAudio(); print(p.get_device_count())"

# Test microphone
python -c "import pyaudio; p = pyaudio.PyAudio(); print(p.get_default_input_device_info())"
```

#### API Key Issues
```bash
# Test Google API
python -c "import google.generativeai as genai; genai.configure(api_key='your_key'); print('Google API OK')"

# Test ElevenLabs API
python -c "from elevenlabs import generate; print('ElevenLabs API OK')"
```

#### Database Issues
```bash
# Check database connection
python -c "from database.database import get_db; db = get_db(); print('Database OK')"

# Reset database
rm database/conversation_history.db
python database/setup_database.py
```

### Performance Optimization
- **Use connection pooling** for database operations
- **Implement caching** for frequently accessed data
- **Optimize audio processing** with appropriate chunk sizes
- **Monitor memory usage** during long conversations

## Security Considerations

### API Security
- **Validate all inputs** before processing
- **Implement rate limiting** for API endpoints
- **Use HTTPS** in production
- **Secure API key storage** (not in code)

### Data Privacy
- **Encrypt sensitive data** in database
- **Implement user authentication** and authorization
- **Log access patterns** for security monitoring
- **Comply with data protection** regulations

## Deployment

### Production Setup
1. **Use production ASGI server** (Gunicorn + Uvicorn)
2. **Set up reverse proxy** (Nginx)
3. **Configure SSL certificates**
4. **Set up monitoring** and logging
5. **Implement backup** strategies

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Contributing

### Development Workflow
1. **Fork** the repository
2. **Create feature branch**
3. **Make changes** with proper testing
4. **Update documentation**
5. **Submit pull request**

### Code Standards
- **Follow PEP 8** style guidelines
- **Add type hints** for all functions
- **Write docstrings** for modules and functions
- **Include error handling** for all external calls
- **Add logging** for debugging

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information
4. Include error logs and system information

---

**Audio Tutor Server** - Powering conversational language learning with AI!
