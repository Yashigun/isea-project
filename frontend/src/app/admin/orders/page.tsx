"use client";

import {
  useCallback,
  useEffect,
  useState,
} from "react";

import Link from "next/link";

import {
  ArrowRight,
  Clock3,
} from "lucide-react";

import {
  orderService,
  Order,
} from "@/services/order";

const statusOptions = [
  "pending",
  "confirmed",
  "processing",
  "shipped",
  "delivered",
  "cancelled",
  "refunded",
];

const getStatusClasses = (status: string) => {
  switch (status) {
    case "delivered":
      return "bg-green-100 text-green-700";

    case "cancelled":
    case "refunded":
      return "bg-red-100 text-red-700";

    case "processing":
    case "shipped":
      return "bg-blue-100 text-blue-700";

    case "confirmed":
      return "bg-purple-100 text-purple-700";

    default:
      return "bg-yellow-100 text-yellow-700";
  }
};

const formatPaymentMethod = (
  paymentMethod: string | undefined
) => {
  if (!paymentMethod) {
    return "Not available";
  }

  return paymentMethod
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) =>
      character.toUpperCase()
    );
};

export default function AdminOrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [filterStatus, setFilterStatus] =
    useState("");

  const [updatingOrderId, setUpdatingOrderId] =
    useState<string | null>(null);

  const fetchOrders = useCallback(async () => {
    setLoading(true);

    try {
      const data = await orderService.listAll(
        filterStatus || undefined
      );

      setOrders(data);
    } catch (error) {
      console.error(
        "Failed to load orders",
        error
      );
    } finally {
      setLoading(false);
    }
  }, [filterStatus]);

  useEffect(() => {
    void Promise.resolve().then(fetchOrders);
  }, [fetchOrders]);

  const handleStatusChange = async (
    publicId: string,
    status: string
  ) => {
    setUpdatingOrderId(publicId);

    try {
      const updatedOrder =
        await orderService.updateStatus(
          publicId,
          status
        );

      setOrders((currentOrders) =>
        currentOrders.map((order) =>
          order.public_id === publicId
            ? {
                ...order,
                ...updatedOrder,
              }
            : order
        )
      );
    } catch (error) {
      console.error(
        "Failed to update order status",
        error
      );
    } finally {
      setUpdatingOrderId(null);
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-[300px] items-center justify-center p-8">
        <p className="text-sm text-gray-500">
          Loading orders...
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold sm:text-3xl">
            Orders
          </h1>

          <p className="mt-1 text-sm text-gray-500">
            Manage customer orders and transactions.
          </p>
        </div>

        <select
          value={filterStatus}
          onChange={(event) =>
            setFilterStatus(event.target.value)
          }
          className="w-full rounded-lg border bg-white px-3 py-2 text-sm sm:w-auto"
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

      <div className="overflow-hidden rounded-xl border bg-white shadow-sm">
        {orders.length === 0 ? (
          <div className="p-10 text-center">
            <p className="text-sm text-gray-500">
              No orders found.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-[1150px] w-full">
              <thead className="border-b bg-gray-50">
                <tr>
                  <th className="whitespace-nowrap px-5 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
                    Order
                  </th>

                  <th className="whitespace-nowrap px-5 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
                    Customer
                  </th>

                  <th className="whitespace-nowrap px-5 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
                    Email
                  </th>

                  <th className="whitespace-nowrap px-5 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
                    Total
                  </th>

                  <th className="whitespace-nowrap px-5 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
                    Payment
                  </th>

                  <th className="whitespace-nowrap px-5 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
                    Status
                  </th>

                  <th className="whitespace-nowrap px-5 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
                    Date
                  </th>

                  <th className="whitespace-nowrap px-5 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
                    Time
                  </th>

                  <th className="whitespace-nowrap px-5 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
                    Update
                  </th>

                  <th className="px-5 py-3 text-right text-xs font-semibold uppercase tracking-wide text-gray-500">
                    View
                  </th>
                </tr>
              </thead>

              <tbody className="divide-y">
                {orders.map((order) => (
                  <tr
                    key={order.public_id}
                    className="transition hover:bg-gray-50/70"
                  >
                    <td className="whitespace-nowrap px-5 py-4 text-sm font-medium">
                      {order.public_id.slice(0, 8)}
                    </td>

                    <td className="whitespace-nowrap px-5 py-4 text-sm">
                      {order.customer.first_name}{" "}
                      {order.customer.last_name ?? ""}
                    </td>

                    <td className="px-5 py-4 text-sm text-gray-600">
                      {order.customer.email}
                    </td>

                    <td className="whitespace-nowrap px-5 py-4 text-sm font-semibold">
                      ₹{order.total_amount}
                    </td>

                    <td className="whitespace-nowrap px-5 py-4 text-sm">
                      {formatPaymentMethod(
                        order.payment?.payment_method
                      )}
                    </td>

                    <td className="whitespace-nowrap px-5 py-4">
                      <span
                        className={`rounded-full px-2.5 py-1 text-xs font-medium capitalize ${getStatusClasses(
                          order.status
                        )}`}
                      >
                        {order.status}
                      </span>
                    </td>

                    <td className="whitespace-nowrap px-5 py-4 text-sm text-gray-600">
                      {new Date(
                        order.created_at
                      ).toLocaleDateString()}
                    </td>

                    <td className="whitespace-nowrap px-5 py-4">
                      <div className="flex items-center gap-1.5 text-sm text-gray-600">
                        <Clock3 size={15} />

                        {new Date(
                          order.created_at
                        ).toLocaleTimeString([], {
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </div>
                    </td>

                    <td className="whitespace-nowrap px-5 py-4">
                      <select
                        value={order.status}
                        disabled={
                          updatingOrderId ===
                          order.public_id
                        }
                        onChange={(event) =>
                          handleStatusChange(
                            order.public_id,
                            event.target.value
                          )
                        }
                        className="rounded-lg border bg-white px-2 py-1.5 text-sm disabled:cursor-not-allowed disabled:opacity-50"
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

                    <td className="px-5 py-4 text-right">
                      <Link
                        href={`/admin/orders/${order.public_id}`}
                        aria-label={`View order ${order.public_id}`}
                        className="inline-flex h-9 w-9 items-center justify-center rounded-full border text-gray-600 transition hover:border-black hover:bg-black hover:text-white"
                      >
                        <ArrowRight size={17} />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
