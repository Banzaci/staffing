import { useQuery } from "@tanstack/react-query";
import { api } from "@/libs/api";
import { useAuth } from "@/providers/AuthProvider";

type Session = {
  user: {
    id: string;
    email: string;
    first_name: string;
    last_name: string;
    role: "worker" | "employer";
    preferred_language: string;
  };
  worker_profile: {
    id: string;
    avatar_url: string | null;
    bio: string | null;
    latitude: number | null;
    longitude: number | null;
    willing_to_travel: boolean;
  } | null;
  skills: {
    skill_id: string;
    years_experience: number | null;
    min_hourly_rate: number | null;
    max_hourly_rate: number | null;
  }[];
  preferences: string[];
};

export function useSession() {
  const { isAuthenticated, isReady } = useAuth();
  return useQuery({
    queryKey: ["session"],
    queryFn: () => api<Session>("/api/private/v1/session/me"),
    enabled: isReady && isAuthenticated,
    staleTime: Infinity,
    retry: false,
  });
}