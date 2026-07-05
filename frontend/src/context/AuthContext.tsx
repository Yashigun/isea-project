"use client";

import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import { auth, User, RegisterData } from "@/services/auth";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const checkAuth = async () => {
    try {
      const userData = await auth.getMe();
      setUser(userData);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkAuth();
  }, []);

  const redirectAfterAuth = (customer: User) => {
    const returnUrl = sessionStorage.getItem("returnUrl");
    sessionStorage.removeItem("returnUrl");

    if (returnUrl) {
      router.push(returnUrl);
      return;
    }

    if (customer.is_admin) {
      router.push("/admin");
    } else {
      router.push("/profile");
    }
  };

  const login = async (email: string, password: string) => {
    // Login response includes access_token, refresh_token, and customer
    const { customer, access_token } = await auth.login({
      email,
      password,
    });

    // Store the access token in localStorage for axios interceptor
    if (access_token) {
      localStorage.setItem("access_token", access_token);
    }

    setUser(customer);
    redirectAfterAuth(customer);
  };

  const register = async (data: RegisterData) => {
    // 1. Create the account
    await auth.register(data);

    // 2. Login using the same credentials
    const { customer, access_token } = await auth.login({
      email: data.email,
      password: data.password,
    });

    // Store the access token
    if (access_token) {
      localStorage.setItem("access_token", access_token);
    }

    setUser(customer);
    redirectAfterAuth(customer);
  };

  const logout = async () => {
    await auth.logout();
    localStorage.removeItem("access_token");
    setUser(null);
    router.push("/");
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        register,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};