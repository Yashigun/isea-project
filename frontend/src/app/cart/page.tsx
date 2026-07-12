"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import {
  Banknote,
  Building2,
  CreditCard,
  Minus,
  Plus,
  ReceiptText,
  Smartphone,
  Trash2,
} from "lucide-react";
import confetti from "canvas-confetti";
import { CheckCircle2, X } from "lucide-react";

import AuthGuard from "@/components/auth/AuthGuard";
import { cartService, Cart } from "@/services/cart";
import { addressService } from "@/services/address";
import { orderService } from "@/services/order";
import { phoneService } from "@/services/phone";

import { Address } from "@/types/address";
import { Phone } from "@/types/phone";

type PaymentMethod =
  | "card"
  | "upi"
  | "net_banking"
  | "cod";

export default function CartPage() {
  const [cart, setCart] = useState<Cart | null>(null);

  const [addresses, setAddresses] = useState<Address[]>([]);
  const [addressId, setAddressId] = useState("");

  const [phones, setPhones] = useState<Phone[]>([]);
  const [phoneId, setPhoneId] = useState("");

  const [notes, setNotes] = useState("");

  const [paymentMethod, setPaymentMethod] =
    useState<PaymentMethod>("cod");

  const [loading, setLoading] = useState(true);
  const [placing, setPlacing] = useState(false);

  const [orderSuccessOpen, setOrderSuccessOpen] =
    useState(false);

  const [placedOrderId, setPlacedOrderId] =
    useState("");

  const [updatingItems, setUpdatingItems] =
    useState<Set<string>>(() => new Set());

  const [message, setMessage] =
    useState<string | null>(null);

  const dispatchCartUpdated = (totalItems: number) => {
    window.dispatchEvent(
      new CustomEvent("cart:updated", {
        detail: {
          totalItems,
        },
      })
    );
  };

  const loadCart = async () => {
    setLoading(true);

    try {
      const [cartData, addressData, phoneData] =
        await Promise.all([
          cartService.get(),
          addressService.getAll(),
          phoneService.getAll(),
        ]);

      setCart(cartData);
      setAddresses(addressData);
      setPhones(phoneData);

      setAddressId((current) => {
        if (current) {
          return current;
        }

        const defaultAddress = addressData.find(
          (address) => address.is_default
        );

        return (
          defaultAddress?.public_id ??
          addressData[0]?.public_id ??
          ""
        );
      });

      setPhoneId((current) => {
        if (current) {
          return current;
        }

        const defaultPhone = phoneData.find(
          (phone) => phone.is_default
        );

        return (
          defaultPhone?.public_id ??
          phoneData[0]?.public_id ??
          ""
        );
      });
    } catch (error) {
      console.error(
        "Failed to load checkout:",
        error
      );

      setMessage(
        "Could not load checkout information."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void Promise.resolve().then(loadCart);
  }, []);

  const updateQuantity = async (
    productPublicId: string,
    quantity: number
  ) => {
    if (quantity < 1) {
      return;
    }

    if (updatingItems.has(productPublicId)) {
      return;
    }

    let previousCart: Cart | null = null;
    let optimisticTotalItems: number | null = null;

    setUpdatingItems((current) => {
      const next = new Set(current);
      next.add(productPublicId);
      return next;
    });

    setCart((currentCart) => {
      if (!currentCart) {
        return currentCart;
      }

      previousCart = currentCart;

      const updatedItems = currentCart.items.map(
        (item) => {
          if (
            item.product.public_id !==
            productPublicId
          ) {
            return item;
          }

          const unitPrice = Number(item.unit_price);
          const newSubtotal =
            unitPrice * quantity;

          return {
            ...item,
            quantity,
            subtotal: newSubtotal.toFixed(2),
          };
        }
      );

      const totalItems = updatedItems.reduce(
        (sum, item) => sum + item.quantity,
        0
      );

      const subtotal = updatedItems.reduce(
        (sum, item) =>
          sum + Number(item.subtotal),
        0
      );

      const discount = Number(
        currentCart.discount
      );

      const tax = Number(currentCart.tax);

      const totalAmount =
        subtotal - discount + tax;

      optimisticTotalItems = totalItems;

      return {
        ...currentCart,
        items: updatedItems,
        total_items: totalItems,
        subtotal: subtotal.toFixed(2),
        total_amount: totalAmount.toFixed(2),
      };
    });

    if (optimisticTotalItems !== null) {
      dispatchCartUpdated(
        optimisticTotalItems
      );
    }

    try {
      const updated =
        await cartService.updateItem(
          productPublicId,
          quantity
        );

      setCart(updated);

      dispatchCartUpdated(
        updated.total_items
      );
    } catch (error) {
      console.error(
        "Failed to update quantity:",
        error
      );

      if (previousCart) {
        setCart(previousCart);

        dispatchCartUpdated(
          previousCart.total_items
        );
      }

      setMessage(
        "Could not update product quantity."
      );
    } finally {
      setUpdatingItems((current) => {
        const next = new Set(current);
        next.delete(productPublicId);
        return next;
      });
    }
  };

  const getImage = (
    image: string | null | undefined
  ) =>
    image
      ? image.startsWith("//")
        ? `https:${image}`
        : image.replace(
            "http://res.cloudinary.com",
            "https://res.cloudinary.com"
          )
      : "/placeholder.jpg";

  const removeItem = async (
    productPublicId: string
  ) => {
    let previousCart: Cart | null = null;
    let optimisticTotalItems: number | null =
      null;

    setCart((currentCart) => {
      if (!currentCart) {
        return currentCart;
      }

      previousCart = currentCart;

      const updatedItems =
        currentCart.items.filter(
          (item) =>
            item.product.public_id !==
            productPublicId
        );

      const totalItems = updatedItems.reduce(
        (sum, item) => sum + item.quantity,
        0
      );

      const subtotal = updatedItems.reduce(
        (sum, item) =>
          sum + Number(item.subtotal),
        0
      );

      const discount = Number(
        currentCart.discount
      );

      const tax = Number(currentCart.tax);

      const totalAmount =
        subtotal - discount + tax;

      optimisticTotalItems = totalItems;

      return {
        ...currentCart,
        items: updatedItems,
        total_items: totalItems,
        subtotal: subtotal.toFixed(2),
        total_amount: totalAmount.toFixed(2),
      };
    });

    if (optimisticTotalItems !== null) {
      dispatchCartUpdated(
        optimisticTotalItems
      );
    }

    try {
      const updated =
        await cartService.removeItem(
          productPublicId
        );

      setCart(updated);

      dispatchCartUpdated(
        updated.total_items
      );
    } catch (error) {
      console.error(
        "Failed to remove item:",
        error
      );

      if (previousCart) {
        setCart(previousCart);

        dispatchCartUpdated(
          previousCart.total_items
        );
      }

      setMessage(
        "Could not remove product from cart."
      );
    }
  };

  const launchOrderConfetti = () => {
    const duration = 2500;
    const animationEnd =
      Date.now() + duration;

    const interval = window.setInterval(() => {
      const timeLeft =
        animationEnd - Date.now();

      if (timeLeft <= 0) {
        window.clearInterval(interval);
        return;
      }

      confetti({
        particleCount: 40,
        spread: 80,
        startVelocity: 30,
        origin: {
          x: Math.random(),
          y: Math.random() * 0.3,
        },
      });
    }, 250);
  };

  const placeOrder = async () => {
    if (!addressId) {
      setMessage(
        "Please add or select a shipping address from your profile."
      );
      return;
    }

    if (!phoneId) {
      setMessage(
        "Please add or select a phone number from your profile."
      );
      return;
    }

    setPlacing(true);
    setMessage(null);

    try {
      const order = await orderService.create({
        shipping_address_public_id: addressId,
        phone_public_id: phoneId,
        payment_method: paymentMethod,
        order_notes: notes || undefined,
      });

      setPlacedOrderId(order.public_id);
      setOrderSuccessOpen(true);

      launchOrderConfetti();

      await loadCart();

      dispatchCartUpdated(0);
    } catch (error: unknown) {
      const detail =
        typeof error === "object" &&
        error !== null &&
        "response" in error &&
        typeof (
          error as {
            response?: {
              data?: {
                detail?: unknown;
              };
            };
          }
        ).response?.data?.detail === "string"
          ? (
              error as {
                response: {
                  data: {
                    detail: string;
                  };
                };
              }
            ).response.data.detail
          : null;

      setMessage(
        detail || "Could not place order."
      );
    } finally {
      setPlacing(false);
    }
  };

  return (
    <AuthGuard>
      {orderSuccessOpen && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4 backdrop-blur-sm"
          role="dialog"
          aria-modal="true"
          aria-labelledby="order-success-title"
        >
          <div className="relative w-full max-w-md rounded-3xl bg-white p-8 text-center shadow-2xl">
            <button
              type="button"
              onClick={() =>
                setOrderSuccessOpen(false)
              }
              className="absolute right-5 top-5 rounded-full p-2 text-gray-500 transition hover:bg-gray-100 hover:text-black"
              aria-label="Close order confirmation"
            >
              <X size={20} />
            </button>

            <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-green-100 text-green-600">
              <CheckCircle2
                size={44}
                strokeWidth={1.8}
              />
            </div>

            <h2
              id="order-success-title"
              className="mt-6 text-2xl font-semibold"
            >
              Order Placed Successfully!
            </h2>

            <p className="mt-3 text-sm leading-6 text-gray-500">
              Thank you for your order. Your order
              has been received and is now being
              processed.
            </p>

            <div className="mt-5 rounded-xl bg-gray-50 px-4 py-3">
              <p className="text-xs uppercase tracking-wide text-gray-500">
                Order ID
              </p>

              <p className="mt-1 font-medium">
                {placedOrderId}
              </p>
            </div>

            <div className="mt-7 flex gap-3">
              <Link
                href="/orders"
                className="flex-1 rounded-full border border-black px-5 py-3 text-sm font-medium transition hover:bg-gray-50"
              >
                View Orders
              </Link>

              <Link
                href="/"
                className="flex-1 rounded-full bg-black px-5 py-3 text-sm font-medium text-white transition hover:bg-gray-800"
              >
                Continue Shopping
              </Link>
            </div>
          </div>
        </div>
      )}

      <main className="mx-auto max-w-6xl px-4 py-10">
        <div className="mb-8 flex items-center gap-3">
          <ReceiptText size={30} />

          <h1 className="text-3xl font-semibold">
            Checkout Invoice
          </h1>
        </div>

        {loading ? (
          <p>Loading checkout...</p>
        ) : !cart ||
          cart.items.length === 0 ? (
          <div className="rounded-lg border bg-white p-10 text-center">
            <p className="text-gray-500">
              Your bag is empty.
            </p>

            <Link
              href="/"
              className="mt-5 inline-block rounded-full bg-black px-6 py-3 text-white"
            >
              Continue Shopping
            </Link>
          </div>
        ) : (
          <div className="grid gap-8 lg:grid-cols-[1fr_380px]">
            <section className="rounded-lg border bg-white">
              <div className="grid grid-cols-[1fr_120px_120px] border-b px-5 py-3 text-sm font-medium text-gray-500">
                <span>Item</span>
                <span>Qty</span>
                <span className="text-right">
                  Amount
                </span>
              </div>

              {cart.items.map((item) => {
                const isUpdating =
                  updatingItems.has(
                    item.product.public_id
                  );

                return (
                  <div
                    key={item.public_id}
                    className="grid grid-cols-[1fr_120px_120px] items-center gap-4 border-b px-5 py-5"
                  >
                    <div className="flex items-center gap-4">
                      <Image
                        src={getImage(
                          item.product.primary_image
                        )}
                        alt={item.product.name}
                        width={72}
                        height={72}
                        className="h-18 w-18 rounded-lg object-cover"
                      />

                      <div>
                        <Link
                          href={`/products/${item.product.slug}`}
                          className="font-medium"
                        >
                          {item.product.name}
                        </Link>

                        <p className="text-sm text-gray-500">
                          ₹{item.unit_price}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        type="button"
                        onClick={() =>
                          updateQuantity(
                            item.product.public_id,
                            item.quantity - 1
                          )
                        }
                        disabled={
                          isUpdating ||
                          item.quantity <= 1
                        }
                        className="rounded-full border p-2 disabled:cursor-not-allowed disabled:opacity-40"
                        aria-label="Decrease quantity"
                      >
                        <Minus size={14} />
                      </button>

                      <span className="w-7 text-center">
                        {item.quantity}
                      </span>

                      <button
                        type="button"
                        onClick={() =>
                          updateQuantity(
                            item.product.public_id,
                            item.quantity + 1
                          )
                        }
                        disabled={isUpdating}
                        className="rounded-full border p-2 disabled:cursor-not-allowed disabled:opacity-40"
                        aria-label="Increase quantity"
                      >
                        <Plus size={14} />
                      </button>

                      <button
                        type="button"
                        onClick={() =>
                          removeItem(
                            item.product.public_id
                          )
                        }
                        disabled={isUpdating}
                        className="ml-2 rounded-full border p-2 text-red-600 disabled:cursor-not-allowed disabled:opacity-40"
                        aria-label="Remove item"
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>

                    <p className="text-right font-semibold">
                      ₹{item.subtotal}
                    </p>
                  </div>
                );
              })}
            </section>

            <aside className="h-fit rounded-lg border bg-white p-6">
              <h2 className="text-xl font-semibold">
                Ready to Order
              </h2>

              <div className="mt-5 space-y-3 text-sm">
                <Row
                  label="Subtotal"
                  value={`₹${cart.subtotal}`}
                />

                <Row
                  label="Discount"
                  value={`₹${cart.discount}`}
                />

                <Row
                  label="Tax"
                  value={`₹${cart.tax}`}
                />

                <Row
                  label="Products Total"
                  value={`₹${cart.items
                    .reduce(
                      (sum, item) =>
                        sum +
                        Number(item.subtotal),
                      0
                    )
                    .toFixed(2)}`}
                />

                <Row
                  label="Total"
                  value={`₹${cart.total_amount}`}
                  strong
                />
              </div>

              <label className="mt-6 block text-sm font-medium">
                Shipping Address
              </label>

              <select
                value={addressId}
                onChange={(event) =>
                  setAddressId(event.target.value)
                }
                className="mt-2 w-full rounded-lg border px-3 py-2"
              >
                <option value="">
                  Select address
                </option>

                {addresses.map((address) => (
                  <option
                    key={address.public_id}
                    value={address.public_id}
                  >
                    {address.address_line_1},{" "}
                    {address.city}
                  </option>
                ))}
              </select>

              <label className="mt-4 block text-sm font-medium">
                Phone Number
              </label>

              <select
                value={phoneId}
                onChange={(event) =>
                  setPhoneId(event.target.value)
                }
                className="mt-2 w-full rounded-lg border px-3 py-2"
              >
                <option value="">
                  Select phone number
                </option>

                {phones.map((phone) => (
                  <option
                    key={phone.public_id}
                    value={phone.public_id}
                  >
                    {phone.phone_number}
                    {phone.is_default
                      ? " (Default)"
                      : ""}
                  </option>
                ))}
              </select>

              <label className="mt-4 block text-sm font-medium">
                Order Notes
              </label>

              <textarea
                value={notes}
                onChange={(event) =>
                  setNotes(event.target.value)
                }
                rows={3}
                className="mt-2 w-full rounded-lg border px-3 py-2"
              />

              <div className="mt-5">
                <p className="text-sm font-medium">
                  Payment Method
                </p>

                <div className="mt-2 space-y-2">
                  <label className="flex cursor-pointer items-center gap-3 rounded-lg border p-3">
                    <input
                      type="radio"
                      name="payment"
                      value="cod"
                      checked={
                        paymentMethod === "cod"
                      }
                      onChange={() =>
                        setPaymentMethod("cod")
                      }
                    />

                    <Banknote size={18} />

                    Cash on Delivery
                  </label>

                  <label className="flex cursor-pointer items-center gap-3 rounded-lg border p-3">
                    <input
                      type="radio"
                      name="payment"
                      value="upi"
                      checked={
                        paymentMethod === "upi"
                      }
                      onChange={() =>
                        setPaymentMethod("upi")
                      }
                    />

                    <Smartphone size={18} />

                    UPI
                  </label>

                  <label className="flex cursor-pointer items-center gap-3 rounded-lg border p-3">
                    <input
                      type="radio"
                      name="payment"
                      value="card"
                      checked={
                        paymentMethod === "card"
                      }
                      onChange={() =>
                        setPaymentMethod("card")
                      }
                    />

                    <CreditCard size={18} />

                    Card Payment
                  </label>

                  <label className="flex cursor-pointer items-center gap-3 rounded-lg border p-3">
                    <input
                      type="radio"
                      name="payment"
                      value="net_banking"
                      checked={
                        paymentMethod ===
                        "net_banking"
                      }
                      onChange={() =>
                        setPaymentMethod(
                          "net_banking"
                        )
                      }
                    />

                    <Building2 size={18} />

                    Net Banking
                  </label>
                </div>
              </div>

              {message && (
                <p className="mt-4 text-sm text-gray-600">
                  {message}
                </p>
              )}

              <button
                type="button"
                onClick={placeOrder}
                disabled={placing}
                className="mt-6 w-full rounded-full bg-black px-5 py-3 text-white disabled:opacity-50"
              >
                {placing
                  ? "Checking Out..."
                  : "Checkout"}
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
    <div
      className={`flex justify-between ${
        strong
          ? "border-t pt-3 text-lg font-semibold"
          : ""
      }`}
    >
      <span>{label}</span>
      <span>{value}</span>
    </div>
  );
}
