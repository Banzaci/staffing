
import {
  BriefcaseBusiness,
  ChefHat,
  Coffee,
  CookingPot,
  ConciergeBell,
  Hammer,
  Martini,
  ShieldCheck,
  SprayCan,
  UtensilsCrossed,
  Wrench,
  type LucideIcon,
} from "lucide-react-native";

// Lägg till faktiska skill.code från databasen här.
const skillIcons: Record<string, LucideIcon> = {
  waiter: UtensilsCrossed,
  waitress: UtensilsCrossed,
  chef: ChefHat,
  cook: CookingPot,
  bartender: Martini,
  barista: Coffee,
  receptionist: ConciergeBell,
  cleaner: SprayCan,
  maintenance: Wrench,
  handyman: Hammer,
  security: ShieldCheck,
};

type Props = {
  code: string;
  size?: number;
  color?: string;
};

export default function SkillIcon({
  code,
  size = 36,
  color = "#155BC7",
}: Props) {
  const Icon = skillIcons[code] ?? BriefcaseBusiness;

  return <Icon size={size} color={color} strokeWidth={1.8} />;
}
