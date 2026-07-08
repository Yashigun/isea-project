"use client";

import { useEffect, useState } from "react";
import { securityService, RequestLog } from "@/services/security";
import DataTable from "@/components/admin/DataTable";

export default function RequestLogsTab() {
  const [logs, setLogs] = useState<RequestLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({ method: "", status_code: "", ip: "" });

  const fetchData = async () => {
    setLoading(true);
    try {
      const data = await securityService.getRequestLogs({
        method: filters.method || undefined,
        status_code: filters.status_code ? parseInt(filters.status_code) : undefined,
        ip: filters.ip || undefined,
        limit: 100,
      });
      setLogs(data.items);
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
      <div className="flex flex-col sm:flex-row sm:flex-wrap gap-3 mb-4">
        <input
          placeholder="Method (GET, POST, ...)"
          value={filters.method}
          onChange={(e) => setFilters({ ...filters, method: e.target.value })}
          className="w-full sm:w-auto border rounded px-3 py-2"
        />
        <input
          placeholder="Status Code"
          value={filters.status_code}
          onChange={(e) => setFilters({ ...filters, status_code: e.target.value })}
          className="w-full sm:w-auto border rounded px-3 py-2"
        />
        <input
          placeholder="IP Address"
          value={filters.ip}
          onChange={(e) => setFilters({ ...filters, ip: e.target.value })}
          className="w-full sm:w-auto border rounded px-3 py-2"
        />
        <button onClick={fetchData} className="w-full sm:w-auto bg-black text-white px-4 py-2 rounded">
          Filter
        </button>
      </div>

      {loading ? (
        <div>Loading...</div>
      ) : (
        <DataTable
          columns={[
            { key: "method", label: "Method" },
            { key: "route", label: "Route" },
            { key: "status_code", label: "Status" },
            { key: "ip_address", label: "IP" },
            { key: "response_time_ms", label: "Response (ms)" },
            { key: "created_at", label: "Time", render: (v) => typeof v === "string" ? new Date(v).toLocaleString() : "" },
          ]}
          data={logs}
        />
      )}
    </div>
  );
}
