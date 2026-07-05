"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/context/AuthContext";
import AuthGuard from "@/components/auth/AuthGuard";
import ProfileSidebar from "@/components/profile/ProfileSidebar";
import DashboardTab from "@/components/profile/DashboardTab";
import AccountTab from "@/components/profile/AccountTab";

import { cartService, Cart } from "@/services/cart";
import { wishlistService } from "@/services/wishlist";
import { addressService } from "@/services/address";
import { phoneService } from "@/services/phone";

import { Product } from "@/types/product";
import { Address } from "@/types/address";
import { Phone } from "@/types/phone";

export default function ProfilePage() {
  const { user } = useAuth();

  const [activeTab, setActiveTab] = useState<"dashboard" | "account">(
    "dashboard"
  );

  const [cart, setCart] = useState<Cart | null>(null);
  const [wishlist, setWishlist] = useState<Product[]>([]);
  const [addresses, setAddresses] = useState<Address[]>([]);
  const [phones, setPhones] = useState<Phone[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);

    try {
      const [
        cartResult,
        wishlistResult,
        addressesResult,
        phonesResult,
      ] = await Promise.allSettled([
        cartService.get(),
        wishlistService.get(),
        addressService.getAll(),
        phoneService.getAll(),
      ]);

      // ----------------------------
      // Cart
      // ----------------------------
      if (cartResult.status === "fulfilled") {
        setCart(cartResult.value);
      } else {
        console.error("Failed to fetch cart:", cartResult.reason);
        setCart(null);
      }

      // ----------------------------
      // Wishlist
      // ----------------------------
      if (wishlistResult.status === "fulfilled") {
        setWishlist(wishlistResult.value as Product[]);
      } else {
        console.error("Failed to fetch wishlist:", wishlistResult.reason);
        setWishlist([]);
      }

      // ----------------------------
      // Addresses
      // ----------------------------
      if (addressesResult.status === "fulfilled") {
        setAddresses(addressesResult.value);
      } else {
        console.error("Failed to fetch addresses:", addressesResult.reason);
        setAddresses([]);
      }

      // ----------------------------
      // Phone Numbers
      // ----------------------------
      if (phonesResult.status === "fulfilled") {
        setPhones(phonesResult.value);
      } else {
        console.error("Failed to fetch phone numbers:", phonesResult.reason);
        setPhones([]);
      }

      console.log("Profile data loaded");
    } catch (error) {
      // This should rarely execute because Promise.allSettled()
      // does not reject on individual request failures.
      console.error("Unexpected error while loading profile:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user) {
      fetchData();
    }
  }, [user]);

  if (!user) return null;

  return (
    <AuthGuard>
      <div className="container mx-auto max-w-7xl py-10 px-4">
        <div className="flex flex-col md:flex-row gap-8">

          <div className="w-full md:w-64 flex-shrink-0">
            <ProfileSidebar
              activeTab={activeTab}
              onTabChange={setActiveTab}
              user={user}
            />
          </div>

          <div className="flex-1">
            {loading ? (
              <div className="flex justify-center py-20">
                <div className="text-gray-500">Loading...</div>
              </div>
            ) : (
              <>
                {activeTab === "dashboard" && (
                  <DashboardTab
                    cart={cart}
                    wishlist={wishlist}
                    onRefresh={fetchData}
                  />
                )}

                {activeTab === "account" && (
                  <AccountTab
                    user={user}
                    addresses={addresses}
                    phones={phones}
                    onRefresh={fetchData}
                  />
                )}
              </>
            )}
          </div>

        </div>
      </div>
    </AuthGuard>
  );
}