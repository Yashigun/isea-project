import { cn } from "@/lib/utils";

interface SectionHeadingProps {
  title: string;
  subtitle?: string;
  className?: string;
  align?: "left" | "center";
}

export default function SectionHeading({
  title,
  subtitle,
  className,
  align = "center",
}: SectionHeadingProps) {
  return (
    <div
      className={cn(
        "mb-12",
        align === "center" ? "text-center" : "text-left",
        className
      )}
    >
      <h2 className="text-4xl font-medium tracking-tight">
        {title}
      </h2>

      {subtitle && (
        <p className="mt-3 text-gray-500 text-lg">
          {subtitle}
        </p>
      )}
    </div>
  );
}