import api from "@/lib/axios";

export interface RegisterData {
  email: string;
  password: string;
  first_name: string;
  last_name?: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface User {
  public_id: string;
  first_name: string;
  last_name: string | null;
  email: string;
  is_admin: boolean;
}

export const auth = {
  async register(data: RegisterData): Promise<void>{
    const response = await api.post("/auth/register", data);
    return response.data;
  },

  async login(data: LoginData): Promise<{ access_token: string; refresh_token: string; customer: User }> {
    const response = await api.post("/auth/login", data);
    return response.data;
  },

  async logout(): Promise<void> {
    await api.post("/auth/logout");
  },

  async getMe(): Promise<User> {
    const response = await api.get("/auth/me");
    return response.data;
  },
};