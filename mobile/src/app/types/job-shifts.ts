export type NearbyJob = {
  id: string;
  business_id: string;
  business_name: string;
  job_type: string;
  description: string | null;
  latitude: number;
  longitude: number;
  distance_km: number;
  starts_at: string;
  ends_at: string;
  hourly_rate: number;
  currency: string;
  workers_needed: number;
};