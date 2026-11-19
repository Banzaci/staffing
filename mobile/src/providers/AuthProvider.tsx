
import { api, getToken, removeToken, setToken } from "@/libs/api";
import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";


type LoginInput = {
  email: string;
  password: string;
};

type TokenResponse = {
  access_token: string;
};

type AuthContextType = {
  isAuthenticated: boolean;
  isReady: boolean;
  login: (input: LoginInput) => Promise<void>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    async function restoreSession() {
      try {
        const token = await getToken();
        setIsAuthenticated(Boolean(token));
      } finally {
        setIsReady(true);
      }
    }

    restoreSession();
  }, []);

  async function login(input: LoginInput) {
    const data = await api<TokenResponse>(
      "/api/public/v1/auth/login",
      {
        method: "POST",
        body: JSON.stringify(input),
      }
    );

    await setToken(data.access_token);
    setIsAuthenticated(true);
  }

  async function logout() {
    await removeToken();
    setIsAuthenticated(false);
  }

  return (
    <AuthContext.Provider
      value={{ isAuthenticated, isReady, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
}
