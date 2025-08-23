# Audio Tutor

A comprehensive voice-first language tutoring platform with both CLI and mobile interfaces. Practice speaking with an AI tutor, get real-time feedback, and track your learning progress across multiple languages.

## Features

### Mobile Client (React Native)
- **Multi-language Support**: Practice Spanish, French, German, Italian, Japanese, and Chinese
- **Interactive Conversations**: Real-time audio recording and playback with AI tutor responses
- **User Profiles**: Complete user management with profile editing and password management
- **Conversation History**: View past conversations with detailed transcripts and learning reports
- **Modern UI**: Clean, intuitive interface with smooth animations and consistent theming

### Server Backend
- **Interactive CLI Tutor**: Full voice conversation with AI tutor via command line
- **Speech-to-Text**: Google Cloud Speech-to-Text integration for real-time transcription
- **Text-to-Speech**: ElevenLabs integration for natural-sounding tutor responses
- **AI Tutor**: Gemini 2.0 Flash powered conversations with conversation memory
- **Conversation Storage**: SQLite database for conversation history and user data
- **Vector Database**: Milvus integration for semantic search and analysis
- **Learning Analytics**: AI-powered analysis reports for learning progress

## Mobile App Screens

1. **Login/Signup**: User authentication with email and password
2. **Main Screen**: Dashboard with recent conversations and new conversation button
3. **Language Selector**: Interactive picker wheel for language selection
4. **Conversation Screen**: Real-time audio recording and chat interface
5. **Conversation Detail**: View transcripts and learning reports
6. **Profile Screen**: User information and account management
7. **Edit Profile**: Form-based profile editing with validation

## Project Structure

```
audio_tutor/
├── client/                     # React Native mobile app
│   ├── screens/               # App screens
│   │   ├── LoginScreen.tsx
│   │   ├── SignupScreen.tsx
│   │   ├── MainScreen.tsx
│   │   ├── LanguageSelectorScreen.tsx
│   │   ├── ConversationScreen.tsx
│   │   ├── ConversationDetailScreen.tsx
│   │   ├── ProfileScreen.tsx
│   │   └── EditProfileScreen.tsx
│   ├── App.tsx               # Main app component
│   └── package.json
├── server/                    # Python backend
│   ├── database/             # Database management
│   │   ├── database.py
│   │   ├── setup_database.py
│   │   └── vector_database.db
│   ├── services/             # Core services
│   │   ├── conversational_tutor.py
│   │   ├── stt_service.py
│   │   ├── tts_service.py
│   │   ├── analyzer_tutor.py
│   │   └── utils.py
│   ├── server.py             # FastAPI server
│   └── requirements.txt
└── README.md
```

## Technology Stack

### Mobile Client
- **React Native** with Expo
- **TypeScript** for type safety
- **React Navigation** for screen management
- **Animated API** for smooth transitions
- **@react-native-picker/picker** for language selection

### Backend Server
- **Python 3.11+**
- **FastAPI** for REST API
- **SQLite** for data persistence
- **Milvus** for vector database
- **Google Cloud Speech-to-Text**
- **ElevenLabs Text-to-Speech**
- **Google Gemini 2.0 Flash** for AI conversations
- **LangChain & LangGraph** for conversation management

## Requirements

### System Requirements
- **Python 3.11+**
- **Node.js 18+**
- **Expo CLI** for mobile development
- **macOS/Linux** with microphone (for CLI tutor)
- **iOS/Android device or simulator** for mobile app

### Python Dependencies
```bash
pip install langchain langgraph langchain-google-genai google-cloud-speech pyaudio python-dotenv elevenlabs langchain-milvus pymilvus milvus-lite fastapi uvicorn
```

### Node.js Dependencies
```bash
cd client
npm install
```

## Setup & Installation

### 1. Backend Setup

1. **Install Python dependencies**:
```bash
pip install -r server/requirements.txt
```

2. **Set up environment variables** (create `.env` file in `server/services/`):
```env
ELEVENLABS_API_KEY=your_elevenlabs_key
GOOGLE_API_KEY=your_google_genai_key
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

3. **Initialize database**:
```bash
python server/database/setup_database.py
```

### 2. Mobile Client Setup

1. **Install dependencies**:
```bash
cd client
npm install
```

2. **Start development server**:
```bash
npx expo start
```

3. **Run on device/simulator**:
   - Scan QR code with Expo Go app (iOS/Android)
   - Press 'i' for iOS simulator
   - Press 'a' for Android emulator

## Running the Application

### CLI Tutor (Backend)
```bash
python server/services/CLI.py
```
- Enter user ID and select language
- Speak naturally with the AI tutor
- Say "stop" to end session and generate analysis

### Mobile App (Frontend)
```bash
cd client
npx expo start
```
- Navigate through screens using the intuitive interface
- Select language and start conversations
- Manage profile and view conversation history

### API Server
```bash
uvicorn server.server:app --reload
```
Visit `http://127.0.0.1:8000/` for API documentation.

## Conversation Management

### View Conversation History
```bash
# List all conversations
python server/view_conversations.py list

# View specific conversation
python server/view_conversations.py detail <conversation_id>

# View user's conversations
python server/view_conversations.py user <user_id>
```