import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  StyleSheet,
  Text,
  TouchableOpacity,
  SafeAreaView,
  Animated,
  ScrollView,
  Dimensions,
  Alert,
} from 'react-native';

const { width, height } = Dimensions.get('window');

interface ConversationScreenProps {
  language: string;
  onBack: () => void;
  onEndConversation: () => void;
}

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'tutor';
  timestamp: Date;
  audioUrl?: string;
}

export default function ConversationScreen({ language, onBack, onEndConversation }: ConversationScreenProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentAudioUrl, setCurrentAudioUrl] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [fadeAnim] = useState(new Animated.Value(0));
  const [slideAnim] = useState(new Animated.Value(50));
  const [recordingAnim] = useState(new Animated.Value(1));
  const scrollViewRef = useRef<ScrollView>(null);
  const recordingInterval = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 800,
        useNativeDriver: true,
      }),
      Animated.timing(slideAnim, {
        toValue: 0,
        duration: 600,
        useNativeDriver: true,
      }),
    ]).start();

    // Add initial tutor message
    addMessage({
      id: '1',
      text: `¡Hola! I'm your ${language} tutor. Let's start practicing!`,
      sender: 'tutor',
      timestamp: new Date(),
    });
  }, []);

  useEffect(() => {
    // Scroll to bottom when new messages arrive
    if (scrollViewRef.current) {
      setTimeout(() => {
        scrollViewRef.current?.scrollToEnd({ animated: true });
      }, 100);
    }
  }, [messages]);

  const addMessage = (message: Message) => {
    setMessages(prev => [...prev, message]);
  };

  const startRecording = async () => {
    try {
      setIsRecording(true);
      
      // Start recording animation
      Animated.loop(
        Animated.sequence([
          Animated.timing(recordingAnim, {
            toValue: 0.3,
            duration: 1000,
            useNativeDriver: true,
          }),
          Animated.timing(recordingAnim, {
            toValue: 1,
            duration: 1000,
            useNativeDriver: true,
          }),
        ])
      ).start();

      // Simulate recording - in real app, this would start actual audio recording
      console.log('Started recording audio...');
      
    } catch (error) {
      Alert.alert('Error', 'Failed to start recording');
      setIsRecording(false);
    }
  };

  const stopRecording = async () => {
    try {
      setIsRecording(false);
      recordingAnim.stopAnimation();
      recordingAnim.setValue(1);

      // Simulate sending audio to backend
      const userMessage: Message = {
        id: Date.now().toString(),
        text: 'User audio message...',
        sender: 'user',
        timestamp: new Date(),
        audioUrl: 'user_audio_url',
      };
      
      addMessage(userMessage);

      // Simulate backend response
      setTimeout(() => {
        const tutorMessage: Message = {
          id: (Date.now() + 1).toString(),
          text: 'Great pronunciation! Let me respond...',
          sender: 'tutor',
          timestamp: new Date(),
          audioUrl: 'tutor_audio_url',
        };
        addMessage(tutorMessage);
      }, 2000);

    } catch (error) {
      Alert.alert('Error', 'Failed to stop recording');
    }
  };

  const playAudio = async (audioUrl: string) => {
    try {
      setIsPlaying(true);
      setCurrentAudioUrl(audioUrl);
      
      // Simulate audio playback
      console.log('Playing audio:', audioUrl);
      
      // Simulate playback duration
      setTimeout(() => {
        setIsPlaying(false);
        setCurrentAudioUrl(null);
      }, 3000);
      
    } catch (error) {
      Alert.alert('Error', 'Failed to play audio');
      setIsPlaying(false);
      setCurrentAudioUrl(null);
    }
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const renderMessage = (message: Message) => (
    <View key={message.id} style={[
      styles.messageContainer,
      message.sender === 'user' ? styles.userMessage : styles.tutorMessage
    ]}>
      <View style={[
        styles.messageBubble,
        message.sender === 'user' ? styles.userBubble : styles.tutorBubble
      ]}>
        <Text style={[
          styles.messageText,
          message.sender === 'user' ? styles.userText : styles.tutorText
        ]}>
          {message.text}
        </Text>
        
        {message.audioUrl && (
          <TouchableOpacity
            style={[
              styles.audioButton,
              isPlaying && currentAudioUrl === message.audioUrl && styles.audioButtonPlaying
            ]}
            onPress={() => playAudio(message.audioUrl!)}
            disabled={isPlaying}
          >
            <Text style={styles.audioButtonText}>
              {isPlaying && currentAudioUrl === message.audioUrl ? '⏸️' : '▶️'}
            </Text>
          </TouchableOpacity>
        )}
        
        <Text style={[
          styles.timestamp,
          message.sender === 'user' ? styles.userTimestamp : styles.tutorTimestamp
        ]}>
          {formatTime(message.timestamp)}
        </Text>
      </View>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <Animated.View 
        style={[
          styles.content,
          {
            opacity: fadeAnim,
            transform: [{ translateY: slideAnim }],
          },
        ]}
      >
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity style={styles.backButton} onPress={onBack}>
            <Text style={styles.backButtonText}>←</Text>
          </TouchableOpacity>
          <View style={styles.headerInfo}>
            <Text style={styles.headerTitle}>{language} Conversation</Text>
            <Text style={styles.headerSubtitle}>Practice your speaking skills</Text>
          </View>
          <TouchableOpacity style={styles.endButton} onPress={onEndConversation}>
            <Text style={styles.endButtonText}>End</Text>
          </TouchableOpacity>
        </View>

        {/* Messages Feed */}
        <ScrollView
          ref={scrollViewRef}
          style={styles.messagesContainer}
          showsVerticalScrollIndicator={false}
          contentContainerStyle={styles.messagesContent}
        >
          {messages.map(renderMessage)}
        </ScrollView>

        {/* Recording Controls */}
        <View style={styles.controlsContainer}>
          <View style={styles.recordingIndicator}>
            {isRecording && (
              <Animated.View style={[
                styles.recordingDot,
                { opacity: recordingAnim }
              ]} />
            )}
            <Text style={styles.recordingText}>
              {isRecording ? 'Recording...' : 'Tap to speak'}
            </Text>
          </View>
          
          <TouchableOpacity
            style={[
              styles.recordButton,
              isRecording && styles.recordButtonRecording
            ]}
            onPress={isRecording ? stopRecording : startRecording}
            disabled={isPlaying}
          >
            <Text style={styles.recordButtonText}>
              {isRecording ? '⏹️' : '🎤'}
            </Text>
          </TouchableOpacity>
        </View>
      </Animated.View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  content: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
  },
  backButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#667eea',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  backButtonText: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
  },
  headerInfo: {
    flex: 1,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 2,
  },
  endButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    backgroundColor: '#dc3545',
    borderRadius: 20,
  },
  endButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  messagesContainer: {
    flex: 1,
    paddingHorizontal: 20,
  },
  messagesContent: {
    paddingVertical: 20,
  },
  messageContainer: {
    marginBottom: 15,
  },
  userMessage: {
    alignItems: 'flex-end',
  },
  tutorMessage: {
    alignItems: 'flex-start',
  },
  messageBubble: {
    maxWidth: '80%',
    padding: 15,
    borderRadius: 20,
    position: 'relative',
  },
  userBubble: {
    backgroundColor: '#667eea',
    borderBottomRightRadius: 5,
  },
  tutorBubble: {
    backgroundColor: '#fff',
    borderBottomLeftRadius: 5,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  messageText: {
    fontSize: 16,
    lineHeight: 22,
  },
  userText: {
    color: '#fff',
  },
  tutorText: {
    color: '#333',
  },
  audioButton: {
    position: 'absolute',
    top: 10,
    right: 10,
    width: 30,
    height: 30,
    borderRadius: 15,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  audioButtonPlaying: {
    backgroundColor: 'rgba(255, 255, 255, 0.4)',
  },
  audioButtonText: {
    fontSize: 14,
  },
  timestamp: {
    fontSize: 12,
    marginTop: 5,
  },
  userTimestamp: {
    color: 'rgba(255, 255, 255, 0.7)',
    textAlign: 'right',
  },
  tutorTimestamp: {
    color: '#666',
  },
  controlsContainer: {
    backgroundColor: '#fff',
    paddingHorizontal: 20,
    paddingVertical: 20,
    borderTopWidth: 1,
    borderTopColor: '#e9ecef',
    alignItems: 'center',
  },
  recordingIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  recordingDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#dc3545',
    marginRight: 8,
  },
  recordingText: {
    fontSize: 14,
    color: '#666',
  },
  recordButton: {
    width: 70,
    height: 70,
    borderRadius: 35,
    backgroundColor: '#667eea',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#667eea',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  recordButtonRecording: {
    backgroundColor: '#dc3545',
    shadowColor: '#dc3545',
  },
  recordButtonText: {
    fontSize: 28,
  },
});
