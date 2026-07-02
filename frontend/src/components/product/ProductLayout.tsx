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
    <div className="grid gap-16 lg:grid-cols-2">

      <div>
        {gallery}
      </div>

      <div>
        {info}
      </div>

    </div>
  );
}