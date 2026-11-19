
import { Pressable, StyleSheet, Text, View } from "react-native";
import {
  ArrowRight,
  type LucideIcon,
} from "lucide-react-native";

type Props = {
  title: string;
  description: string;
  color: string;
  icon: LucideIcon;
  onPress: () => void;
};

export default function DashboardActionCard({
  title,
  description,
  color,
  icon: Icon,
  onPress,
}: Props) {
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={title}
      onPress={onPress}
      style={styles.card}
    >
      <View style={[styles.iconContainer, { backgroundColor: `${color}12` }]}>
        <Icon size={32} color={color} strokeWidth={1.8} />
      </View>

      <View style={styles.content}>
        <Text style={styles.title}>{title}</Text>
        <Text style={styles.description}>{description}</Text>
      </View>

      <ArrowRight size={22} color={color} />
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: "#FFFFFF",
    borderRadius: 18,
    borderWidth: 1,
    borderColor: "#E6EAF0",
    padding: 18,
    flexDirection: "row",
    alignItems: "center",
    gap: 14,
  },
  iconContainer: {
    width: 62,
    height: 62,
    borderRadius: 16,
    justifyContent: "center",
    alignItems: "center",
  },
  content: {
    flex: 1,
  },
  title: {
    fontSize: 17,
    fontWeight: "700",
    color: "#172033",
  },
  description: {
    fontSize: 13,
    color: "#64748B",
    marginTop: 5,
    lineHeight: 19,
  },
});
