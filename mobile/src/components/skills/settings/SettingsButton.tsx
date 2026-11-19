
import React from "react";
import {
  Pressable,
  View,
  Text,
  StyleSheet,
} from "react-native";
import {
  ChevronRight,
  type LucideIcon,
} from "lucide-react-native";

type Props = {
  title: string;
  subtitle: string;
  icon: LucideIcon;
  iconColor?: string;
  onPress: () => void;
};

export default function SettingsButton({
  title,
  subtitle,
  icon: Icon,
  iconColor = "#2686F5",
  onPress,
}: Props) {
  return (
    <Pressable
      onPress={onPress}
      accessibilityRole="button"
      accessibilityLabel={`${title}. ${subtitle}`}
      style={({ pressed }) => [
        styles.container,
        pressed && styles.pressed,
      ]}
    >
      <View
        style={[
          styles.iconBox,
          { backgroundColor: iconColor },
        ]}
      >
        <Icon size={29} color="#FFFFFF" strokeWidth={2.5} />
      </View>

      <View style={styles.content}>
        <Text style={styles.title}>{title}</Text>
        <Text style={styles.subtitle}>{subtitle}</Text>
      </View>

      <ChevronRight
        size={25}
        color="#111B3C"
        strokeWidth={2.5}
      />
    </Pressable>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#F2F9FF",
    borderRadius: 22,
    borderWidth: 1,
    borderColor: "#FFFFFF",
    paddingHorizontal: 18,
    paddingVertical: 14,
    marginBottom: 12,
    shadowColor: "#2476B8",
    shadowOffset: { width: 0, height: 5 },
    shadowOpacity: 0.14,
    shadowRadius: 12,
    elevation: 4,
  },
  pressed: {
    opacity: 0.8,
    transform: [{ scale: 0.98 }],
  },
  iconBox: {
    width: 58,
    height: 58,
    borderRadius: 18,
    justifyContent: "center",
    alignItems: "center",
    marginRight: 18,
  },
  content: {
    flex: 1,
  },
  title: {
    fontSize: 18,
    fontWeight: "700",
    color: "#101936",
  },
  subtitle: {
    fontSize: 13,
    color: "#34425B",
    marginTop: 4,
  },
});
