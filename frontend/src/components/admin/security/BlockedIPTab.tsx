"use client";

import { useEffect, useState } from "react";
import { securityService, BlockedIP } from "@/services/security";
import DataTable from "@/components/admin/DataTable";

export default function BlockedIPTab() {
  const [ips, setIps] = useState<BlockedIP[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeOnly, setActiveOnly] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const data = await securityService.getBlockedIPs({ active_only: activeOnly, limit: 100 });
      setIps(data.items);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [activeOnly]);

  const handleUnblock = async (publicId: string) => {
    if (!confirm("Unblock this IP?")) return;
    await securityService.unblockIp(publicId);
    fetchData();
  };

  return (
    <div>
      <div className="flex items-center gap-4 mb-4">
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={activeOnly}
            onChange={(e) => setActiveOnly(e.target.checked)}
          />
          Active only
        </label>
        <button onClick={fetchData} className="bg-black text-white px-4 py-2 rounded">
          Refresh
        </button>
      </div>

      {loading ? (
        <div>Loading...</div>
      ) : (
        <DataTable
          columns={[
            { key: "ip_address", label: "IP" },
            { key: "reason", label: "Reason" },
            { key: "blocked_by", label: "Blocked By" },
            { key: "permanently_blocked", label: "Permanent", render: (v) => (v ? "✅" : "❌") },
            { key: "is_active", label: "Active", render: (v) => (v ? "✅" : "❌") },
            { key: "blocked_until", label: "Expires", render: (v) => typeof v === "string" && v ? new Date(v).toLocaleString() : "Never" },
            { key: "created_at", label: "Created", render: (v) => typeof v === "string" ? new Date(v).toLocaleString() : "" },
          ]}
          data={ips}
          onDelete={(row) => row.is_active ? handleUnblock(row.public_id) : undefined}
          deleteLabel="Unblock"
        />
      )}
    </div>
  );
}