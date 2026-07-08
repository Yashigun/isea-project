import { ReactNode } from "react";

import { cn } from "@/lib/utils";

interface HeadingProps {
  title: string;
  subtitle?: ReactNode;
  className?: string;
}

export default function Heading({
  title,
  subtitle,
  className,
}: HeadingProps) {
  return (
    <div className={cn("space-y-2", className)}>
      <h2 className="text-2xl font-bold tracking-tight sm:text-3xl md:text-4xl">
        {title}
      </h2>

      {subtitle && (
        <p className="text-muted-foreground max-w-2xl text-sm sm:text-base md:text-lg">
          {subtitle}
        </p>
      )}
    </div>
  );
}
