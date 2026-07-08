"use client";

import { useState } from "react";
import { Phone, phoneService } from "@/services/phone";
import { X } from "lucide-react";

interface PhoneFormProps {
  initialData?: Phone | null;
  onClose: () => void;
  onSuccess: () => void;
}

export default function PhoneForm({
  initialData,
  onClose,
  onSuccess,
}: PhoneFormProps) {
  const [phoneNumber, setPhoneNumber] = useState(initialData?.phone_number || "");
  const [isDefault, setIsDefault] = useState(initialData?.is_default || false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = {
        phone_number: phoneNumber,
        is_default: isDefault,
      };
      if (initialData) {
        await phoneService.update(initialData.public_id, data);
      } else {
        await phoneService.create(data);
      }
      onSuccess();
    } catch (error) {
      console.error("Failed to save phone number:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-3 sm:p-4">
      <div className="bg-white rounded-xl p-4 sm:p-6 max-w-md w-full">
        <div className="flex justify-between items-center gap-3 mb-4">
          <h2 className="text-lg sm:text-xl font-semibold">
            {initialData ? "Edit Phone Number" : "Add Phone Number"}
          </h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700 shrink-0">
            <X size={24} />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Phone Number *</label>
            <input
              type="tel"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              required
              placeholder="+91 9876543210"
              className="w-full border rounded-lg px-3 py-2"
            />
          </div>
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={isDefault}
              onChange={(e) => setIsDefault(e.target.checked)}
              id="defaultPhone"
            />
            <label htmlFor="defaultPhone" className="text-sm">Set as default</label>
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-black text-white py-2 rounded-lg disabled:opacity-50"
          >
            {loading ? "Saving..." : initialData ? "Update" : "Add Phone Number"}
          </button>
        </form>
      </div>
    </div>
  );
}