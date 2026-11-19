
import {
  View,
  Text,
  Pressable,
  StyleSheet,
  SafeAreaView,
} from "react-native";
import { useRouter } from "expo-router";
import { useApp } from "@/providers/AppProvider";
import {
  BriefcaseBusiness,
  UsersRound,
  ChevronRight,
} from "lucide-react-native";

export default function WelcomeScreen() {
  const router = useRouter();
  const { setRole } = useApp();

  async function selectRole(role: "worker" | "employer") {
    await setRole(role);
    router.push("/login");
  }
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.emoji}>👋</Text>
        <Text style={styles.title}>Welcome!</Text>
        <Text style={styles.subtitle}>
          What would you like to do?
        </Text>

        <View style={styles.options}>
          <Pressable style={styles.card} onPress={() => selectRole("worker")}>
            <View style={styles.iconBox}>
              <BriefcaseBusiness size={44} color="#155BC7" />
            </View>
            <View style={styles.cardText}>
              <Text style={styles.cardTitle}>Find a Job</Text>
              <Text style={styles.description}>
                Find work and earn money
              </Text>
            </View>
            <ChevronRight size={24} color="#155BC7" />
          </Pressable>

          <Pressable style={styles.card} onPress={() => selectRole("employer")}>
            <View style={styles.iconBox}>
              <UsersRound size={44} color="#155BC7" />
            </View>
            <View style={styles.cardText}>
              <Text style={styles.cardTitle}>Hire Staff</Text>
              <Text style={styles.description}>
                Find people to help your business
              </Text>
            </View>
            <ChevronRight size={24} color="#155BC7" />
          </Pressable>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F5F9FF",
  },
  content: {
    flex: 1,
    justifyContent: "center",
    paddingHorizontal: 24,
  },
  emoji: {
    fontSize: 64,
    textAlign: "center",
    marginBottom: 16,
  },
  title: {
    fontSize: 36,
    fontWeight: "800",
    color: "#153B70",
    textAlign: "center",
  },
  subtitle: {
    fontSize: 18,
    color: "#64748B",
    textAlign: "center",
    marginTop: 10,
    marginBottom: 48,
  },
  options: {
    gap: 20,
  },
  card: {
    backgroundColor: "#FFFFFF",
    borderRadius: 24,
    padding: 20,
    flexDirection: "row",
    alignItems: "center",
    gap: 16,
    borderWidth: 1,
    borderColor: "#DFEAF9",
  },
  iconBox: {
    width: 76,
    height: 76,
    borderRadius: 20,
    backgroundColor: "#EAF2FF",
    justifyContent: "center",
    alignItems: "center",
  },
  cardText: {
    flex: 1,
  },
  cardTitle: {
    fontSize: 21,
    fontWeight: "700",
    color: "#153B70",
  },
  description: {
    fontSize: 14,
    color: "#64748B",
    marginTop: 5,
  },
});
