"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { CreditCard, Minus, Plus, ReceiptText, Trash2, WalletCards } from "lucide-react";
import AuthGuard from "@/components/auth/AuthGuard";
import { cartService, Cart } from "@/services/cart";
import { addressService } from "@/services/address";
import { orderService } from "@/services/order";
import { Address } from "@/types/address";

export default function CartPage() {
  const [cart, setCart] = useState<Cart | null>(null);
  const [addresses, setAddresses] = useState<Address[]>([]);
  const [addressId, setAddressId] = useState("");
  const [notes, setNotes] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("cod");
  const [loading, setLoading] = useState(true);
  const [placing, setPlacing] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const loadCart = async () => {
    setLoading(true);
    try {
      const [cartData, addressData] = await Promise.all([
        cartService.get(),
        addressService.getAll(),
      ]);
      setCart(cartData);
      setAddresses(addressData);
      setAddressId((current) => current || addressData[0]?.public_id || "");
    } catch (error) {
      console.error("Failed to load checkout:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void Promise.resolve().then(loadCart);
  }, []);

  const updateQuantity = async (productPublicId: string, quantity: number) => {
    if (quantity < 1) return;
    const updated = await cartService.updateItem(productPublicId, quantity);
    setCart(updated);
    window.dispatchEvent(
      new CustomEvent("cart:updated", { detail: { totalItems: updated.total_items } })
    );
  };

  const getImage = (image: string | null | undefined) =>
    image
      ? image.startsWith("//")
        ? `https:${image}`
        : image.replace("http://res.cloudinary.com", "https://res.cloudinary.com")
      : "/placeholder.jpg";

  const removeItem = async (productPublicId: string) => {
    const updated = await cartService.removeItem(productPublicId);
    setCart(updated);
    window.dispatchEvent(
      new CustomEvent("cart:updated", { detail: { totalItems: updated.total_items } })
    );
  };

  const placeOrder = async () => {
    if (!addressId) {
      setMessage("Please add or select a shipping address from your profile.");
      return;
    }

    setPlacing(true);
    setMessage(null);
    try {
      const order = await orderService.create({
        shipping_address_public_id: addressId,
        order_notes: notes || undefined,
      });
      setMessage(`Order ${order.public_id.slice(0, 8)} is ready.`);
      await loadCart();
      window.dispatchEvent(new CustomEvent("cart:updated", { detail: { totalItems: 0 } }));
    } catch (error: unknown) {
      const detail =
        typeof error === "object" &&
        error !== null &&
        "response" in error &&
        typeof (error as { response?: { data?: { detail?: unknown } } }).response?.data?.detail === "string"
          ? (error as { response: { data: { detail: string } } }).response.data.detail
          : null;
      setMessage(detail || "Could not place order.");
    } finally {
      setPlacing(false);
    }
  };

  return (
    <AuthGuard>
      <main className="mx-auto max-w-6xl px-4 py-10">
        <div className="mb-8 flex items-center gap-3">
          <ReceiptText size={30} />
          <h1 className="text-3xl font-semibold">Checkout Invoice</h1>
        </div>

        {loading ? (
          <p>Loading checkout...</p>
        ) : !cart || cart.items.length === 0 ? (
          <div className="rounded-lg border bg-white p-10 text-center">
            <p className="text-gray-500">Your bag is empty.</p>
            <Link href="/" className="mt-5 inline-block rounded-full bg-black px-6 py-3 text-white">
              Continue Shopping
            </Link>
          </div>
        ) : (
          <div className="grid gap-8 lg:grid-cols-[1fr_380px]">
            <section className="rounded-lg border bg-white">
              <div className="grid grid-cols-[1fr_120px_120px] border-b px-5 py-3 text-sm font-medium text-gray-500">
                <span>Item</span>
                <span>Qty</span>
                <span className="text-right">Amount</span>
              </div>
              {cart.items.map((item) => (
                <div
                  key={item.public_id}
                  className="grid grid-cols-[1fr_120px_120px] items-center gap-4 border-b px-5 py-5"
                >
                  <div className="flex items-center gap-4">
                    <Image
                      src={getImage(item.product.primary_image)}
                      alt={item.product.name}
                      width={72}
                      height={72}
                      className="h-18 w-18 rounded-lg object-cover"
                    />
                    <div>
                      <Link href={`/products/${item.product.slug}`} className="font-medium">
                        {item.product.name}
                      </Link>
                      <p className="text-sm text-gray-500">₹{item.unit_price}</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => updateQuantity(item.product.public_id, item.quantity - 1)}
                      className="rounded-full border p-2"
                      aria-label="Decrease quantity"
                    >
                      <Minus size={14} />
                    </button>
                    <span className="w-7 text-center">{item.quantity}</span>
                    <button
                      type="button"
                      onClick={() => updateQuantity(item.product.public_id, item.quantity + 1)}
                      className="rounded-full border p-2"
                      aria-label="Increase quantity"
                    >
                      <Plus size={14} />
                    </button>
                    <button
                      type="button"
                      onClick={() => removeItem(item.product.public_id)}
                      className="ml-2 rounded-full border p-2 text-red-600"
                      aria-label="Remove item"
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>

                  <p className="text-right font-semibold">₹{item.subtotal}</p>
                </div>
              ))}
            </section>

            <aside className="h-fit rounded-lg border bg-white p-6">
              <h2 className="text-xl font-semibold">Ready to Order</h2>
              <div className="mt-5 space-y-3 text-sm">
                <Row label="Subtotal" value={`₹${cart.subtotal}`} />
                <Row label="Discount" value={`₹${cart.discount}`} />
                <Row label="Tax" value={`₹${cart.tax}`} />
                <Row label="Products Total" value={`₹${cart.items.reduce((sum, item) => sum + Number(item.subtotal), 0).toFixed(2)}`} />
                <Row label="Total" value={`₹${cart.total_amount}`} strong />
              </div>

              <label className="mt-6 block text-sm font-medium">Shipping Address</label>
              <select
                value={addressId}
                onChange={(event) => setAddressId(event.target.value)}
                className="mt-2 w-full rounded-lg border px-3 py-2"
              >
                <option value="">Select address</option>
                {addresses.map((address) => (
                  <option key={address.public_id} value={address.public_id}>
                    {address.address_line_1}, {address.city}
                  </option>
                ))}
              </select>

              <label className="mt-4 block text-sm font-medium">Order Notes</label>
              <textarea
                value={notes}
                onChange={(event) => setNotes(event.target.value)}
                rows={3}
                className="mt-2 w-full rounded-lg border px-3 py-2"
              />

              <div className="mt-5">
                <p className="text-sm font-medium">Payment Method</p>
                <div className="mt-2 space-y-2">
                  <label className="flex cursor-pointer items-center gap-3 rounded-lg border p-3">
                    <input
                      type="radio"
                      name="payment"
                      value="cod"
                      checked={paymentMethod === "cod"}
                      onChange={(event) => setPaymentMethod(event.target.value)}
                    />
                    <WalletCards size={18} />
                    Cash on Delivery
                  </label>
                  <label className="flex cursor-pointer items-center gap-3 rounded-lg border p-3 opacity-70">
                    <input
                      type="radio"
                      name="payment"
                      value="card"
                      checked={paymentMethod === "card"}
                      onChange={(event) => setPaymentMethod(event.target.value)}
                    />
                    <CreditCard size={18} />
                    Card Payment
                  </label>
                </div>
              </div>

              {message && <p className="mt-4 text-sm text-gray-600">{message}</p>}

              <button
                type="button"
                onClick={placeOrder}
                disabled={placing}
                className="mt-6 w-full rounded-full bg-black px-5 py-3 text-white disabled:opacity-50"
              >
                {placing ? "Checking Out..." : "Checkout"}
              </button>
            </aside>
          </div>
        )}
      </main>
    </AuthGuard>
  );
}

function Row({
  label,
  value,
  strong = false,
}: {
  label: string;
  value: string;
  strong?: boolean;
}) {
  return (
    <div className={`flex justify-between ${strong ? "border-t pt-3 text-lg font-semibold" : ""}`}>
      <span>{label}</span>
      <span>{value}</span>
    </div>
  );
}
