import React, { useState } from 'react';
import { StyleSheet, TouchableOpacity, ScrollView, Text, View, ActivityIndicator } from 'react-native';

export default function TabOneScreen() {
  const [selectedButtons, setSelectedButtons] = useState<number[]>([]);
  const [results, setResults] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const buttons = [
    'apple', 'berry', 'citrus', 'dry', 'earth', 'firm tannins', 'floral', 'full-bodied',
    'high acidity', 'light-bodied', 'low acidity', 'medium-bodied', 'oak', 'off-dry',
    'semi-sweet', 'smooth tannins', 'spice', 'stone fruit', 'sweet', 'tropical'
  ];

  const handlePress = (index: number) => {
    setSelectedButtons(currentSelected => {
      return currentSelected.includes(index) ? currentSelected.filter(i => i !== index) : [...currentSelected, index];
    });
  };

  const handleFindClick = async () => {
    setLoading(true);
    setError('');
    const selectedCriteria = selectedButtons.map(index => buttons[index]);
    try {
      const response = await fetch('http://127.0.0.1:5000/find', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({criteria: selectedCriteria}),
      });
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error during fetch operation:', error);
      setError('Failed to fetch results. Please try again.');
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
  <View style={styles.container}>
    <Text style={styles.title}>Bottle Buddy</Text>
    <View style={styles.separator} />
    <ScrollView style={styles.buttonContainer} contentContainerStyle={styles.buttonInnerContainer}>
      {buttons.map((button, index) => (
        <TouchableOpacity
          key={index}
          style={[styles.button, { borderColor: selectedButtons.includes(index) ? '#6a0dad' : '#d3d3d3' }]}
          onPress={() => handlePress(index)}
        >
          <Text style={[styles.buttonText, { color: selectedButtons.includes(index) ? '#6a0dad' : '#d3d3d3' }]}>{button}</Text>
        </TouchableOpacity>
      ))}
      <TouchableOpacity style={styles.findButton} onPress={handleFindClick} disabled={loading}>
        {loading ? <ActivityIndicator size="small" color="#FFF" /> : <Text style={styles.findButtonText}>Find</Text>}
      </TouchableOpacity>
      {error ? <Text style={styles.errorText}>{error}</Text> : null}
      {results.map((result, index) => (
        <View key={index} style={styles.resultCard}>
          <Text style={styles.resultText}>{result}</Text>
        </View>
      ))}
    </ScrollView>
  </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 20,
  },
  separator: {
    marginVertical: 10,
    height: 1,
    width: '80%',
  },
  buttonContainer: {
    width: '100%',
  },
  buttonInnerContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    padding: 10,
  },
  button: {
    padding: 10,
    margin: 5,
    borderRadius: 12,
    borderWidth: 2,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'transparent',
  },
  buttonText: {
    fontSize: 14,
  },
  findButton: {
    padding: 12,
    marginTop: 20,
    borderRadius: 12,
    backgroundColor: '#6a0dad',
    borderWidth: 2,
    borderColor: '#6a0dad',
    width: '50%',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 20,
  },
  findButtonText: {
    fontSize: 16,
    color: '#d3d3d3',
    fontWeight: 'bold',
  },
  resultCard: {
    backgroundColor: 'white',
    borderRadius: 10,
    padding: 15,
    marginVertical: 5,
    marginHorizontal: 40, // Increase horizontal margin to make the card narrower
    marginBottom: 10,
    flexShrink: 1, // Allows card to shrink and wrap
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 5,
    alignItems: 'center',
    justifyContent: 'center',
  },
  resultText: {
    fontSize: 14,
    color: 'black',
    textAlign: 'center', // Center text to make it look better when wrapped
    flexShrink: 1, // Allows text to shrink and wrap
  },
  errorText: {
    fontSize: 16,
    color: 'red',
    padding: 10,
    textAlign: 'center',
    width: '80%'
  }
});