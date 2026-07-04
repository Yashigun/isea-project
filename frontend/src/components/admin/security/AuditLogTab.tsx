"use client";

import { useEffect, useState } from "react";
import { securityService, AuditLog } from "@/services/security";
import DataTable from "@/components/admin/DataTable";

export default function AuditLogsTab() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({ action: "", entity_type: "" });

  const fetchData = async () => {
    setLoading(true);
    try {
      const data = await securityService.getAuditLogs({
        action: filters.action || undefined,
        entity_type: filters.entity_type || undefined,
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
      <div className="flex flex-wrap gap-3 mb-4">
        <input
          placeholder="Action (create, update, delete, ...)"
          value={filters.action}
          onChange={(e) => setFilters({ ...filters, action: e.target.value })}
          className="border rounded px-3 py-2"
        />
        <input
          placeholder="Entity Type (product, category, order, ...)"
          value={filters.entity_type}
          onChange={(e) => setFilters({ ...filters, entity_type: e.target.value })}
          className="border rounded px-3 py-2"
        />
        <button onClick={fetchData} className="bg-black text-white px-4 py-2 rounded">
          Filter
        </button>
      </div>

      {loading ? (
        <div>Loading...</div>
      ) : (
        <DataTable
          columns={[
            { key: "action", label: "Action" },
            { key: "entity_type", label: "Entity" },
            { key: "entity_name", label: "Entity Name" },
            { key: "ip_address", label: "IP" },
            { key: "created_at", label: "Time", render: (v) => new Date(v).toLocaleString() },
          ]}
          data={logs}
        />
      )}
    </div>
  );
}