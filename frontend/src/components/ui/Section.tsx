import { ReactNode } from "react";

import { cn } from "@/lib/utils";

interface SectionProps {
  children: ReactNode;
  className?: string;
}

export default function Section({
  children,
  className,
}: SectionProps) {
  return (
    <section
      className={cn(
        "py-10 sm:py-12 md:py-20 lg:py-24",
        className
      )}
    >
      {children}
    </section>
  );
}
