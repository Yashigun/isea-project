import Image from "next/image";

import Container from "./layout/Container";

export default function Hero() {
  return (
    <section className="relative overflow-hidden pb-20 pt-10">

      {/* Background Hero Image */}
      <Image
        src="/images/hero.png"
        alt="Hero"
        fill
        priority
        className="object-cover"
      />

      {/* Content */}
      <div className="relative z-10">

        <Container>

          <div className="grid items-center gap-16 lg:grid-cols-2">

            {/* Left */}

            <div>

              <p className="mb-4 text-lg">
                Handmade • <span className="text-[#657ab1]">Cute</span> • Minimal
              </p>

              <h1 className="text-6xl font-light leading-tight">

                Made with <span className="text-[#ac142a]">Love</span>,

                <br />

                <span className="text-[#8da86c]">crafted</span> for

                <br />

                everyday <span className="text-[#031d8c]">joy</span>.

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

          </div>

        </Container>

      </div>

    </section>
  );
}