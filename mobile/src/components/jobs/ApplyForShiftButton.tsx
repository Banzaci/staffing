
import { Alert, Pressable, StyleSheet, Text } from "react-native";
import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import { api } from "@/libs/api";

type ShiftApplication = {
  id: string;
  job_shift_id: string;
  status: string;
};

type Props = {
  shiftId: string;
};

export default function ApplyForShiftButton({ shiftId }: Props) {
  const queryClient = useQueryClient();

  const { data: applications = [], isPending: isLoading } = useQuery<
    ShiftApplication[]
  >({
    queryKey: ["my-shift-applications"],
    queryFn: () =>
      api<ShiftApplication[]>(
        "/api/private/v1/worker/shifts/applications"
      ),
  });

  const application = applications.find(
    (item) => item.job_shift_id === shiftId
  );

  const applyMutation = useMutation({
    mutationFn: () =>
      api<{ id: string; status: string }>(
        `/api/private/v1/worker/shifts/${shiftId}/apply`,
        { method: "POST" }
      ),
    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey: ["my-shift-applications"],
      });
    },
    onError: () => {
      Alert.alert("Error", "Could not submit your application.");
    },
  });

  const disabled =
    isLoading || !!application || applyMutation.isPending;

  const label = applyMutation.isPending
    ? "Applying..."
    : isLoading
      ? "Loading..."
      : application
        ? application.status.charAt(0).toUpperCase() +
          application.status.slice(1)
        : "Apply for job";

  return (
    <Pressable
      style={[styles.button, disabled && styles.disabledButton]}
      disabled={disabled}
      onPress={() => applyMutation.mutate()}
    >
      <Text style={styles.buttonText}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    backgroundColor: "#155BC7",
    paddingVertical: 16,
    borderRadius: 14,
    alignItems: "center",
    marginTop: 8,
  },
  disabledButton: {
    backgroundColor: "#94A3B8",
  },
  buttonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "700",
  },
});
