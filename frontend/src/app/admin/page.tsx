"use client";

import { useEffect, useState } from "react";
import { securityService, DashboardStats } from "@/services/security";

export default function AdminDashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    securityService.getDashboardStats()
      .then(setStats)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading stats...</div>;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <StatCard label="Total Requests" value={stats?.total_requests ?? 0} />
        <StatCard label="Security Events" value={stats?.total_security_events ?? 0} />
        <StatCard label="Critical Events" value={stats?.critical_events ?? 0} />
        <StatCard label="High Events" value={stats?.high_events ?? 0} />
        <StatCard label="Blocked IPs" value={stats?.blocked_ips ?? 0} />
        <StatCard label="Failed Logins (24h)" value={stats?.failed_logins_last_24h ?? 0} />
      </div>
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <p className="text-sm text-gray-500">{label}</p>
      <p className="text-3xl font-bold">{value}</p>
    </div>
  );
}