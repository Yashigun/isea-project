"use client";

import { useEffect, useState } from "react";
import { securityService, LoginAttempt } from "@/services/security";
import DataTable from "@/components/admin/DataTable";

export default function LoginAttemptsTab() {
  const [attempts, setAttempts] = useState<LoginAttempt[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({ email: "", ip: "", successful: "" });

  const fetchData = async () => {
    setLoading(true);
    try {
      const data = await securityService.getLoginAttempts({
        email: filters.email || undefined,
        ip: filters.ip || undefined,
        successful: filters.successful === "" ? undefined : filters.successful === "true",
        limit: 100,
      });
      setAttempts(data.items);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [filters]);

  return (
    <div>
      <div className="flex flex-wrap gap-3 mb-4">
        <input
          placeholder="Email"
          value={filters.email}
          onChange={(e) => setFilters({ ...filters, email: e.target.value })}
          className="border rounded px-3 py-2"
        />
        <input
          placeholder="IP Address"
          value={filters.ip}
          onChange={(e) => setFilters({ ...filters, ip: e.target.value })}
          className="border rounded px-3 py-2"
        />
        <select
          value={filters.successful}
          onChange={(e) => setFilters({ ...filters, successful: e.target.value })}
          className="border rounded px-3 py-2"
        >
          <option value="">All</option>
          <option value="true">Successful</option>
          <option value="false">Failed</option>
        </select>
        <button onClick={fetchData} className="bg-black text-white px-4 py-2 rounded">
          Filter
        </button>
      </div>

      {loading ? (
        <div>Loading...</div>
      ) : (
        <DataTable
          columns={[
            { key: "email", label: "Email" },
            { key: "attempt_type", label: "Type" },
            { key: "ip_address", label: "IP" },
            { key: "successful", label: "Success", render: (v) => (v ? "✅" : "❌") },
            { key: "failure_reason", label: "Failure Reason" },
            { key: "created_at", label: "Time", render: (v) => new Date(v).toLocaleString() },
          ]}
          data={attempts}
        />
      )}
    </div>
  );
}