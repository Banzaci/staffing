import { Stack, Redirect } from "expo-router";
import { ActivityIndicator, View } from "react-native";
import { useQuery } from "@tanstack/react-query";
import { useAuth } from "@/providers/AuthProvider";
import { useSession } from "@/hooks/useSession";
import { api } from "@/libs/api";

type Session = {
  user: {
    role: "worker" | "employer";
  };
};

export default function ProtectedLayout() {
  const { isAuthenticated, isReady } = useAuth();
  const { data: session, isPending, isError } = useSession();

  if (!isReady) return null;

  if (!isAuthenticated) {
    return <Redirect href="/login" />;
  }

  if (isPending) {
    return (
      <View style={{ flex: 1, justifyContent: "center" }}>
        <ActivityIndicator />
      </View>
    );
  }

  if (isError || !session) {
    return <Redirect href="/login" />;
  }

  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Protected guard={session.user.role === "worker"}>
        <Stack.Screen name="(worker)" />
      </Stack.Protected>
      <Stack.Protected guard={session.user.role === "employer"}>
        <Stack.Screen name="(employer)" />
      </Stack.Protected>
    </Stack>
  );
}