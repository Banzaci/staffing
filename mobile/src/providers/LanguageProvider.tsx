
import AsyncStorage from "@react-native-async-storage/async-storage";
import { getLocales } from "expo-localization";
import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

export type Language = "en" | "sv" | "fil" | "ceb" | "fr" | "de";

const supported: Language[] = ["en", "sv", "fil", "ceb", "fr", "de"];


const translations = {
  en: {
    welcome: "Welcome!",
    question: "What are you looking for?",
    worker: "Find a Job",
    employer: "Find Workers",
    dashboardGreeting: "Hello",
    dashboardSubtitle: "Get ready for your next job",
    addSkills: "Add your skills",
    addSkillsDescription: "Tell us what you can do to find suitable jobs",
  },
  sv: {
    welcome: "Välkommen!",
    question: "Vad söker du?",
    worker: "Sök jobb",
    employer: "Sök personal",
    dashboardGreeting: "Hej",
    dashboardSubtitle: "Gör dig redo för ditt nästa jobb",
    addSkills: "Lägg till dina kompetenser",
    addSkillsDescription: "Berätta vad du kan för att hitta passande jobb",
  },
  fil: {
    welcome: "Maligayang pagdating!",
    question: "Ano ang hinahanap mo?",
    worker: "Maghanap ng Trabaho",
    employer: "Maghanap ng Manggagawa",
    dashboardGreeting: "Kumusta",
    dashboardSubtitle: "Maghanda para sa iyong susunod na trabaho",
    addSkills: "Idagdag ang iyong mga kasanayan",
    addSkillsDescription: "Sabihin kung ano ang kaya mong gawin",
  },
  ceb: {
    welcome: "Maayong pag-abot!",
    question: "Unsa imong gipangita?",
    worker: "Pangita og Trabaho",
    employer: "Pangita og Trabahante",
    dashboardGreeting: "Kumusta",
    dashboardSubtitle: "Pag-andam sa imong sunod nga trabaho",
    addSkills: "Idugang ang imong mga kahanas",
    addSkillsDescription: "Isulti kung unsay imong mahimo",
  },
  fr: {
    welcome: "Bienvenue !",
    question: "Que recherchez-vous ?",
    worker: "Trouver un emploi",
    employer: "Trouver du personnel",
    dashboardGreeting: "Bonjour",
    dashboardSubtitle: "Préparez votre prochain emploi",
    addSkills: "Ajoutez vos compétences",
    addSkillsDescription: "Indiquez vos compétences pour trouver un emploi",
  },
  de: {
    welcome: "Willkommen!",
    question: "Was suchen Sie?",
    worker: "Job finden",
    employer: "Personal finden",
    dashboardGreeting: "Hallo",
    dashboardSubtitle: "Bereite dich auf deinen nächsten Job vor",
    addSkills: "Füge deine Fähigkeiten hinzu",
    addSkillsDescription: "Zeige, was du kannst, um passende Jobs zu finden",
  },
};

type LanguageContextType = {
  language: Language;
  setLanguage: (language: Language) => Promise<void>;
  t: typeof translations.en;
};

const LanguageContext = createContext<LanguageContextType | null>(null);

export function LanguageProvider({ children }: { children: ReactNode }) {
  const deviceLanguage = getLocales()[0]?.languageCode;

  const initialLanguage: Language = supported.includes(
    deviceLanguage as Language
  )
    ? (deviceLanguage as Language)
    : "en";

  const [language, setLanguageState] = useState<Language>(initialLanguage);

  useEffect(() => {
    AsyncStorage.getItem("app_language").then((saved) => {
      if (supported.includes(saved as Language)) {
        setLanguageState(saved as Language);
      }
    });
  }, []);

  async function setLanguage(next: Language) {
    await AsyncStorage.setItem("app_language", next);
    setLanguageState(next);
  }

  return (
    <LanguageContext.Provider
      value={{ language, setLanguage, t: translations[language] }}
    >
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);

  if (!context) {
    throw new Error("useLanguage must be used inside LanguageProvider");
  }

  return context;
}
