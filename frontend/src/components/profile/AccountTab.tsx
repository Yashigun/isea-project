"use client";

import { useState } from "react";
import { User } from "@/services/auth";
import { Address, addressService } from "@/services/address";
import { Phone, phoneService } from "@/services/phone";
import AddressForm from "./AddressForm";
import PhoneForm from "./PhoneForm";

interface AccountTabProps {
  user: User;
  addresses: Address[];
  phones: Phone[];
  onRefresh: () => void;
}

export default function AccountTab({
  user,
  addresses,
  phones,
  onRefresh,
}: AccountTabProps) {
  const [showAddressForm, setShowAddressForm] = useState(false);
  const [editingAddress, setEditingAddress] = useState<Address | null>(null);
  const [showPhoneForm, setShowPhoneForm] = useState(false);
  const [editingPhone, setEditingPhone] = useState<Phone | null>(null);
  const [loading, setLoading] = useState(false);

  const handleDeleteAddress = async (publicId: string) => {
    if (!confirm("Delete this address?")) return;
    setLoading(true);
    try {
      await addressService.delete(publicId);
      onRefresh();
    } catch (error) {
      console.error("Failed to delete address:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeletePhone = async (publicId: string) => {
    if (!confirm("Delete this phone number?")) return;
    setLoading(true);
    try {
      await phoneService.delete(publicId);
      onRefresh();
    } catch (error) {
      console.error("Failed to delete phone:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 sm:space-y-8">
      <h1 className="text-2xl font-bold sm:text-3xl">Account Settings</h1>

      {/* Personal Info */}
      <section className="bg-white rounded-xl shadow-sm border p-4 sm:p-6">
        <h2 className="text-lg font-semibold mb-4 sm:text-xl">Personal Information</h2>
        <div className="space-y-2 break-words">
          <p>
            <span className="font-medium">Name:</span> {user.first_name}{" "}
            {user.last_name}
          </p>
          <p>
            <span className="font-medium">Email:</span> {user.email}
          </p>
        </div>
      </section>

      {/* Addresses */}
      <section className="bg-white rounded-xl shadow-sm border p-4 sm:p-6">
        <div className="flex flex-col gap-3 mb-4 sm:flex-row sm:justify-between sm:items-center">
          <h2 className="text-lg font-semibold sm:text-xl">Addresses</h2>
          <button
            onClick={() => {
              setEditingAddress(null);
              setShowAddressForm(true);
            }}
            className="text-sm bg-black text-white px-4 py-2 rounded-lg w-full sm:w-auto"
          >
            Add Address
          </button>
        </div>
        {addresses.length === 0 ? (
          <p className="text-gray-500">No addresses saved.</p>
        ) : (
          <div className="space-y-3">
            {addresses.map((addr) => (
              <div
                key={addr.public_id}
                className="border rounded-lg p-4 flex flex-col gap-3 sm:flex-row sm:justify-between sm:items-start"
              >
                <div className="min-w-0 break-words">
                  <p className="font-medium">
                    {addr.address_line_1}
                    {addr.address_line_2 && `, ${addr.address_line_2}`}
                  </p>
                  <p className="text-sm text-gray-600">
                    {addr.city}, {addr.state} {addr.postal_code}
                  </p>
                  <p className="text-sm text-gray-500">{addr.country}</p>
                  {addr.is_default && (
                    <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
                      Default
                    </span>
                  )}
                </div>
                <div className="flex gap-2 shrink-0">
                  <button
                    onClick={() => {
                      setEditingAddress(addr);
                      setShowAddressForm(true);
                    }}
                    className="text-sm text-blue-600 hover:text-blue-800"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDeleteAddress(addr.public_id)}
                    className="text-sm text-red-600 hover:text-red-800"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Phone Numbers */}
      <section className="bg-white rounded-xl shadow-sm border p-4 sm:p-6">
        <div className="flex flex-col gap-3 mb-4 sm:flex-row sm:justify-between sm:items-center">
          <h2 className="text-lg font-semibold sm:text-xl">Phone Numbers</h2>
          <button
            onClick={() => {
              setEditingPhone(null);
              setShowPhoneForm(true);
            }}
            className="text-sm bg-black text-white px-4 py-2 rounded-lg w-full sm:w-auto"
          >
            Add Phone Number
          </button>
        </div>
        {phones.length === 0 ? (
          <p className="text-gray-500">No phone numbers saved.</p>
        ) : (
          <div className="space-y-3">
            {phones.map((phone) => (
              <div
                key={phone.public_id}
                className="border rounded-lg p-4 flex flex-col gap-3 sm:flex-row sm:justify-between sm:items-center"
              >
                <div className="min-w-0 break-words">
                  <p className="font-medium">{phone.phone_number}</p>
                  {phone.is_default && (
                    <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
                      Default
                    </span>
                  )}
                </div>
                <div className="flex gap-2 shrink-0">
                  <button
                    onClick={() => {
                      setEditingPhone(phone);
                      setShowPhoneForm(true);
                    }}
                    className="text-sm text-blue-600 hover:text-blue-800"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDeletePhone(phone.public_id)}
                    className="text-sm text-red-600 hover:text-red-800"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Modals */}
      {showAddressForm && (
        <AddressForm
          initialData={editingAddress}
          onClose={() => {
            setShowAddressForm(false);
            setEditingAddress(null);
          }}
          onSuccess={() => {
            setShowAddressForm(false);
            setEditingAddress(null);
            onRefresh(); // ✅ This calls fetchData in parent
          }}
        />
      )}

      {showPhoneForm && (
        <PhoneForm
          initialData={editingPhone}
          onClose={() => {
            setShowPhoneForm(false);
            setEditingPhone(null);
          }}
          onSuccess={() => {
            setShowPhoneForm(false);
            setEditingPhone(null);
            onRefresh();
          }}
        />
      )}
    </div>
  );
}
