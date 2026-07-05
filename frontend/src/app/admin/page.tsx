"use client";

import { useEffect, useState } from "react";
import type { ReactNode } from "react";
import { Package, FolderTree, ShoppingCart, IndianRupee, Users, Activity } from "lucide-react";
import { securityService, DashboardStats, RequestLog, LoginAttempt } from "@/services/security";
import { productService } from "@/services/product";
import { categoryService } from "@/services/category";
import { orderService, Order } from "@/services/order";

export default function AdminDashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [productCount, setProductCount] = useState(0);
  const [categoryCount, setCategoryCount] = useState(0);
  const [orders, setOrders] = useState<Order[]>([]);
  const [requestLogs, setRequestLogs] = useState<RequestLog[]>([]);
  const [loginAttempts, setLoginAttempts] = useState<LoginAttempt[]>([]);
  const [loading, setLoading] = useState(true);

  const loadDashboard = async () => {
    const [
      statsData,
      products,
      categories,
      orderData,
      requests,
      attempts,
    ] = await Promise.all([
      securityService.getDashboardStats(),
      productService.getAll(),
      categoryService.getAll(false),
      orderService.listAll(),
      securityService.getRequestLogs({ limit: 100 }),
      securityService.getLoginAttempts({ limit: 100 }),
    ]);

    setStats(statsData);
    setProductCount(products.length);
    setCategoryCount(categories.length);
    setOrders(orderData);
    setRequestLogs(requests.items);
    setLoginAttempts(attempts.items);
  };

  useEffect(() => {
    void Promise.resolve().then(loadDashboard)
      .catch(console.error)
      .finally(() => setLoading(false));

    const timer = window.setInterval(() => {
      loadDashboard().catch(console.error);
    }, 30000);

    return () => window.clearInterval(timer);
  }, []);

  if (loading) return <div>Loading stats...</div>;

  const revenue = orders.reduce((sum, order) => sum + Number(order.total_amount || 0), 0);
  const delivered = orders.filter((order) => order.status === "delivered").length;
  const pending = orders.filter((order) => order.status === "pending").length;
  const trafficSeries = groupByMinute(requestLogs);
  const authSeries = groupSuccessfulLogins(loginAttempts);
  const authenticatedUsers = new Set(
    loginAttempts
      .filter((attempt) => attempt.successful)
      .map((attempt) => attempt.email)
  ).size;

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <StatCard icon={<Package size={22} />} label="Products" value={productCount} />
        <StatCard icon={<FolderTree size={22} />} label="Categories" value={categoryCount} />
        <StatCard icon={<ShoppingCart size={22} />} label="Orders" value={orders.length} />
        <StatCard icon={<IndianRupee size={22} />} label="Revenue" value={`₹${revenue.toFixed(2)}`} />
        <StatCard icon={<Activity size={22} />} label="Requests" value={stats?.total_requests ?? 0} />
        <StatCard icon={<Users size={22} />} label="Authenticated Users" value={authenticatedUsers} />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <OverviewCard
          title="Order Overview"
          rows={[
            ["Pending", pending],
            ["Delivered", delivered],
            ["Other", Math.max(orders.length - pending - delivered, 0)],
          ]}
        />
        <OverviewCard
          title="Revenue Overview"
          rows={[
            ["Subtotal", revenue],
            ["Average Order", orders.length ? revenue / orders.length : 0],
            ["Orders", orders.length],
          ]}
          currency
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <BarChart title="Live Traffic" subtitle="Requests by minute" data={trafficSeries} />
        <BarChart title="Authenticated Users" subtitle="Successful logins by minute" data={authSeries} />
      </div>
    </div>
  );
}

function StatCard({
  icon,
  label,
  value,
}: {
  icon: ReactNode;
  label: string;
  value: number | string;
}) {
  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-full bg-gray-100">
        {icon}
      </div>
      <p className="text-sm text-gray-500">{label}</p>
      <p className="text-3xl font-bold">{value}</p>
    </div>
  );
}

function OverviewCard({
  title,
  rows,
  currency = false,
}: {
  title: string;
  rows: Array<[string, number]>;
  currency?: boolean;
}) {
  return (
    <div className="rounded-lg bg-white p-6 shadow">
      <h2 className="text-xl font-semibold">{title}</h2>
      <div className="mt-5 space-y-3">
        {rows.map(([label, value]) => (
          <div key={label} className="flex justify-between border-b pb-2 text-sm">
            <span className="text-gray-500">{label}</span>
            <span className="font-medium">
              {currency && label !== "Orders" ? `₹${value.toFixed(2)}` : value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

function BarChart({
  title,
  subtitle,
  data,
}: {
  title: string;
  subtitle: string;
  data: Array<{ label: string; value: number }>;
}) {
  const max = Math.max(...data.map((item) => item.value), 1);

  return (
    <div className="rounded-lg bg-white p-6 shadow">
      <div className="mb-6">
        <h2 className="text-xl font-semibold">{title}</h2>
        <p className="text-sm text-gray-500">{subtitle}</p>
      </div>
      <div className="flex h-56 items-end gap-2">
        {data.map((item) => (
          <div key={item.label} className="flex flex-1 flex-col items-center gap-2">
            <div className="flex h-44 w-full items-end rounded bg-gray-100">
              <div
                className="w-full rounded bg-black transition-all"
                style={{ height: `${Math.max((item.value / max) * 100, item.value ? 8 : 0)}%` }}
                title={`${item.label}: ${item.value}`}
              />
            </div>
            <span className="text-[10px] text-gray-500">{item.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function groupByMinute(items: RequestLog[]) {
  const counts = new Map<string, number>();
  items.forEach((item) => {
    const date = new Date(item.created_at);
    const label = `${date.getHours()}:${date.getMinutes().toString().padStart(2, "0")}`;
    counts.set(label, (counts.get(label) ?? 0) + 1);
  });
  return Array.from(counts.entries()).slice(-12).map(([label, value]) => ({ label, value }));
}

function groupSuccessfulLogins(items: LoginAttempt[]) {
  const counts = new Map<string, number>();
  items.filter((item) => item.successful).forEach((item) => {
    const date = new Date(item.created_at);
    const label = `${date.getHours()}:${date.getMinutes().toString().padStart(2, "0")}`;
    counts.set(label, (counts.get(label) ?? 0) + 1);
  });
  return Array.from(counts.entries()).slice(-12).map(([label, value]) => ({ label, value }));
}
