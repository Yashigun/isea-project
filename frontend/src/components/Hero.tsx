import Image from "next/image";

import Container from "./layout/Container";

export default function Hero() {
  return (
    <section className="relative h-[450px] w-[100%] overflow-hidden pb-0 pt-0 sm:h-auto sm:pb-14 sm:pt-8 md:pb-16 md:pt-10 lg:pb-20">

      {/* Mobile Background Hero Image */}
      <Image
        src="/images/vimsy.png"
        alt="Hero"
        fill
        priority
        className="object-cover sm:hidden"
      />

      {/* Background Hero Image */}
      <Image
        src="/images/hero.png"
        alt="Hero"
        fill
        priority
        className="hidden object-cover sm:block"
      />

      {/* Content */}
      <div className="relative z-10 hidden sm:block">

        <Container>

          <div className="grid items-center gap-8 sm:gap-10 md:gap-12 lg:grid-cols-2 lg:gap-16">

            {/* Left */}

            <div>

              <p className="mb-3 text-sm sm:mb-4 sm:text-base md:text-lg">
                Handmade • <span className="text-[#657ab1]">Cute</span> • Minimal
              </p>

              <h1 className="text-4xl font-light leading-tight sm:text-5xl md:text-6xl">

                Made with <span className="text-[#ac142a]">Love</span>,

                <br />

                <span className="text-[#8da86c]">crafted</span> for

                <br />

                everyday <span className="text-[#031d8c]">joy</span>.

              </h1>

              <p className="mt-5 max-w-lg text-sm text-gray-600 sm:mt-6 sm:text-base md:mt-8 md:text-lg">

                Discover handcrafted products designed to
                bring warmth, charm and personality to your
                everyday life.

              </p>

              <button
                className="
                  mt-6
                  rounded-full
                  border
                  border-black
                  px-6
                  py-2.5
                  text-sm
                  transition
                  duration-300
                  hover:bg-black
                  hover:text-white
                  sm:mt-8
                  sm:px-7
                  sm:py-3
                  sm:text-base
                  lg:mt-10
                  lg:px-8
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
