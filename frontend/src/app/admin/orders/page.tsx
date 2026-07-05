"use client";

import { useEffect, useState } from "react";
import { orderService, Order } from "@/services/order";

const statusOptions = [
  "pending",
  "confirmed",
  "processing",
  "shipped",
  "delivered",
  "cancelled",
  "refunded",
];

export default function AdminOrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState("");

  const fetchOrders = async () => {
    setLoading(true);

    try {
      const data = await orderService.listAll(
        filterStatus || undefined
      );

      setOrders(data);
    } catch (err) {
      console.error("Failed to load orders", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, [filterStatus]);

  const handleStatusChange = async (
    publicId: string,
    status: string
  ) => {
    try {
      await orderService.updateStatus(
        publicId,
        status
      );

      fetchOrders();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="p-8">
        Loading orders...
      </div>
    );
  }

  return (
    <div className="space-y-6">

      <div className="flex items-center justify-between">

        <h1 className="text-3xl font-bold">
          Orders
        </h1>

        <select
          value={filterStatus}
          onChange={(e) =>
            setFilterStatus(e.target.value)
          }
          className="rounded-lg border px-3 py-2"
        >
          <option value="">
            All Orders
          </option>

          {statusOptions.map((status) => (
            <option
              key={status}
              value={status}
            >
              {status}
            </option>
          ))}
        </select>

      </div>

      <div className="overflow-hidden rounded-xl bg-white shadow">

        <table className="w-full">

          <thead className="border-b bg-gray-50">

            <tr>
              <th className="px-6 py-3 text-left">
                Order
              </th>

              <th className="px-6 py-3 text-left">
                Customer
              </th>

              <th className="px-6 py-3 text-left">
                Email
              </th>

              <th className="px-6 py-3 text-left">
                Total
              </th>

              <th className="px-6 py-3 text-left">
                Status
              </th>

              <th className="px-6 py-3 text-left">
                Date
              </th>

              <th className="px-6 py-3 text-left">
                Update
              </th>
            </tr>

          </thead>

          <tbody>

            {orders.map((order) => (

              <tr
                key={order.public_id}
                className="border-b"
              >

                <td className="px-6 py-4">
                  {order.public_id.slice(0, 8)}
                </td>

                <td className="px-6 py-4">
                  {order.customer.first_name}{" "}
                  {order.customer.last_name ?? ""}
                </td>

                <td className="px-6 py-4">
                  {order.customer.email}
                </td>

                <td className="px-6 py-4">
                  ₹{order.total_amount}
                </td>

                <td className="px-6 py-4">

                  <span
                    className={`rounded-full px-2 py-1 text-xs ${
                      order.status === "delivered"
                        ? "bg-green-100 text-green-700"
                        : order.status === "cancelled"
                        ? "bg-red-100 text-red-700"
                        : order.status === "processing"
                        ? "bg-blue-100 text-blue-700"
                        : "bg-yellow-100 text-yellow-700"
                    }`}
                  >
                    {order.status}
                  </span>

                </td>

                <td className="px-6 py-4">
                  {new Date(
                    order.created_at
                  ).toLocaleDateString()}
                </td>

                <td className="px-6 py-4">

                  <select
                    value={order.status}
                    onChange={(e) =>
                      handleStatusChange(
                        order.public_id,
                        e.target.value
                      )
                    }
                    className="rounded border px-2 py-1"
                  >
                    {statusOptions.map((status) => (
                      <option
                        key={status}
                        value={status}
                      >
                        {status}
                      </option>
                    ))}
                  </select>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}