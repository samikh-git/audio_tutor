## Audio Tutor

A voice-first language tutoring project. It lets you speak with an AI tutor, streams replies back with text-to-speech, and saves full session transcripts for analysis.

### What's implemented
- **Interactive CLI tutor session** (`server/services/app.py`)
  - Microphone input with Google Cloud Speech-to-Text (streaming, voice-activity end).
  - Tutor replies via Gemini 2.0 Flash (LangChain + LangGraph) with per-user conversation memory stored in SQLite.
  - ElevenLabs streaming Text-to-Speech with language-specific voices.
  - Language selection, per-session transcript accumulation, and graceful stop by saying "stop".
  - Saves full transcript to SQLite and also to a vector store, then generates an analysis report and saves it as well.
- **Conversation storage** (`server/database/database.py`)
  - SQLite DB for conversation history with helpers to save/query/delete and fetch stats.
- **Vector database and analysis** (`server/services/analyzer_tutor.py`)
  - Milvus (milvus-lite) via `langchain-milvus` for semantic retrieval, partitioned by user id.
  - Analyzer uses Gemini 2.5 Pro with a retrieval tool to fetch a user’s past conversations and produce a feedback report.
- **Utilities**
  - View recent conversations, details, or by user via `server/view_conversations.py`.
- **API placeholder** (`server/server.py`)
  - Minimal FastAPI app with a root route. Not yet wired to the CLI tutor flow.
- **Mobile client (prototype)** (`client/`)
  - Expo React Native app that records audio and can play it back locally. Not yet integrated with the server or STT/TTS services.

### Project structure (high level)
```
audio_tutor/
  client/                # Expo app (record/playback prototype)
  server/
    database/            # SQLite + vector DB, setup script, docs
    services/            # CLI session, STT, TTS, tutor, analyzer, utils
    server.py            # FastAPI app (placeholder)
  README.md
```

### Requirements
- Python 3.11+
- Node.js 18+ and a working mobile environment if running the client (Expo)
- macOS/Linux with a microphone (for CLI tutor)
- For PyAudio on macOS: `brew install portaudio` before `pip install pyaudio`

Python packages used (install as needed):
- `langchain`, `langgraph`, `langchain-google-genai`, `google-cloud-speech`, `pyaudio`, `python-dotenv`, `elevenlabs`, `langchain-milvus`, `pymilvus`, `milvus-lite`, `fastapi`, `uvicorn`

### Environment variables
Create a `.env` file in `server/services/` or export these in your shell:
- `ELEVENLABS_API_KEY` — ElevenLabs API key (for TTS)
- `GOOGLE_API_KEY` — Google Generative AI key (for Gemini via LangChain)
- `GOOGLE_APPLICATION_CREDENTIALS` — absolute path to a Google Cloud service account JSON (for Speech-to-Text)

Example `.env` snippet:
```
ELEVENLABS_API_KEY=...
GOOGLE_API_KEY=...
GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/service-account.json
```

### Setup
1) Install Python deps (example):
```
pip install langchain langgraph langchain-google-genai google-cloud-speech pyaudio python-dotenv elevenlabs langchain-milvus pymilvus milvus-lite fastapi uvicorn
```

2) Initialize the SQLite database (creates tables and indexes):
```
python server/database/setup_database.py
```

### Run the interactive tutor (CLI)
Runs microphone capture → STT → Gemini tutor → TTS playback, with persistence.
```
python server/services/app.py
```
- Enter a user id (or it will auto-generate one), then select a language by number.
- Speak to the tutor; say `stop` to end the session.
- After ending, the transcript is saved to SQLite, added to the vector DB, an analysis report is generated, and stored as well.

### View conversation history
```
# List recent conversations and DB stats
python server/view_conversations.py list

# View details for a conversation id
python server/view_conversations.py detail 1

# View conversations for a user id
python server/view_conversations.py user <user_id>
```

### Run the API (placeholder)
```
uvicorn server.server:app --reload
```
Visit `http://127.0.0.1:8000/` to see the placeholder response.

### Mobile client (prototype)
```
cd client
npm install
npx expo start
```
- The app can record audio and play it back locally.
- Server integration and end‑to‑end streaming on device are not implemented yet.

### Current limitations / next steps
- The FastAPI app is a placeholder; no REST/WebSocket endpoints for live sessions yet.
- The Expo client is not connected to the server/STT/TTS.
- The interactive flow runs from the CLI on desktop using your microphone.

### Notes
- Vector DB uses milvus‑lite with a local file at `server/database/vector_database.db`.
- Conversation memory for the tutor is handled by LangGraph checkpoints in SQLite.