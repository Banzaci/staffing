
import { StyleSheet, View } from "react-native";
import { BriefcaseBusiness, Building2 } from "lucide-react-native";

type Props = {
  role: "worker" | "employer";
  color: string;
};

export default function DashboardBackground({ role, color }: Props) {
  const Icon = role === "worker" ? BriefcaseBusiness : Building2;

  return (
    <View pointerEvents="none" style={styles.background}>
      <Icon
        size={300}
        strokeWidth={0.7}
        color={color}
        opacity={0.2}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  background: {
    ...StyleSheet.absoluteFill,
    justifyContent: "center",
    alignItems: "center",
  },
});
