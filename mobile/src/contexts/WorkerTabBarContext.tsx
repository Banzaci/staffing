
import {
  createContext,
  useContext,
  useState,
  type ReactNode,
} from "react";

type WorkerTabBarContextValue = {
  minimized: boolean;
  setMinimized: (value: boolean) => void;
};

const WorkerTabBarContext =
  createContext<WorkerTabBarContextValue | null>(null);

export function WorkerTabBarProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [minimized, setMinimized] = useState(false);

  return (
    <WorkerTabBarContext.Provider
      value={{ minimized, setMinimized }}
    >
      {children}
    </WorkerTabBarContext.Provider>
  );
}

export function useWorkerTabBar() {
  const context = useContext(WorkerTabBarContext);

  if (!context) {
    throw new Error("WorkerTabBarProvider is missing");
  }

  return context;
}
