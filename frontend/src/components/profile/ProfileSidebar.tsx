
"use client";

import { User } from "@/services/auth";
import { LayoutDashboard, UserCircle, LogOut } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

interface ProfileSidebarProps {
  activeTab: "dashboard" | "account";
  onTabChange: (tab: "dashboard" | "account") => void;
  user: User;
}

export default function ProfileSidebar({
  activeTab,
  onTabChange,
  user,
}: ProfileSidebarProps) {
  const { logout } = useAuth();

  return (
    <div className="bg-white rounded-2xl shadow-lg p-4 sm:p-6 lg:sticky lg:top-24">
      {/* User Avatar & Name */}
      <div className="text-center pb-4 sm:pb-6 border-b border-gray-100">
        <div className="w-16 h-16 sm:w-20 sm:h-20 mx-auto rounded-full bg-gray-200 flex items-center justify-center text-xl sm:text-2xl font-semibold text-gray-600">
          {user.first_name?.[0]}{user.last_name?.[0]}
        </div>
        <h2 className="mt-3 text-base sm:text-lg font-semibold">
          {user.first_name} {user.last_name}
        </h2>
        <p className="text-sm text-gray-500 break-words">{user.email}</p>
      </div>

      {/* Navigation */}
      <nav className="mt-4 sm:mt-6 space-y-2">
        <button
          onClick={() => onTabChange("dashboard")}
          className={`w-full flex items-center gap-3 px-3 sm:px-4 py-3 rounded-lg transition-colors ${
            activeTab === "dashboard"
              ? "bg-black text-white"
              : "hover:bg-gray-100"
          }`}
        >
          <LayoutDashboard size={20} />
          <span>Dashboard</span>
        </button>

        <button
          onClick={() => onTabChange("account")}
          className={`w-full flex items-center gap-3 px-3 sm:px-4 py-3 rounded-lg transition-colors ${
            activeTab === "account"
              ? "bg-black text-white"
              : "hover:bg-gray-100"
          }`}
        >
          <UserCircle size={20} />
          <span>Account</span>
        </button>
      </nav>

      {/* Logout */}
      <div className="mt-6 sm:mt-8 pt-4 sm:pt-6 border-t border-gray-100">
        <button
          onClick={logout}
          className="w-full flex items-center gap-3 px-3 sm:px-4 py-3 rounded-lg text-red-600 hover:bg-red-50 transition-colors"
        >
          <LogOut size={20} />
          <span>Logout</span>
        </button>
      </div>
    </div>
  );
}