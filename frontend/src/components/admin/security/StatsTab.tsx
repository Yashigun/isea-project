"use client";

import { useEffect, useState } from "react";
import { securityService } from "@/services/security";

export default function StatsTab() {
  const [topIPs, setTopIPs] = useState<{ ip: string; count: number }[]>([]);
  const [topFailed, setTopFailed] = useState<{ ip: string; count: number }[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      securityService.getTopIPsByRequests(),
      securityService.getTopIPsByFailedLogins(),
    ]).then(([requests, failed]) => {
      setTopIPs(requests);
      setTopFailed(failed);
    }).catch(console.error).finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading stats...</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <h3 className="text-lg font-semibold mb-3">Top IPs by Requests (last 24h)</h3>
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="text-left px-4 py-2">IP</th>
                <th className="text-left px-4 py-2">Count</th>
              </tr>
            </thead>
            <tbody>
              {topIPs.map((item) => (
                <tr key={item.ip} className="border-b">
                  <td className="px-4 py-2">{item.ip}</td>
                  <td className="px-4 py-2">{item.count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <div>
        <h3 className="text-lg font-semibold mb-3">Top IPs by Failed Logins (last 24h)</h3>
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="text-left px-4 py-2">IP</th>
                <th className="text-left px-4 py-2">Count</th>
              </tr>
            </thead>
            <tbody>
              {topFailed.map((item) => (
                <tr key={item.ip} className="border-b">
                  <td className="px-4 py-2">{item.ip}</td>
                  <td className="px-4 py-2">{item.count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}