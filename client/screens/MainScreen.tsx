import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  Text,
  TouchableOpacity,
  Alert,
  Animated,
  FlatList,
  SafeAreaView,
} from 'react-native';

interface MainScreenProps {
  onLogout: () => void;
  onNavigateToConversation: (conversation: Conversation) => void;
  onNavigateToNewConversation: () => void;
  onNavigateToProfile: () => void;
}

interface Conversation {
  id: string;
  date: string;
  language: string;
  preview: string;
  duration: string;
}

export default function MainScreen({ onLogout, onNavigateToConversation, onNavigateToNewConversation, onNavigateToProfile }: MainScreenProps) {
  const [fadeAnim] = useState(new Animated.Value(0));

  useEffect(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 800,
      useNativeDriver: true,
    }).start();
  }, []);

  // Mock conversation data
  const conversations: Conversation[] = [
    {
      id: '1',
      date: '2024-01-15',
      language: 'Spanish',
      preview: 'Hola, ¿cómo estás? Me llamo...',
      duration: '12 min',
    },
    {
      id: '2',
      date: '2024-01-14',
      language: 'French',
      preview: 'Bonjour! Comment allez-vous?',
      duration: '8 min',
    },
    {
      id: '3',
      date: '2024-01-13',
      language: 'Japanese',
      preview: 'こんにちは！お元気ですか？',
      duration: '15 min',
    },
    {
      id: '4',
      date: '2024-01-12',
      language: 'German',
      preview: 'Hallo! Wie geht es dir?',
      duration: '10 min',
    },
  ];

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
      return 'Today';
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Yesterday';
    } else {
      return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric',
        year: date.getFullYear() !== today.getFullYear() ? 'numeric' : undefined
      });
    }
  };

  const renderConversation = ({ item }: { item: Conversation }) => (
    <TouchableOpacity 
      style={styles.conversationCard}
      onPress={() => onNavigateToConversation(item)}
    >
      <View style={styles.conversationHeader}>
        <View style={styles.languageBadge}>
          <Text style={styles.languageText}>{item.language}</Text>
        </View>
        <Text style={styles.dateText}>{formatDate(item.date)}</Text>
      </View>
      <Text style={styles.previewText} numberOfLines={2}>
        {item.preview}
      </Text>
      <View style={styles.conversationFooter}>
        <Text style={styles.durationText}>{item.duration}</Text>
        <TouchableOpacity style={styles.playButton}>
          <Text style={styles.playButtonText}>▶</Text>
        </TouchableOpacity>
      </View>
    </TouchableOpacity>
  );

  const handleNewConversation = () => {
    onNavigateToNewConversation();
  };

  const handleProfileSettings = () => {
    onNavigateToProfile();
  };

  return (
    <SafeAreaView style={styles.mainContainer}>
      <Animated.View style={[styles.mainContent, { opacity: fadeAnim }]}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>Audio Tutor</Text>
          <TouchableOpacity style={styles.profileButton} onPress={handleProfileSettings}>
            <Text style={styles.profileIcon}>👤</Text>
          </TouchableOpacity>
        </View>

        {/* Feed Section */}
        <View style={styles.feedContainer}>
          <View style={styles.feedHeader}>
            <Text style={styles.feedTitle}>Recent Conversations</Text>
            <Text style={styles.feedSubtitle}>Continue your language learning journey</Text>
          </View>

          {conversations.length > 0 ? (
            <FlatList
              data={conversations}
              renderItem={renderConversation}
              keyExtractor={(item) => item.id}
              showsVerticalScrollIndicator={false}
              contentContainerStyle={styles.conversationList}
            />
          ) : (
            <View style={styles.emptyState}>
              <Text style={styles.emptyStateIcon}>🎤</Text>
              <Text style={styles.emptyStateTitle}>No conversations yet</Text>
              <Text style={styles.emptyStateText}>
                Start your first conversation to begin learning!
              </Text>
            </View>
          )}
        </View>

        {/* Floating Action Button */}
        <TouchableOpacity style={styles.fab} onPress={handleNewConversation}>
          <Text style={styles.fabText}>+</Text>
        </TouchableOpacity>
      </Animated.View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  mainContainer: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  mainContent: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  profileButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#667eea',
    justifyContent: 'center',
    alignItems: 'center',
  },
  profileIcon: {
    fontSize: 20,
  },
  feedContainer: {
    flex: 1,
    paddingHorizontal: 20,
  },
  feedHeader: {
    paddingVertical: 20,
  },
  feedTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  feedSubtitle: {
    fontSize: 16,
    color: '#666',
  },
  conversationList: {
    paddingBottom: 100, // Space for FAB
  },
  conversationCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  conversationHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  languageBadge: {
    backgroundColor: '#667eea',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  languageText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  dateText: {
    fontSize: 14,
    color: '#666',
  },
  previewText: {
    fontSize: 16,
    color: '#333',
    lineHeight: 22,
    marginBottom: 15,
  },
  conversationFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  durationText: {
    fontSize: 14,
    color: '#666',
  },
  playButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#667eea',
    justifyContent: 'center',
    alignItems: 'center',
  },
  playButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  fab: {
    position: 'absolute',
    bottom: 30,
    right: 30,
    width: 60,
    height: 60,
    borderRadius: 30,
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
  fabText: {
    color: '#fff',
    fontSize: 32,
    fontWeight: 'bold',
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 60,
  },
  emptyStateIcon: {
    fontSize: 80,
    marginBottom: 20,
  },
  emptyStateTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  emptyStateText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    paddingHorizontal: 40,
  },
});
