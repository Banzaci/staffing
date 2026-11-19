
import { useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  StyleSheet,
  Text,
  TextInput,
  View,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { useMutation } from "@tanstack/react-query";
import { useApp } from "@/providers/AppProvider";
import { router } from "expo-router";
import {
  UserRound,
  Mail,
  LockKeyhole,
} from "lucide-react-native";

import { api } from "@/libs/api";

type RegisterInput = {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  preferred_language: string;
  role: "worker" | "employer";
};

export default function RegisterScreen() {
  const { role } = useApp();
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const registerMutation = useMutation({
    mutationFn: (input: RegisterInput) =>
      api("/api/public/v1/auth/register", {
        method: "POST",
        body: JSON.stringify(input),
      }),
    onSuccess: () => {
      router.replace("/login");
    },
  });

  const canSubmit =
    firstName.trim().length > 0 &&
    lastName.trim().length > 0 &&
    email.trim().length > 0 &&
    password.length >= 8;

  function handleRegister() {
    if (!canSubmit || !role || registerMutation.isPending) return;

    registerMutation.mutate({
      first_name: firstName.trim(),
      last_name: lastName.trim(),
      email: email.trim().toLowerCase(),
      password,
      preferred_language: "en",
      role,
    });
  }

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <ScrollView
        contentContainerStyle={styles.content}
        keyboardShouldPersistTaps="handled"
      >
        <Text style={styles.title}>Create Account</Text>
        <Text style={styles.subtitle}>
          Register to get started
        </Text>

        <View style={styles.inputContainer}>
          <UserRound size={22} color="#64748B" />
          <TextInput
            placeholder="First name"
            autoCapitalize="words"
            value={firstName}
            onChangeText={setFirstName}
            style={styles.input}
          />
        </View>

        <View style={styles.inputContainer}>
          <UserRound size={22} color="#64748B" />
          <TextInput
            placeholder="Last name"
            autoCapitalize="words"
            value={lastName}
            onChangeText={setLastName}
            style={styles.input}
          />
        </View>

        <View style={styles.inputContainer}>
          <Mail size={22} color="#64748B" />
          <TextInput
            placeholder="Email"
            autoCapitalize="none"
            autoCorrect={false}
            keyboardType="email-address"
            value={email}
            onChangeText={setEmail}
            style={styles.input}
          />
        </View>

        <View style={styles.inputContainer}>
          <LockKeyhole size={22} color="#64748B" />
          <TextInput
            placeholder="Password (minimum 8 characters)"
            secureTextEntry
            value={password}
            onChangeText={setPassword}
            style={styles.input}
          />
        </View>

        {registerMutation.isError && (
          <Text style={styles.error}>
            {registerMutation.error instanceof Error
              ? registerMutation.error.message
              : "Registration failed"}
          </Text>
        )}

        <Pressable
          style={[
            styles.button,
            (!canSubmit || registerMutation.isPending) &&
              styles.buttonDisabled,
          ]}
          disabled={!canSubmit || registerMutation.isPending}
          onPress={handleRegister}
        >
          {registerMutation.isPending ? (
            <ActivityIndicator color="#FFFFFF" />
          ) : (
            <Text style={styles.buttonText}>
              Create Account
            </Text>
          )}
        </Pressable>

        <Pressable onPress={() => router.replace("/login")}>
          <Text style={styles.login}>
            Already have an account? Sign In
          </Text>
        </Pressable>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFFFFF",
  },
  content: {
    flexGrow: 1,
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
    marginBottom: 35,
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
    color: "#0F172A",
  },
  button: {
    backgroundColor: "#155BC7",
    borderRadius: 15,
    padding: 18,
    alignItems: "center",
    marginTop: 15,
  },
  buttonDisabled: {
    opacity: 0.5,
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
  login: {
    textAlign: "center",
    marginTop: 25,
    color: "#155BC7",
    fontWeight: "600",
  },
});