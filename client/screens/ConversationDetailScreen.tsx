import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  Text,
  TouchableOpacity,
  ScrollView,
  SafeAreaView,
  Animated,
  Dimensions,
} from 'react-native';

const { width, height } = Dimensions.get('window');

interface ConversationDetailScreenProps {
  conversation: {
    id: string;
    date: string;
    language: string;
    preview: string;
    duration: string;
  };
  onBack: () => void;
}

export default function ConversationDetailScreen({ conversation, onBack }: ConversationDetailScreenProps) {
  const [isTranscriptExpanded, setIsTranscriptExpanded] = useState(false);
  const [isReportExpanded, setIsReportExpanded] = useState(false);
  const [fadeAnim] = useState(new Animated.Value(0));
  const [slideAnim] = useState(new Animated.Value(50));

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
  }, []);

  // Mock data for transcript and report
  const fullTranscript = `Date: ${conversation.date}
Language: ${conversation.language}

USER: Hola, ¿cómo estás? Me llamo María.
TUTOR: ¡Hola María! Mucho gusto. ¿Cómo estás hoy? ¿Te gustaría practicar español?

USER: Sí, por favor. Quiero mejorar mi pronunciación.
TUTOR: ¡Excelente! La pronunciación es muy importante. Empecemos con algunos ejercicios básicos.

USER: ¿Puedes ayudarme con los verbos irregulares?
TUTOR: ¡Por supuesto! Los verbos irregulares pueden ser complicados. Vamos a practicar "ser", "estar" y "ir".

USER: Gracias por tu ayuda. Esto es muy útil.
TUTOR: ¡De nada! Estás progresando muy bien. ¿Te gustaría continuar con más práctica?

USER: Sí, pero necesito un descanso.
TUTOR: Entiendo perfectamente. Los descansos son importantes para el aprendizaje. ¡Hasta la próxima!`;

  const fullReport = `Language Learning Progress Report
Student: María
Session Date: ${conversation.date}
Language: ${conversation.language}

STRENGTHS:
• Good basic vocabulary foundation
• Enthusiastic attitude toward learning
• Clear pronunciation of basic words
• Willingness to practice and ask questions

AREAS FOR IMPROVEMENT:
• Verb conjugation needs more practice
• Some pronunciation of "r" sounds could be clearer
• More exposure to natural conversation flow needed

RECOMMENDATIONS:
1. Practice irregular verbs daily (ser, estar, ir, tener)
2. Listen to native Spanish speakers for pronunciation
3. Engage in more conversational practice
4. Review basic grammar structures

NEXT SESSION FOCUS:
• Advanced verb conjugations
• Pronunciation exercises
• Real-world conversation scenarios

Overall Progress: Good foundation, ready for intermediate level practice.`;

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      weekday: 'long',
      year: 'numeric', 
      month: 'long', 
      day: 'numeric'
    });
  };

  const toggleTranscript = () => {
    setIsTranscriptExpanded(!isTranscriptExpanded);
  };

  const toggleReport = () => {
    setIsReportExpanded(!isReportExpanded);
  };

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
            <Text style={styles.headerTitle}>{conversation.language}</Text>
            <Text style={styles.headerDate}>{formatDate(conversation.date)}</Text>
          </View>
          <View style={styles.headerDuration}>
            <Text style={styles.durationText}>{conversation.duration}</Text>
          </View>
        </View>

        <ScrollView style={styles.scrollContent} showsVerticalScrollIndicator={false}>
          {/* Transcript Section */}
          <View style={styles.section}>
            <View style={styles.sectionHeader}>
              <Text style={styles.sectionTitle}>Conversation Transcript</Text>
              <TouchableOpacity onPress={toggleTranscript}>
                <Text style={styles.expandButton}>
                  {isTranscriptExpanded ? 'Collapse' : 'Expand'}
                </Text>
              </TouchableOpacity>
            </View>
            <View style={styles.sectionContent}>
              <Text style={styles.sectionText} numberOfLines={isTranscriptExpanded ? undefined : 6}>
                {fullTranscript}
              </Text>
            </View>
          </View>

          {/* Report Section */}
          <View style={styles.section}>
            <View style={styles.sectionHeader}>
              <Text style={styles.sectionTitle}>Learning Report</Text>
              <TouchableOpacity onPress={toggleReport}>
                <Text style={styles.expandButton}>
                  {isReportExpanded ? 'Collapse' : 'Expand'}
                </Text>
              </TouchableOpacity>
            </View>
            <View style={styles.sectionContent}>
              <Text style={styles.sectionText} numberOfLines={isReportExpanded ? undefined : 8}>
                {fullReport}
              </Text>
            </View>
          </View>
        </ScrollView>
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
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  headerDate: {
    fontSize: 14,
    color: '#666',
    marginTop: 2,
  },
  headerDuration: {
    backgroundColor: '#667eea',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 15,
  },
  durationText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  scrollContent: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 20,
  },
  section: {
    backgroundColor: '#fff',
    borderRadius: 16,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  expandButton: {
    color: '#667eea',
    fontSize: 14,
    fontWeight: '600',
  },
  sectionContent: {
    padding: 20,
  },
  sectionText: {
    fontSize: 14,
    lineHeight: 22,
    color: '#333',
  },
});
