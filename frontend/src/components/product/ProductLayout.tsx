import { ReactNode } from "react";

interface ProductLayoutProps {
  gallery: ReactNode;
  info: ReactNode;
}

export default function ProductLayout({
  gallery,
  info,
}: ProductLayoutProps) {
  return (
    <div className="grid gap-8 sm:gap-12 lg:grid-cols-2 lg:gap-16">

      <div>
        {gallery}
      </div>

      <div>
        {info}
      </div>

    </div>
  );
}
