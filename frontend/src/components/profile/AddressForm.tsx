"use client";

import { useState } from "react";
import { addressService } from "@/services/address";
import { X } from "lucide-react";
import { Address } from "@/types/address";

interface AddressFormProps {
  initialData?: Address | null;
  onClose: () => void;
  onSuccess: () => void;
}

export default function AddressForm({
  initialData,
  onClose,
  onSuccess,
}: AddressFormProps) {
  const [addressLine1, setAddressLine1] = useState(initialData?.address_line_1 || "");
  const [addressLine2, setAddressLine2] = useState(initialData?.address_line_2 || "");
  const [city, setCity] = useState(initialData?.city || "");
  const [state, setState] = useState(initialData?.state || "");
  const [country, setCountry] = useState(initialData?.country || "");
  const [postalCode, setPostalCode] = useState(initialData?.postal_code || "");
  const [isDefault, setIsDefault] = useState(initialData?.is_default || false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const data = {
        address_line_1: addressLine1,
        address_line_2: addressLine2 || undefined,
        city,
        state,
        country,
        postal_code: postalCode,
        is_default: isDefault,
      };

      console.log("📦 Saving address:", data);

      if (initialData) {
        await addressService.update(initialData.public_id, data);
      } else {
        await addressService.create(data);
      }

      console.log("✅ Address saved successfully");
      onSuccess();
    } catch (err: any) {
      console.error("❌ Failed to save address:", err);
      if (err.response) {
        setError(err.response.data?.detail || "Failed to save address");
      } else {
        setError("Network error. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div className="bg-white rounded-xl p-6 max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">
            {initialData ? "Edit Address" : "Add Address"}
          </h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <X size={24} />
          </button>
        </div>

        {error && (
          <div className="bg-red-50 text-red-700 p-3 rounded-lg mb-4 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Address Line 1 *</label>
            <input
              value={addressLine1}
              onChange={(e) => setAddressLine1(e.target.value)}
              required
              className="w-full border rounded-lg px-3 py-2"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Address Line 2</label>
            <input
              value={addressLine2}
              onChange={(e) => setAddressLine2(e.target.value)}
              className="w-full border rounded-lg px-3 py-2"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">City *</label>
            <input
              value={city}
              onChange={(e) => setCity(e.target.value)}
              required
              className="w-full border rounded-lg px-3 py-2"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">State *</label>
            <input
              value={state}
              onChange={(e) => setState(e.target.value)}
              required
              className="w-full border rounded-lg px-3 py-2"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Country *</label>
            <input
              value={country}
              onChange={(e) => setCountry(e.target.value)}
              required
              className="w-full border rounded-lg px-3 py-2"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Postal Code *</label>
            <input
              value={postalCode}
              onChange={(e) => setPostalCode(e.target.value)}
              required
              className="w-full border rounded-lg px-3 py-2"
            />
          </div>
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={isDefault}
              onChange={(e) => setIsDefault(e.target.checked)}
              id="defaultAddress"
            />
            <label htmlFor="defaultAddress" className="text-sm">Set as default</label>
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-black text-white py-2 rounded-lg disabled:opacity-50"
          >
            {loading ? "Saving..." : initialData ? "Update" : "Add Address"}
          </button>
        </form>
      </div>
    </div>
  );
}