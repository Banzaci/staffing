
import { useState } from "react";
import {
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Modal,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { useRouter } from "expo-router";
import {
  ArrowLeft,
  Bell,
  BriefcaseBusiness,
  Check,
  ChevronDown,
  Coins,
  FileText,
  X,
} from "lucide-react-native";

import { useSession } from "@/hooks/useSession";
import { useWorkerSkills } from "@/hooks/useWorkerSkills";
import SkillIcon from "@/components/skills/SkillIcon";
import type { Skill } from "@/app/services/skills";

const BLUE = "#0877F9";
const NAVY = "#08143E";

const COLORS = [
  { main: "#FF742C", light: "#FFF0E8" },
  { main: "#08B979", light: "#DDF9EC" },
  { main: "#9B55F5", light: "#F1E6FF" },
  { main: "#F6A500", light: "#FFF3CC" },
  { main: "#ED459D", light: "#FFE1F1" },
  { main: "#168BF4", light: "#DDF1FF" },
];

type Draft = {
  hourlyRate: string;
  description: string;
};

export default function Screen() {
  const router = useRouter();
  const { data: session } = useSession();

  const {
    skills,
    isPending,
    isError,
    saveSkill,
    removeSkill,
  } = useWorkerSkills();

  const [selectedSkill, setSelectedSkill] =
    useState<Skill | null>(null);
  const [years, setYears] = useState(0);
  const [drafts, setDrafts] = useState<Record<string, Draft>>({});
  const [hourlyRate, setHourlyRate] = useState("");
  const [description, setDescription] = useState("");
  const [showYears, setShowYears] = useState(false);

  const selectedIds = new Set(
    session?.skills.map((item) => item.skill_id) ?? []
  );

  const isSaving =
    saveSkill.isPending || removeSkill.isPending;

  function skillName(skill: Skill) {
    return skill.translations.en ?? skill.code;
  }

  function skillColor(skill: Skill) {
    const index = skills.findIndex((s) => s.id === skill.id);
    return COLORS[Math.max(0, index) % COLORS.length];
  }

  function openSkill(skill: Skill) {
    const existing = session?.skills.find(
      (item) => item.skill_id === skill.id
    );

    setYears(existing?.years_experience ?? 0);
    setHourlyRate(drafts[skill.id]?.hourlyRate ?? "");
    setDescription(drafts[skill.id]?.description ?? "");
    setShowYears(false);
    setSelectedSkill(skill);
  }

  async function handleSave() {
    if (!selectedSkill || isSaving) return;

    try {
      await saveSkill.mutateAsync({
        skillId: selectedSkill.id,
        yearsExperience: years,
      });

      setDrafts((prev) => ({
        ...prev,
        [selectedSkill.id]: {
          hourlyRate,
          description,
        },
      }));

      setSelectedSkill(null);
    } catch {
      Alert.alert("Error", "Could not save skill.");
    }
  }

  async function handleDelete() {
    if (!selectedSkill || isSaving) return;

    try {
      await removeSkill.mutateAsync(selectedSkill.id);
      setSelectedSkill(null);
    } catch {
      Alert.alert("Error", "Could not remove skill.");
    }
  }

  const modalColor = selectedSkill
    ? skillColor(selectedSkill)
    : COLORS[0];

  return (
    <View style={styles.container}>
      <View style={styles.topBar}>
        <Pressable
          onPress={() => router.back()}
          style={styles.backButton}
          accessibilityRole="button"
          accessibilityLabel="Go back"
        >
          <ArrowLeft size={25} color={NAVY} />
        </Pressable>

        <View style={styles.brand}>
          <Text style={styles.brandText}>Staffing,</Text>
          <Text style={styles.brandText}>Staffing</Text>
        </View>

        <Pressable
          style={styles.bellButton}
          accessibilityLabel="Notifications"
          accessibilityRole="button"
        >
          <Bell size={25} color={NAVY} />
          <View style={styles.notificationDot} />
        </Pressable>
      </View>

      <ScrollView
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        <Text style={styles.heading}>Choose your skills</Text>
        <Text style={styles.subtitle}>
          Select one or more roles you can work in.
        </Text>

        {isPending ? (
          <ActivityIndicator size="large" color={BLUE} />
        ) : isError ? (
          <Text style={styles.error}>
            Unable to load skills.
          </Text>
        ) : (
          <View style={styles.grid}>
            {skills.map((skill) => {
              const color = skillColor(skill);
              const selected = selectedIds.has(skill.id);

              return (
                <Pressable
                  key={skill.id}
                  onPress={() => openSkill(skill)}
                  accessibilityRole="button"
                  accessibilityLabel={skillName(skill)}
                  accessibilityState={{ selected }}
                  style={({ pressed }) => [
                    styles.skillCard,
                    selected && styles.selectedCard,
                    pressed && { opacity: 0.85 },
                  ]}
                >
                  <View
                    style={[
                      styles.skillIcon,
                      { backgroundColor: color.light },
                    ]}
                  >
                    <SkillIcon
                      code={skill.code}
                      size={47}
                      color={color.main}
                    />
                  </View>

                  <Text
                    style={styles.skillName}
                    numberOfLines={2}
                  >
                    {skillName(skill)}
                  </Text>

                  <View
                    style={[
                      styles.selection,
                      selected && styles.selectionActive,
                    ]}
                  >
                    {selected && (
                      <Check
                        size={17}
                        color="#FFFFFF"
                        strokeWidth={3}
                      />
                    )}
                  </View>
                </Pressable>
              );
            })}
          </View>
        )}

        <Pressable
          style={styles.continueButton}
          onPress={() => router.back()}
        >
          <Check size={23} color="#FFFFFF" strokeWidth={3} />
          <Text style={styles.continueText}>Continue</Text>
        </Pressable>
      </ScrollView>

      <Modal
        visible={selectedSkill !== null}
        transparent
        animationType="slide"
        onRequestClose={() => {
          if (!isSaving) setSelectedSkill(null);
        }}
      >
        <KeyboardAvoidingView
          style={styles.modalOverlay}
          behavior={Platform.OS === "ios" ? "padding" : undefined}
        >
          <View style={styles.modal}>
            <Pressable
              style={styles.close}
              disabled={isSaving}
              onPress={() => setSelectedSkill(null)}
            >
              <X size={23} color={NAVY} />
            </Pressable>

            {selectedSkill && (
              <ScrollView
                showsVerticalScrollIndicator={false}
                keyboardShouldPersistTaps="handled"
              >
                <View style={styles.modalHeading}>
                  <View
                    style={[
                      styles.modalIcon,
                      { backgroundColor: modalColor.light },
                    ]}
                  >
                    <SkillIcon
                      code={selectedSkill.code}
                      size={45}
                      color={modalColor.main}
                    />
                  </View>

                  <Text style={styles.modalTitle}>
                    {skillName(selectedSkill)}
                  </Text>
                </View>

                <View style={styles.fieldCard}>
                  <View style={styles.fieldRow}>
                    <BriefcaseBusiness size={23} color={BLUE} />
                    <Text style={styles.fieldLabel}>
                      Experience
                    </Text>

                    <Pressable
                      style={styles.yearSelector}
                      onPress={() => setShowYears(!showYears)}
                    >
                      <Text style={styles.yearValue}>
                        {years} {years === 1 ? "year" : "years"}
                      </Text>
                      <ChevronDown size={19} color={NAVY} />
                    </Pressable>
                  </View>

                  {showYears && (
                    <ScrollView
                      style={styles.yearOptions}
                      nestedScrollEnabled
                    >
                      {Array.from(
                        { length: 41 },
                        (_, i) => i
                      ).map((value) => (
                        <Pressable
                          key={value}
                          style={styles.yearOption}
                          onPress={() => {
                            setYears(value);
                            setShowYears(false);
                          }}
                        >
                          <Text style={styles.yearOptionText}>
                            {value} {value === 1 ? "year" : "years"}
                          </Text>
                        </Pressable>
                      ))}
                    </ScrollView>
                  )}
                </View>

                <View style={styles.fieldCard}>
                  <View style={styles.fieldRow}>
                    <Coins size={24} color="#F6A500" />
                    <Text style={styles.fieldLabel}>
                      Expected hourly rate
                    </Text>

                    <TextInput
                      style={styles.rateInput}
                      value={hourlyRate}
                      onChangeText={setHourlyRate}
                      keyboardType="decimal-pad"
                      placeholder="0"
                      placeholderTextColor="#94A3B8"
                    />
                  </View>
                </View>

                <View style={styles.fieldCard}>
                  <View style={styles.descriptionHeader}>
                    <FileText size={23} color={BLUE} />
                    <Text style={styles.fieldLabel}>
                      Description
                    </Text>
                    <Text style={styles.optional}>
                      (optional)
                    </Text>
                  </View>

                  <TextInput
                    style={styles.descriptionInput}
                    value={description}
                    onChangeText={setDescription}
                    multiline
                    textAlignVertical="top"
                    placeholder="Describe your experience..."
                    placeholderTextColor="#94A3B8"
                  />
                </View>

                <Pressable
                  style={styles.saveButton}
                  disabled={isSaving}
                  onPress={handleSave}
                >
                  {saveSkill.isPending ? (
                    <ActivityIndicator color="#FFFFFF" />
                  ) : (
                    <>
                      <Check
                        size={23}
                        color="#FFFFFF"
                        strokeWidth={3}
                      />
                      <Text style={styles.saveText}>Save</Text>
                    </>
                  )}
                </Pressable>

                {selectedIds.has(selectedSkill.id) ? (
                  <Pressable
                    style={styles.cancelButton}
                    disabled={isSaving}
                    onPress={handleDelete}
                  >
                    <Text style={styles.cancelText}>
                      Remove skill
                    </Text>
                  </Pressable>
                ) : (
                  <Pressable
                    style={styles.cancelButton}
                    onPress={() => setSelectedSkill(null)}
                  >
                    <Text style={styles.cancelText}>
                      Cancel
                    </Text>
                  </Pressable>
                )}
              </ScrollView>
            )}
          </View>
        </KeyboardAvoidingView>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#E4F5FF",
  },
  topBar: {
    height: 80,
    paddingHorizontal: 20,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    backgroundColor: "#F0FAFF",
  },
  backButton: {
    width: 40,
    justifyContent: "center",
  },
  brand: {
    alignItems: "center",
  },
  brandText: {
    fontSize: 20,
    fontWeight: "900",
    color: "#0752A4",
    lineHeight: 21,
  },
  bellButton: {
    width: 40,
    alignItems: "center",
  },
  notificationDot: {
    position: "absolute",
    top: -2,
    right: 4,
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: "#FF442F",
  },
  content: {
    paddingHorizontal: 18,
    paddingTop: 22,
    paddingBottom: 45,
  },
  heading: {
    fontSize: 27,
    fontWeight: "800",
    textAlign: "center",
    color: NAVY,
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 14,
    textAlign: "center",
    color: NAVY,
    marginBottom: 28,
  },
  grid: {
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "space-between",
    rowGap: 13,
  },
  skillCard: {
    width: "48%",
    minHeight: 167,
    borderRadius: 22,
    backgroundColor: "rgba(255,255,255,0.82)",
    borderWidth: 2,
    borderColor: "#FFFFFF",
    alignItems: "center",
    justifyContent: "center",
    padding: 12,
    shadowColor: "#2589D5",
    shadowOpacity: 0.08,
    shadowOffset: { width: 0, height: 4 },
    shadowRadius: 8,
    elevation: 2,
  },
  selectedCard: {
    borderColor: BLUE,
  },
  skillIcon: {
    width: 85,
    height: 85,
    borderRadius: 43,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 8,
  },
  skillName: {
    fontSize: 17,
    fontWeight: "800",
    color: NAVY,
    textAlign: "center",
  },
  selection: {
    position: "absolute",
    top: 13,
    right: 13,
    width: 26,
    height: 26,
    borderRadius: 13,
    borderWidth: 2,
    borderColor: "#AAB8C9",
    backgroundColor: "#FFFFFF",
    alignItems: "center",
    justifyContent: "center",
  },
  selectionActive: {
    borderColor: BLUE,
    backgroundColor: BLUE,
  },
  continueButton: {
    backgroundColor: BLUE,
    borderRadius: 28,
    paddingVertical: 16,
    marginTop: 30,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    gap: 12,
  },
  continueText: {
    color: "#FFFFFF",
    fontSize: 20,
    fontWeight: "800",
  },
  error: {
    color: "#DC2626",
    textAlign: "center",
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: "rgba(5,15,35,0.4)",
    justifyContent: "flex-end",
  },
  modal: {
    backgroundColor: "#E4F5FF",
    borderTopLeftRadius: 30,
    borderTopRightRadius: 30,
    paddingHorizontal: 20,
    paddingTop: 12,
    paddingBottom: 30,
    maxHeight: "92%",
  },
  close: {
    alignSelf: "flex-end",
    padding: 8,
  },
  modalHeading: {
    flexDirection: "row",
    alignItems: "center",
    gap: 18,
    marginBottom: 28,
    paddingHorizontal: 10,
  },
  modalIcon: {
    width: 78,
    height: 78,
    borderRadius: 39,
    justifyContent: "center",
    alignItems: "center",
  },
  modalTitle: {
    flex: 1,
    fontSize: 26,
    fontWeight: "800",
    color: NAVY,
  },
  fieldCard: {
    backgroundColor: "rgba(255,255,255,0.88)",
    borderRadius: 20,
    padding: 16,
    marginBottom: 14,
  },
  fieldRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
  },
  fieldLabel: {
    fontSize: 15,
    fontWeight: "700",
    color: NAVY,
    flexShrink: 1,
  },
  yearSelector: {
    marginLeft: "auto",
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    backgroundColor: "#FFFFFF",
    borderWidth: 1,
    borderColor: "#D8E6F3",
    borderRadius: 14,
    paddingHorizontal: 14,
    paddingVertical: 11,
  },
  yearValue: {
    fontSize: 15,
    fontWeight: "700",
    color: NAVY,
  },
  yearOptions: {
    maxHeight: 170,
    marginTop: 12,
  },
  yearOption: {
    paddingVertical: 11,
    paddingHorizontal: 14,
  },
  yearOptionText: {
    color: NAVY,
    fontSize: 15,
  },
  rateInput: {
    marginLeft: "auto",
    width: 95,
    backgroundColor: "#FFFFFF",
    borderWidth: 1,
    borderColor: "#D8E6F3",
    borderRadius: 14,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 16,
    fontWeight: "700",
    textAlign: "right",
    color: NAVY,
  },
  descriptionHeader: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    marginBottom: 12,
  },
  optional: {
    color: "#7C8FA7",
    fontSize: 13,
  },
  descriptionInput: {
    backgroundColor: "#FFFFFF",
    borderWidth: 1,
    borderColor: "#D8E6F3",
    borderRadius: 15,
    minHeight: 110,
    padding: 14,
    fontSize: 15,
    color: NAVY,
  },
  saveButton: {
    backgroundColor: BLUE,
    borderRadius: 28,
    paddingVertical: 17,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    gap: 12,
    marginTop: 12,
  },
  saveText: {
    color: "#FFFFFF",
    fontSize: 20,
    fontWeight: "800",
  },
  cancelButton: {
    paddingVertical: 20,
    alignItems: "center",
  },
  cancelText: {
    color: BLUE,
    fontSize: 16,
    fontWeight: "600",
  },
});
