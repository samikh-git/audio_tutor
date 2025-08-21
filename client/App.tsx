import React, { useState } from 'react';
import LoginScreen from './screens/LoginScreen';
import SignupScreen from './screens/SignupScreen';
import MainScreen from './screens/MainScreen';
import ConversationDetailScreen from './screens/ConversationDetailScreen';
import LanguageSelectorScreen from './screens/LanguageSelectorScreen';
import ConversationScreen from './screens/ConversationScreen';
import ProfileScreen from './screens/ProfileScreen';
import EditProfileScreen from './screens/EditProfileScreen';

interface Conversation {
  id: string;
  date: string;
  language: string;
  preview: string;
  duration: string;
}

type ScreenType = 'login' | 'signup' | 'main' | 'conversation-detail' | 'conversation' | 'language-selector' | 'profile' | 'edit-profile';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState<ScreenType>('login');
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
  const [selectedLanguage, setSelectedLanguage] = useState<string>('');
  
  const handleNavigateToConversation = (conversation: Conversation) => {
    setSelectedConversation(conversation);
    setCurrentScreen('conversation-detail');
  };

  const handleBackFromConversationDetail = () => {
    setCurrentScreen('main');
    setSelectedConversation(null);
  };

  const handleNavigateToNewConversation = () => {
    setCurrentScreen('language-selector');
  };

  const handleBackFromLanguageSelector = () => {
    setCurrentScreen('main');
  };

  const handleStartConversation = (language: string) => {
    setSelectedLanguage(language);
    setCurrentScreen('conversation');
  };

  const handleBackFromConversation = () => {
    setCurrentScreen('language-selector');
  };

  const handleEndConversation = () => {
    setCurrentScreen('main');
    setSelectedLanguage('');
  };

  const handleNavigateToProfile = () => {
    setCurrentScreen('profile');
  };

  const handleBackFromProfile = () => {
    setCurrentScreen('main');
  };

  const handleNavigateToEditProfile = () => {
    setCurrentScreen('edit-profile');
  };

  const handleBackFromEditProfile = () => {
    setCurrentScreen('profile');
  };

  const handleSaveProfile = (updatedProfile: any) => {
    // In a real app, this would save to backend
    console.log('Profile updated:', updatedProfile);
    setCurrentScreen('profile');
  };
  
  return (
    <>
      {currentScreen === 'login' && (
        <LoginScreen 
          onNavigateToSignup={() => setCurrentScreen('signup')} 
          onLoginSuccess={() => setCurrentScreen('main')} 
        />
      )}
      {currentScreen === 'signup' && (
        <SignupScreen 
          onNavigateToLogin={() => setCurrentScreen('login')} 
          onSignupSuccess={() => setCurrentScreen('main')} 
        />
      )}
      {currentScreen === 'main' && (
        <MainScreen 
          onLogout={() => setCurrentScreen('login')} 
          onNavigateToConversation={handleNavigateToConversation}
          onNavigateToNewConversation={handleNavigateToNewConversation}
          onNavigateToProfile={handleNavigateToProfile}
        />
      )}
      {currentScreen === 'conversation-detail' && selectedConversation && (
        <ConversationDetailScreen 
          conversation={selectedConversation}
          onBack={handleBackFromConversationDetail}
        />
      )}
      {currentScreen === 'language-selector' && (
        <LanguageSelectorScreen 
          onBack={handleBackFromLanguageSelector}
          onStartConversation={handleStartConversation}
        />
      )}
      {currentScreen === 'conversation' && (
        <ConversationScreen 
          language={selectedLanguage}
          onBack={handleBackFromConversation}
          onEndConversation={handleEndConversation}
        />
      )}
      {currentScreen === 'profile' && (
        <ProfileScreen 
          onBack={handleBackFromProfile}
          onLogout={() => setCurrentScreen('login')}
          onEditProfile={handleNavigateToEditProfile}
        />
      )}
      {currentScreen === 'edit-profile' && (
        <EditProfileScreen 
          onBack={handleBackFromEditProfile}
          onSave={handleSaveProfile}
        />
      )}
    </>
  );
}