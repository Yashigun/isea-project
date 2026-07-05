"use client";

import { useState } from "react";
import { useSearchParams } from "next/navigation";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import RequestLogsTab from "@/components/admin/security/RequestLogTab";
import LoginAttemptsTab from "@/components/admin/security/LoginAttemptTab";
import AuditLogsTab from "@/components/admin/security/AuditLogTab";
import BlockedIPTab from "@/components/admin/security/BlockedIPTab";
import StatsTab from "@/components/admin/security/StatsTab";

export default function AdminSecurityPage() {
  const searchParams = useSearchParams();
  const defaultTab = searchParams.get("tab") || "requests";
  const [activeTab, setActiveTab] = useState(defaultTab);

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Security</h1>
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList>
          <TabsTrigger value="requests">Request Logs</TabsTrigger>
          <TabsTrigger value="login-attempts">Login Attempts</TabsTrigger>
          <TabsTrigger value="audit-logs">Audit Logs</TabsTrigger>
          <TabsTrigger value="blocked-ips">Blocked IPs</TabsTrigger>
          <TabsTrigger value="stats">Stats</TabsTrigger>
        </TabsList>

        <TabsContent value="requests">
          <RequestLogsTab />
        </TabsContent>

        <TabsContent value="login-attempts">
          <LoginAttemptsTab />
        </TabsContent>

        <TabsContent value="audit-logs">
          <AuditLogsTab />
        </TabsContent>

        <TabsContent value="blocked-ips">
          <BlockedIPTab />
        </TabsContent>

        <TabsContent value="stats">
          <StatsTab />
        </TabsContent>
      </Tabs>
    </div>
  );
}
