import Image from "next/image";

import Container from "./layout/Container";

export default function Hero() {
  return (
    <section className="pb-20 pt-10">

      <Container>

        <div className="grid items-center gap-16 lg:grid-cols-2">

          {/* Left */}

          <div>

            <p className="mb-4 text-lg">
              Handmade • Cute • Minimal
            </p>

            <h1 className="text-6xl font-light leading-tight">

              Made with love,

              <br />

              crafted for

              <br />

              everyday joy.

            </h1>

            <p className="mt-8 max-w-lg text-lg text-gray-600">

              Discover handcrafted products designed to
              bring warmth, charm and personality to your
              everyday life.

            </p>

            <button
              className="
                mt-10
                rounded-full
                border
                border-black
                px-8
                py-3
                transition
                duration-300
                hover:bg-black
                hover:text-white
              "
            >
              Shop Collection
            </button>

          </div>

          {/* Right */}

          <div className="overflow-hidden rounded-[40px]">

            <Image
              src="/images/hero.jpg"
              alt="Hero"
              width={900}
              height={900}
              priority
              className="aspect-square w-full object-cover"
            />

          </div>

        </div>

      </Container>

    </section>
  );
}