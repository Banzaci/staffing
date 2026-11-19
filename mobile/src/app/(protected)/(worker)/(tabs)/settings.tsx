
import React from "react";
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
} from "react-native";
import {
  UserRound,
  ChefHat,
  BriefcaseBusiness,
  MapPin,
  Plane,
  Settings,
} from "lucide-react-native";
import { useRouter } from "expo-router";
import SettingsButton from "@/components/skills/settings/SettingsButton";

export default function Screen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.header}>
          <Text style={styles.heading}>
            Inställningar
          </Text>
          <Text style={styles.subtitle}>
            Hantera din profil och dina inställningar.
          </Text>
        </View>
        <SettingsButton
          title="Profile"
          subtitle="Personal information and contact details"
          icon={UserRound}
          iconColor="#2686F5"
          onPress={() => router.push("/profile")}
        />
        <SettingsButton
          title="Skills & Hourly Rate"
          subtitle="Your skills, experience and expected pay"
          icon={ChefHat}
          iconColor="#FF9800"
          onPress={() => router.push("/(protected)/(worker)/(settings)/skills")}
        />

        <SettingsButton
          title="Work Experience"
          subtitle="Previous jobs and verified experience"
          icon={BriefcaseBusiness}
          iconColor="#A855F7"
          onPress={() => router.push("/experience")}
        />

        <SettingsButton
          title="Locations"
          subtitle="Your current location and preferred areas"
          icon={MapPin}
          iconColor="#10B981"
          onPress={() => router.push("/(protected)/(worker)/(settings)/locations")}
        />

        <SettingsButton
          title="Travel"
          subtitle="Travel preferences and maximum distance"
          icon={Plane}
          iconColor="#2686F5"
          onPress={() => router.push("/travel")}
        />

        <SettingsButton
          title="Other Settings"
          subtitle="Notifications, language and account"
          icon={Settings}
          iconColor="#64748B"
          onPress={() => router.push("/preferences")}
        />

      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#D9EFFF",
  },
  content: {
    paddingHorizontal: 20,
    paddingTop: 55,
    paddingBottom: 40,
  },
  header: {
    marginBottom: 32,
    alignItems: "center",
  },
  heading: {
    fontSize: 30,
    fontWeight: "800",
    color: "#101936",
  },
  subtitle: {
    fontSize: 14,
    color: "#34425B",
    textAlign: "center",
    marginTop: 8,
  },
});
