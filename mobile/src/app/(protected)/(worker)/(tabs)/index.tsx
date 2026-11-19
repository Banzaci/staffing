
import { StyleSheet, Text, View } from "react-native";
import { BriefcaseBusiness } from "lucide-react-native";

import { useSession } from "@/hooks/useSession";
import { useLanguage } from "@/providers/LanguageProvider";
import DashboardActionCard from "@/components/dashboard/DashboardActionCard";

const WORKER_COLOR = "#155BC7";

export default function WorkerIndex() {
  const { data: session, isPending } = useSession();
  const { t } = useLanguage();

  
  if (isPending || !session) return null;
  
  const hasSkills = session.skills.length > 0;
  console.log("Worker skills:", session.skills);
  console.log("Has skills:", hasSkills);

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.greeting}>
          {t.dashboardGreeting}, {session.user.first_name}
        </Text>
        <Text style={styles.subtitle}>
          {t.dashboardSubtitle}
        </Text>
      </View>

      {!hasSkills && (
        <DashboardActionCard
          title={t.addSkills}
          description={t.addSkillsDescription}
          icon={BriefcaseBusiness}
          color={WORKER_COLOR}
          onPress={() => {}}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFFFFF",
    paddingHorizontal: 24,
    paddingTop: 48,
  },
  header: {
    marginBottom: 32,
  },
  greeting: {
    fontSize: 28,
    fontWeight: "700",
    color: "#172033",
  },
  subtitle: {
    fontSize: 16,
    color: "#64748B",
    marginTop: 8,
  },
});
