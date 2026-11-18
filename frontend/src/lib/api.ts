export class ApiError extends Error {
  status: number;
  detail?: {
    message?: string;
    url?: string;
  };

  constructor(
    message: string,
    status: number,
    detail?: {
      message?: string;
      url?: string;
    }
  ) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8010";

let refreshPromise: Promise<string> | null = null;

async function refreshAccessToken(): Promise<string> {
  if (!refreshPromise) {
    refreshPromise = (async () => {
      const res = await fetch(`${API_URL}/auth/admin/refresh`, {
        method: "POST",
        credentials: "include",
      });

      if (!res.ok) {
        throw new Error("Session expired");
      }

      const data = await res.json();
      localStorage.setItem("token", data.access_token);

      return data.access_token as string;
    })().finally(() => {
      refreshPromise = null;
    });
  }

  return refreshPromise;
}

export async function api<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const isFormData = options.body instanceof FormData;

  const request = (token: string | null) =>
    fetch(`${API_URL}${endpoint}`, {
      ...options,
      credentials: "include",
      headers: {
        ...(isFormData ? {} : { "Content-Type": "application/json" }),
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...options.headers,
      },
    });

  let res = await request(getToken());

  if (res.status === 401 && endpoint !== "/admin/refresh") {
    try {
      const newToken = await refreshAccessToken();
      res = await request(newToken);
    } catch {
      // Refresh failed — session has expired.
    }
  }

  if (res.status === 401) {
    localStorage.removeItem("token");

    if (
      window.location.pathname !== "/login" &&
      window.location.pathname !== "/admin/login"
    ) {
      window.location.replace("/login");
    }

    throw new ApiError("Session expired", 401);
  }

  if (!res.ok) {
    const data = await res.json().catch(() => null);

    throw new ApiError(
      data?.detail?.message || data?.detail || "Request failed",
      res.status,
      data?.detail
    );
  }

  return res.json();
}

export function getToken() {
  return typeof window !== "undefined" ? localStorage.getItem("token") : null;
}

export function setToken(token: string) {
  localStorage.setItem("token", token);
}

export function removeToken() {
  localStorage.removeItem("token");
}