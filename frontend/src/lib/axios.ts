import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";
import { getStoredAccessToken, getStoredRefreshToken, clearAuthTokens, saveAuthTokens } from "@/lib/authStorage";

const API_URL =
  typeof window === "undefined"
    ? process.env.NEXT_PUBLIC_API_URL  : "/api/v1";

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

let isRefreshing = false;
let failedQueue: Array<{
  resolve: (value?: unknown) => void;
  reject: (reason?: unknown) => void;
}> = [];

const processQueue = (error: unknown, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

const clearAuthAndReject = (error: unknown) => {
  if (typeof window !== "undefined") {
    clearAuthTokens();
  }
  return Promise.reject(error);
};

const attachAuthHeader = (config: InternalAxiosRequestConfig) => {
  if (typeof window === "undefined") return config;

  const token = getStoredAccessToken();
  if (!token) return config;

  if (typeof config.headers?.set === "function") {
    config.headers.set("Authorization", `Bearer ${token}`);
    config.headers.set("x-access-token", token);
  } else {
    const nextHeaders = new axios.AxiosHeaders({
      ...(config.headers ?? {}),
      Authorization: `Bearer ${token}`,
      "x-access-token": token,
    });
    config.headers = nextHeaders;
  }

  return config;
};

// Request interceptor – add token only on client side
api.interceptors.request.use((config) => attachAuthHeader(config));

// Response interceptor – handle errors
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    if (!error.response) {
      console.error("Network Error:", error.message);
      console.error("Full URL:", `${error.config?.baseURL ?? ""}${error.config?.url ?? ""}`);
      return Promise.reject(error);
    }

    if (
      error.response.status === 401 &&
      originalRequest &&
      !originalRequest._retry &&
      !originalRequest.url?.includes("/auth/refresh") &&
      !originalRequest.url?.includes("/auth/login")
    ) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then(() => api(originalRequest))
          .catch((err) => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      const refreshToken = getStoredRefreshToken();

      try {
        const refreshResponse = await api.post(
          "/auth/refresh",
          refreshToken ? { refresh_token: refreshToken } : {},
          { withCredentials: true }
        );
        const newAccessToken = refreshResponse.data?.access_token;

        if (newAccessToken) {
          saveAuthTokens({
            access_token: newAccessToken,
            ...(refreshToken ? { refresh_token: refreshToken } : {}),
          });
          attachAuthHeader(originalRequest);
          processQueue(null, newAccessToken);
          return api(originalRequest);
        }

        processQueue(error);
        return clearAuthAndReject(error);
      } catch (refreshError) {
        processQueue(refreshError);
        return clearAuthAndReject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    if (error.response.status === 401) {
      return clearAuthAndReject(error);
    } else {
      console.error("API Error:", error.response.status, error.response.data);
    }

    return Promise.reject(error);
  }
);

export default api;
