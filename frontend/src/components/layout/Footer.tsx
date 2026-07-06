import Link from "next/link";
import Image from "next/image";
import Container from "./Container";

export default function Footer() {
  return (
    <footer className="border-t py-12">

      <Container>

        <div className="grid gap-10 md:grid-cols-3">

          <div>
            <div className="mb-2 flex items-center gap-2">

                <Link href="/" aria-label="Vimsy Home">

                    <Image
                    src="/logo.svg"
                    alt="Vimsy"
                    width={180}
                    height={90}
                    priority
                    className="h-auto w-[150px] lg:w-[180px]"
                    />

                </Link>

            </div>

            <p className="ml-9 text-sm text-muted-foreground">
              Handmade with love.
            </p>

          </div>

          <div>

            <h4 className="mb-4 font-semibold">
              Quick Links
            </h4>

            <div className="flex flex-col gap-2">

              <Link href="/">
                Home
              </Link>

              <Link href="/about">
                About
              </Link>

              <Link href="/contact">
                Contact
              </Link>

            </div>

          </div>

          <div>

            <h4 className="mb-4 font-semibold">
              Contact
            </h4>

            <p className="text-sm text-muted-foreground">
              shopvimsical@gmail.com
            </p>

          </div>

        </div>

      </Container>
    </footer>
  );
}