
import AsyncStorage from "@react-native-async-storage/async-storage";
import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

type Role = "worker" | "employer";

type AppContextType = {
  role: Role | null;
  isReady: boolean;
  setRole: (role: Role) => Promise<void>;
};

const AppContext = createContext<AppContextType | null>(null);

export function AppProvider({ children }: { children: ReactNode }) {
  const [role, setRoleState] = useState<Role | null>(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const saved = await AsyncStorage.getItem("app_role");

        if (saved === "worker" || saved === "employer") {
          setRoleState(saved);
        }
      } finally {
        setIsReady(true);
      }
    }

    load();
  }, []);

  async function setRole(nextRole: Role) {
    await AsyncStorage.setItem("app_role", nextRole);
    setRoleState(nextRole);
  }

  return (
    <AppContext.Provider value={{ role, isReady, setRole }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);

  if (!context) {
    throw new Error("useApp must be used inside AppProvider");
  }

  return context;
}
