import { api } from "@/libs/api";

type WorkerLocation = {
  latitude: number;
  longitude: number;
};

export function updateWorkerLocation(location: WorkerLocation) {
  return api<WorkerLocation>("/api/private/v1/workers/location", {
    method: "PATCH",
    body: JSON.stringify(location),
  });
}