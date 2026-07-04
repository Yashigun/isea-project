"use client";

import { createContext, useContext, ReactNode } from "react";

type TabsContextType = {
  activeTab: string;
  setActiveTab: (value: string) => void;
};

const TabsContext = createContext<TabsContextType | undefined>(undefined);

export function Tabs({
  children,
  value,
  onValueChange,
  className = "",
}: {
  children: ReactNode;
  value: string;
  onValueChange: (value: string) => void;
  className?: string;
}) {
  return (
    <TabsContext.Provider value={{ activeTab: value, setActiveTab: onValueChange }}>
      <div className={className}>{children}</div>
    </TabsContext.Provider>
  );
}

export function TabsList({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  return <div className={`flex gap-2 border-b border-gray-200 ${className}`}>{children}</div>;
}

export function TabsTrigger({
  children,
  value,
  className = "",
}: {
  children: ReactNode;
  value: string;
  className?: string;
}) {
  const context = useContext(TabsContext);
  if (!context) throw new Error("TabsTrigger must be used inside a Tabs component");

  const isActive = context.activeTab === value;

  return (
    <button
      onClick={() => context.setActiveTab(value)}
      className={`px-4 py-2 text-sm font-medium transition-colors ${
        isActive
          ? "border-b-2 border-black text-black"
          : "text-gray-500 hover:text-black"
      } ${className}`}
    >
      {children}
    </button>
  );
}

export function TabsContent({
  children,
  value,
  className = "",
}: {
  children: ReactNode;
  value: string;
  className?: string;
}) {
  const context = useContext(TabsContext);
  if (!context) throw new Error("TabsContent must be used inside a Tabs component");

  if (context.activeTab !== value) return null;

  return <div className={className}>{children}</div>;
}