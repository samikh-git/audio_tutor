import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  Text,
  TouchableOpacity,
  SafeAreaView,
  Animated,
  ScrollView,
  Dimensions
} from 'react-native';

interface LanguageSelectorScreenProps {
  onBack: () => void;
  onStartConversation: (language: string) => void;
}

const languages = [
  { id: 'spanish', name: 'Spanish', flag: '🇪🇸', color: '#E63946' },
  { id: 'french', name: 'French', flag: '🇫🇷', color: '#3A86FF' },
  { id: 'german', name: 'German', flag: '🇩🇪', color: '#FF006E' },
  { id: 'italian', name: 'Italian', flag: '🇮🇹', color: '#8338EC' },
  { id: 'portuguese', name: 'Portuguese', flag: '🇵🇹', color: '#06FFA5' },
  { id: 'japanese', name: 'Japanese', flag: '🇯🇵', color: '#FFBE0B' },
  { id: 'korean', name: 'Korean', flag: '🇰🇷', color: '#FB5607' },
  { id: 'chinese', name: 'Chinese', flag: '🇨🇳', color: '#FF006E' },
];

export default function LanguageSelectorScreen({ onBack, onStartConversation }: LanguageSelectorScreenProps) {
  const [selectedLanguage, setSelectedLanguage] = useState<string | null>(null);
  const [fadeAnim] = useState(new Animated.Value(0));
  const [slideAnim] = useState(new Animated.Value(50));
  const scrollViewRef = React.useRef<ScrollView>(null);

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

  // Start the picker in the middle cycle (cycle 10) when component mounts
  useEffect(() => {
    const timer = setTimeout(() => {
      if (scrollViewRef.current) {
        // Start at cycle 10 (middle of 20 cycles) and center on the first language
        const startY = 10 * languages.length * 50;
        scrollViewRef.current.scrollTo({ y: startY, animated: false });
        // Set the first language as selected
        setSelectedLanguage(languages[0].id);
      }
    }, 100);
    return () => clearTimeout(timer);
  }, []);

  const handleStartConversation = () => {
    if (selectedLanguage) {
      onStartConversation(selectedLanguage);
    }
  };

  const getSelectedLanguage = () => {
    return languages.find(lang => lang.id === selectedLanguage);
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
          <Text style={styles.headerTitle}>New Conversation</Text>
          <View style={styles.placeholder} />
        </View>

        <ScrollView style={styles.scrollContent} showsVerticalScrollIndicator={false}>
          {/* Language Selection Section */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Choose a Language</Text>
            <Text style={styles.sectionSubtitle}>
              Select the language you'd like to practice
            </Text>
            
                        <View style={styles.pickerContainer}>
              <View style={styles.pickerWrapper}>
                <View style={styles.pickerSelectionIndicator} />
                <ScrollView
                  ref={scrollViewRef}
                  showsVerticalScrollIndicator={false}
                  snapToInterval={50}
                  decelerationRate="fast"
                  onMomentumScrollEnd={(event) => {
                    const y = event.nativeEvent.contentOffset.y;
                    const index = Math.round(y / 50);
                    const actualIndex = ((index - 10 * languages.length) % languages.length + languages.length) % languages.length;
                    const selectedLang = languages[actualIndex];
                    setSelectedLanguage(selectedLang.id);
                  }}
                  style={styles.pickerScrollView}
                  contentContainerStyle={styles.pickerContent}
                >
                  {/* Create 20 cycles of languages for infinite looping */}
                  {Array.from({ length: 20 }, (_, cycleIndex) => 
                    languages.map((language, index) => (
                      <View key={`cycle-${cycleIndex}-${language.id}`} style={styles.pickerItem}>
                        <Text style={[
                          styles.pickerItemText,
                          selectedLanguage === language.id && styles.pickerItemTextSelected
                        ]}>
                          {language.flag} {language.name}
                        </Text>
                      </View>
                    ))
                  ).flat()}
                </ScrollView>
              </View>
            </View>
          </View>

          {/* Start Conversation Button */}
          {selectedLanguage && (
            <View style={styles.startSection}>
              <View style={styles.selectedLanguageInfo}>
                <Text style={styles.selectedLanguageText}>
                  Selected: <Text style={styles.selectedLanguageName}>
                    {getSelectedLanguage()?.flag} {getSelectedLanguage()?.name}
                  </Text>
                </Text>
              </View>
              
              <TouchableOpacity
                style={styles.startButton}
                onPress={handleStartConversation}
              >
                <Text style={styles.startButtonText}>Start Conversation</Text>
                <Text style={styles.startButtonIcon}>🎤</Text>
              </TouchableOpacity>
            </View>
          )}
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
    justifyContent: 'space-between',
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
  },
  backButtonText: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  placeholder: {
    width: 40,
  },
  scrollContent: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 20,
  },
  section: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
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
  sectionTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  sectionSubtitle: {
    fontSize: 16,
    color: '#666',
    marginBottom: 25,
  },
  pickerContainer: {
    alignItems: 'center',
    paddingVertical: 20,
  },
  pickerWrapper: {
    height: 150,
    width: 250,
    position: 'relative',
  },
  pickerSelectionIndicator: {
    position: 'absolute',
    top: '50%',
    left: 0,
    right: 0,
    height: 50,
    backgroundColor: 'rgba(102, 126, 234, 0.1)',
    borderRadius: 8,
    zIndex: 1,
    transform: [{ translateY: -25 }],
  },
  pickerScrollView: {
    height: 150,
  },
  pickerContent: {
    paddingVertical: 50,
  },
  pickerItem: {
    height: 50,
    justifyContent: 'center',
    alignItems: 'center',
  },
  pickerItemText: {
    fontSize: 18,
    color: '#333',
    textAlign: 'center',
  },
  pickerItemTextSelected: {
    color: '#667eea',
    fontWeight: 'bold',
  },
  startSection: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
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
  selectedLanguageInfo: {
    alignItems: 'center',
    marginBottom: 20,
  },
  selectedLanguageText: {
    fontSize: 16,
    color: '#666',
  },
  selectedLanguageName: {
    fontWeight: 'bold',
    color: '#333',
  },
  startButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
    paddingHorizontal: 24,
    borderRadius: 12,
    backgroundColor: '#667eea',
    shadowColor: '#667eea',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 5,
  },
  startButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    marginRight: 8,
  },
  startButtonIcon: {
    fontSize: 20,
  },
});
