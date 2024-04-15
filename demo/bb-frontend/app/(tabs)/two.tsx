import React from 'react';
import { StyleSheet, ScrollView, Text, View } from 'react-native';

export default function TabTwoScreen() {
  const wineAttributes = {
    'apple': 'A flavor note that gives wine a taste reminiscent of apples.',
    'berry': 'A general term for wines that have a flavor profile of various kinds of berries.',
    'citrus': 'Wines with a fresh, tangy flavor profile similar to that of citrus fruits like oranges and lemons.',
    'dry': 'A wine that is not sweet, having no perception of sugar content.',
    'earth': 'Describes a taste or aroma reminiscent of wet soil, mushrooms, or a forest floor.',
    'firm tannins': 'A term indicating a strong presence of tannins, giving the wine a structured and sometimes astringent mouthfeel.',
    'floral': 'Wines that contain aromas or flavors that are reminiscent of flowers.',
    'full-bodied': 'Describes a wine that is robust and rich, often with higher alcohol content and flavor intensity.',
    'high acidity': 'Wines with bright, crisp characteristics often described as "tart".',
    'light-bodied': 'Refers to wines that are lighter in weight and mouthfeel, often with less alcohol and a delicate flavor profile.',
    'low acidity': 'Wines that are smoother and rounder, lacking in the sharpness provided by acidity.',
    'medium-bodied': 'Wines that fall between light and full-bodied with a moderate feel and balanced attributes.',
    'oak': 'A flavor profile imparted by aging wine in oak barrels, contributing to notes of vanilla, toast, and spices.',
    'off-dry': 'A wine that has a slight sweetness to it, typically with sugar content that is detectable but not high.',
    'semi-sweet': 'Wines that are more perceptibly sweet than off-dry wines, but not as sweet as dessert wines.',
    'smooth tannins': 'Wines with a softer, more velvety feel from tannins, lacking harshness.',
    'spice': 'Describes wines with flavors or aromas reminiscent of spices, which can range from black pepper to cinnamon.',
    'stone fruit': 'A flavor profile in wines that suggests fruits with pits, like peaches and apricots.',
    'sweet': 'Wines with high sugar content and a noticeably sweet taste.',
    'tropical': 'Wines with flavors that recall tropical fruits such as pineapple, mango, or papaya.',
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Bottle Buddy</Text>
      <ScrollView style={styles.attributeContainer}>
        {Object.entries(wineAttributes).map(([attribute, description], index) => (
          <View key={index} style={styles.attributeBox}>
            <Text style={styles.attributeTitle}>{attribute}</Text>
            <Text style={styles.attributeDescription}>{description}</Text>
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
    paddingTop: 20,
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  attributeContainer: {
    width: '90%',
  },
  attributeBox: {
    backgroundColor: '#f0f0f0',
    borderRadius: 10,
    padding: 15,
    marginBottom: 10,
  },
  attributeTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  attributeDescription: {
    fontSize: 16,
    color: '#333',
    marginTop: 5,
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: '80%',
  },
});
