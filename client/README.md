# Audio Tutor Mobile Client

A React Native mobile application for interactive language learning conversations. Practice speaking with an AI tutor, track your progress, and manage your learning journey across multiple languages.

## App Overview

The Audio Tutor mobile client provides a complete language learning experience with:
- **Multi-language support** (8 languages)
- **Real-time audio conversations** with AI tutor
- **User authentication and profile management**
- **Conversation history and learning analytics**
- **Modern, intuitive UI** with smooth animations

## Supported Languages

- Spanish
- French  
- German
- Italian
- Japanese
- Chinese

## Project Structure

```
client/
├── screens/                    # App screens
│   ├── LoginScreen.tsx        # User authentication
│   ├── SignupScreen.tsx       # User registration
│   ├── MainScreen.tsx         # Dashboard with conversations
│   ├── LanguageSelectorScreen.tsx  # Language selection
│   ├── ConversationScreen.tsx # Real-time conversation
│   ├── ConversationDetailScreen.tsx # Conversation history
│   ├── ProfileScreen.tsx      # User profile
│   └── EditProfileScreen.tsx  # Profile editing
├── App.tsx                    # Main app component
├── package.json              # Dependencies
├── tsconfig.json             # TypeScript configuration
└── README.md                 # This file
```

## Technology Stack

- **React Native** with Expo
- **TypeScript** for type safety
- **React Hooks** for state management
- **Animated API** for smooth transitions
- **@react-native-picker/picker** for language selection
- **SafeAreaView** for device compatibility

## Prerequisites

- **Node.js 18+**
- **npm** or **yarn**
- **Expo CLI** (`npm install -g @expo/cli`)
- **iOS Simulator** (macOS) or **Android Emulator**
- **Expo Go app** on your mobile device

## Installation & Setup

### 1. Install Dependencies

```bash
cd client
npm install
```

### 2. Start Development Server

```bash
npx expo start
```

### 3. Run on Device/Simulator

- **iOS Simulator**: Press `i` in the terminal
- **Android Emulator**: Press `a` in the terminal
- **Physical Device**: Scan QR code with Expo Go app

## Screen Descriptions

### 1. Login Screen (`LoginScreen.tsx`)
- Email and password authentication
- Navigation to signup screen
- Form validation and error handling
- Smooth animations and loading states

### 2. Signup Screen (`SignupScreen.tsx`)
- User registration with email and password
- Password confirmation
- Form validation
- Navigation back to login

### 3. Main Screen (`MainScreen.tsx`)
- Dashboard with recent conversations
- Floating action button for new conversations
- Profile button in header
- Empty state for new users

### 4. Language Selector (`LanguageSelectorScreen.tsx`)
- Interactive picker wheel for language selection
- 8 supported languages with flags
- Infinite scrolling carousel
- Start conversation button

### 5. Conversation Screen (`ConversationScreen.tsx`)
- Real-time audio recording interface
- Chat-style message display
- Audio playback controls
- Recording status indicators

### 6. Conversation Detail (`ConversationDetailScreen.tsx`)
- Full conversation transcript
- Learning analysis report
- Expandable sections
- Back navigation

### 7. Profile Screen (`ProfileScreen.tsx`)
- User information display
- Password visibility toggle
- Account actions (logout, delete)
- Navigation to edit profile

### 8. Edit Profile (`EditProfileScreen.tsx`)
- Form-based profile editing
- Password change functionality
- Form validation
- Save/cancel actions

## UI/UX Features

### Design System
- **Color Scheme**: Consistent blueish theme (`#667eea`)
- **Typography**: Clear hierarchy with proper font weights
- **Spacing**: Consistent padding and margins
- **Shadows**: Subtle elevation for depth

### Animations
- **Fade-in animations** on screen load
- **Slide transitions** between screens
- **Recording animations** with pulsing effects
- **Smooth scrolling** in conversation feed

### Responsive Design
- **SafeAreaView** for device compatibility
- **Flexible layouts** that adapt to screen sizes
- **Touch-friendly** button sizes
- **Accessible** color contrasts

## Navigation Flow

```
Login → Signup → Main → Language Selector → Conversation
  ↓        ↓       ↓           ↓                ↓
Profile ← Edit Profile ← Conversation Detail ← Back
```

## Dependencies

### Core Dependencies
```json
{
  "expo": "^50.0.0",
  "react": "18.2.0",
  "react-native": "0.73.0",
  "@react-native-picker/picker": "^2.6.0"
}
```

### Development Dependencies
```json
{
  "@types/react": "~18.2.45",
  "typescript": "^5.1.3"
}
```
