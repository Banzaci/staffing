
import { StyleSheet, Text, View } from "react-native";

type Props = {
  greeting: string;
  name: string;
  subtitle: string;
  color: string;
};

export default function DashboardHeader({
  greeting,
  name,
  subtitle,
  color,
}: Props) {
  return (
    <View style={styles.container}>
      <Text style={styles.greeting}>
        {greeting}, {name}
      </Text>
      <Text style={[styles.subtitle, { color }]}>
        {subtitle}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 32,
  },
  greeting: {
    fontSize: 28,
    fontWeight: "700",
    color: "#172033",
  },
  subtitle: {
    fontSize: 15,
    marginTop: 8,
  },
});
