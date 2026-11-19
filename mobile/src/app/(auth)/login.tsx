
import { useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { useMutation } from "@tanstack/react-query";
import { router } from "expo-router";
import { LockKeyhole, Mail } from "lucide-react-native";
import { useApp } from "@/providers/AppProvider";
import { useAuth } from "@/providers/AuthProvider";

export default function LoginScreen() {
  const { login } = useAuth();
  const { role } = useApp();

  const [email, setEmail] = useState("test1@worker.com");
  const [password, setPassword] = useState("Test1234");

  const loginMutation = useMutation({
    mutationFn: login,
    onSuccess: () => {
      if (role === "worker") {
        router.replace("/(protected)/(worker)");
      } else if (role === "employer") {
        router.replace("/(protected)/(employer)");
      }
    },
  });

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome back!</Text>
      <Text style={styles.subtitle}>Sign in to continue</Text>
      <View style={styles.inputContainer}>
        <Mail size={22} color="#64748B" />
        <TextInput
          placeholder="Email"
          autoCapitalize="none"
          keyboardType="email-address"
          value={email}
          onChangeText={setEmail}
          style={styles.input}
        />
      </View>

      <View style={styles.inputContainer}>
        <LockKeyhole size={22} color="#64748B" />
        <TextInput
          placeholder="Password"
          secureTextEntry
          value={password}
          onChangeText={setPassword}
          style={styles.input}
        />
      </View>

      {loginMutation.isError && (
        <Text style={styles.error}>
          Invalid email or password
        </Text>
      )}

      <Pressable
        style={styles.button}
        disabled={loginMutation.isPending}
        onPress={() => loginMutation.mutate({ email, password })}
      >
        {loginMutation.isPending ? (
          <ActivityIndicator color="#FFFFFF" />
        ) : (
          <Text style={styles.buttonText}>Sign In</Text>
        )}
      </Pressable>

      <Pressable onPress={() => router.push("/register")}>
        <Text style={styles.register}>
          Don't have an account? Register
        </Text>
      </Pressable>
    </View>
  );
}
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFFFFF",
    justifyContent: "center",
    padding: 25,
  },
  title: {
    fontSize: 32,
    fontWeight: "800",
    color: "#155BC7",
    textAlign: "center",
  },
  subtitle: {
    fontSize: 17,
    color: "#64748B",
    textAlign: "center",
    marginTop: 8,
    marginBottom: 40,
  },
  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#CBD5E1",
    borderRadius: 15,
    paddingHorizontal: 15,
    marginBottom: 15,
  },
  input: {
    flex: 1,
    padding: 17,
    fontSize: 16,
  },
  button: {
    backgroundColor: "#155BC7",
    borderRadius: 15,
    padding: 18,
    alignItems: "center",
    marginTop: 15,
  },
  buttonText: {
    color: "#FFFFFF",
    fontSize: 18,
    fontWeight: "700",
  },
  error: {
    color: "#DC2626",
    textAlign: "center",
    marginTop: 10,
  },
  register: {
    textAlign: "center",
    marginTop: 25,
    color: "#155BC7",
    fontWeight: "600",
  },
});
