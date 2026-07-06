import api from "@/lib/axios";

export interface CustomerSession {
  public_id: string;
  customer_id: string;

  device_name: string | null;
  browser: string | null;
  operating_system: string | null;

  ip_address: string;
  user_agent: string;

  country: string | null;
  city: string | null;

  login_at: string;
  last_activity: string;
  expires_at: string;
  revoked_at: string | null;

  created_at: string;
  updated_at: string;
}

export interface CustomerSessionListResponse {
  items: CustomerSession[];
  total: number;
  limit: number;
  offset: number;
}

export interface SecurityEvent {
  public_id: string;
  event_type: string;
  severity: "low" | "medium" | "high" | "critical";
  title: string;
  description: string;
  ip_address: string;
  country: string | null;
  city: string | null;
  resolved: boolean;
  created_at: string;
  evidence: any;
}

export interface RequestLog {
  public_id: string;
  method: string;
  route: string;
  path: string;
  status_code: number;
  response_time_ms: number;
  ip_address: string;
  user_agent: string;
  created_at: string;
  customer_id: string | null;
  query_string: string | null;
}

export interface LoginAttempt {
  public_id: string;
  email: string;
  ip_address: string;
  user_agent: string;
  successful: boolean;
  failure_reason: string | null;
  attempt_type: string;
  created_at: string;
  customer_id: string | null;
}

export interface AuditLog {
  public_id: string;
  action: string;
  entity_type: string;
  entity_name: string | null;
  entity_public_id: string | null;
  old_data: any;
  new_data: any;
  ip_address: string;
  user_agent: string;
  created_at: string;
  customer_id: string | null;
}

export interface BlockedIP {
  public_id: string;
  ip_address: string;
  reason: string;
  blocked_by: string;
  block_note: string | null;
  blocked_until: string | null;
  permanently_blocked: boolean;
  is_active: boolean;
  created_at: string;
}

export interface DashboardStats {
  total_requests: number;
  total_security_events: number;
  critical_events: number;
  high_events: number;
  active_blocked_ips: number;
  failed_logins_last_24h: number;
}

export const securityService = {
  // ---------------------------------------------------------
  // Dashboard
  // ---------------------------------------------------------

  async getDashboardStats(): Promise<DashboardStats> {
    const response = await api.get(
      "/admin/security/dashboard/stats"
    );

    return response.data;
  },

  // ---------------------------------------------------------
  // Security Events
  // ---------------------------------------------------------

  async listEvents(params?: {
    severity?: string;
    resolved?: boolean;
    limit?: number;
  }): Promise<SecurityEvent[]> {
    const response = await api.get(
      "/admin/security/events",
      {
        params,
      }
    );

    return response.data;
  },

  async resolveEvent(
    publicId: string
  ): Promise<void> {
    await api.post(
      `/admin/security/events/${publicId}/resolve`
    );
  },

  // ---------------------------------------------------------
  // Customer Sessions
  // ---------------------------------------------------------

  async getCustomerSessions(
    params: {
      limit?: number;
      offset?: number;
    } = {}
  ): Promise<CustomerSessionListResponse> {
    const response = await api.get(
      "/admin/security/sessions",
      {
        params,
      }
    );

    return response.data;
  },

  async revokeCustomerSession(
    publicId: string
  ): Promise<CustomerSession> {
    const response = await api.post(
      `/admin/security/sessions/${publicId}/revoke`
    );

    return response.data;
  },

  // ---------------------------------------------------------
  // Request Logs
  // ---------------------------------------------------------

  async getRequestLogs(
    params: {
      method?: string;
      status_code?: number;
      ip?: string;
      start_date?: string;
      end_date?: string;
      limit?: number;
      offset?: number;
    } = {}
  ): Promise<{
    items: RequestLog[];
    total: number;
  }> {
    const response = await api.get(
      "/admin/security/requests",
      {
        params,
      }
    );

    return response.data;
  },

  // ---------------------------------------------------------
  // Login Attempts
  // ---------------------------------------------------------

  async getLoginAttempts(
    params: {
      email?: string;
      ip?: string;
      successful?: boolean;
      start_date?: string;
      end_date?: string;
      limit?: number;
      offset?: number;
    } = {}
  ): Promise<{
    items: LoginAttempt[];
    total: number;
  }> {
    const response = await api.get(
      "/admin/security/login-attempts",
      {
        params,
      }
    );

    return response.data;
  },

  // ---------------------------------------------------------
  // Audit Logs
  // ---------------------------------------------------------

  async getAuditLogs(
    params: {
      action?: string;
      entity_type?: string;
      customer_id?: string;
      start_date?: string;
      end_date?: string;
      limit?: number;
      offset?: number;
    } = {}
  ): Promise<{
    items: AuditLog[];
    total: number;
  }> {
    const response = await api.get(
      "/admin/security/audit-logs",
      {
        params,
      }
    );

    return response.data;
  },

  // ---------------------------------------------------------
  // Blocked IPs
  // ---------------------------------------------------------

  async getBlockedIPs(
    params: {
      active_only?: boolean;
      limit?: number;
      offset?: number;
    } = {}
  ): Promise<{
    items: BlockedIP[];
    total: number;
  }> {
    const response = await api.get(
      "/admin/security/blocked-ips",
      {
        params,
      }
    );

    return response.data;
  },

  async blockIp(data: {
    ip_address: string;
    reason: string;
    note?: string;
    expires_in_minutes?: number;
    permanently?: boolean;
  }): Promise<{
    public_id: string;
  }> {
    const response = await api.post(
      "/admin/security/blocked-ips",
      data
    );

    return response.data;
  },

  async unblockIp(
    publicId: string
  ): Promise<void> {
    await api.delete(
      `/admin/security/blocked-ips/${publicId}`
    );
  },

  // ---------------------------------------------------------
  // Statistics
  // ---------------------------------------------------------

  async getTopIPsByRequests(
    since?: string
  ): Promise<
    {
      ip: string;
      count: number;
    }[]
  > {
    const response = await api.get(
      "/admin/security/stats/requests-by-ip",
      {
        params: {
          since,
        },
      }
    );

    return response.data;
  },

  async getTopIPsByFailedLogins(
    since?: string
  ): Promise<
    {
      ip: string;
      count: number;
    }[]
  > {
    const response = await api.get(
      "/admin/security/stats/failed-logins-by-ip",
      {
        params: {
          since,
        },
      }
    );

    return response.data;
  },
};