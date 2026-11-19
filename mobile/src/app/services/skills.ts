
import { api } from "@/libs/api";

export type Skill = {
  id: string;
  code: string;
  translations: Record<string, string>;
};

export type WorkerSkillInput = {
  skillId: string;
  yearsExperience: number;
};

export function getSkills() {
  return api<Skill[]>("/api/private/v1/skills");
}

export function saveWorkerSkill({
  skillId,
  yearsExperience,
}: WorkerSkillInput) {
  return api(`/api/private/v1/skills/${skillId}/me`, {
    method: "PUT",
    body: JSON.stringify({
      years_experience: yearsExperience,
    }),
  });
}

export function deleteWorkerSkill(skillId: string) {
  return api(`/api/private/v1/skills/${skillId}/me`, {
    method: "DELETE",
  });
}
