
import { deleteWorkerSkill, getSkills, saveWorkerSkill } from "@/app/services/skills";
import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

export function useWorkerSkills() {
  const queryClient = useQueryClient();

  const skillsQuery = useQuery({
    queryKey: ["skills"],
    queryFn: getSkills,
    staleTime: Infinity,
    gcTime: Infinity,
  });

  const saveSkill = useMutation({
    mutationFn: saveWorkerSkill,
    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey: ["session"],
      });
    },
  });

  const removeSkill = useMutation({
    mutationFn: deleteWorkerSkill,
    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey: ["session"],
      });
    },
  });

  return {
    skills: skillsQuery.data ?? [],
    isPending: skillsQuery.isPending,
    isError: skillsQuery.isError,
    saveSkill,
    removeSkill,
  };
}
