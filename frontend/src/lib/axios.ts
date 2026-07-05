import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor – add token only on client side
api.interceptors.request.use((config) => {
  // Only access localStorage on the client
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  console.log(`🚀 ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
  return config;
});

// Response interceptor – handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (!error.response) {
      console.error("🌐 Network Error:", error.message);
      console.error("🔗 Full URL:", error.config?.baseURL + error.config?.url);
    } else if (error.response.status === 401) {
      // Only clear token on client
      if (typeof window !== "undefined") {
        localStorage.removeItem("access_token");
      }
    } else {
      console.error("❌ API Error:", error.response.status, error.response.data);
    }
    return Promise.reject(error);
  }
);

export default api;