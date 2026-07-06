import Image from "next/image";
import Link from "next/link";
import Container from "@/components/layout/Container";





export default function AboutPage() {
  return (
    <main>

      {/* Hero */}

      <section className="py-24">

        <Container>

          <div className="grid items-center gap-16 lg:grid-cols-2">

            <div>

              <p className="mb-5 text-lg">
                Handmade • <span className="text-[#657ab1]">Thoughtful</span> • Personal
              </p>

              <h1 className="text-5xl font-light leading-tight md:text-7xl">

                Little things,

                <br />

                made with <span className="text-[#ac142a]">love.</span>

              </h1>

              <p className="mt-8 max-w-xl text-lg leading-8 text-gray-600">

                We create handmade crochet pieces designed to bring warmth,
                comfort and a little more joy into everyday life.

                Every piece is carefully crafted, one stitch at a time.

              </p>

            </div>


            <div className="overflow-hidden rounded-[40px]">

              <Image
                src="/images/about.png"
                alt="Handmade crochet products"
                width={800}
                height={1000}
                className="w-full object-cover"
              />

            </div>

          </div>

        </Container>

      </section>



      {/* Story */}

      <section className="bg-[#fff1ea] py-24">

        <Container>

          <div className="mx-auto max-w-3xl text-center">

            <p className="mb-5 text-sm uppercase tracking-[0.3em] text-gray-500">
              Our Story
            </p>

            <h2 className="text-4xl font-light leading-tight md:text-5xl">

              From a simple thread

              <br />

              to something <span className="text-[#8da86c]">special.</span>

            </h2>

            <p className="mt-8 text-lg leading-8 text-gray-600">

              What started as a love for creating small handmade pieces slowly
              became a collection of products made to be shared.

              From cozy accessories to thoughtful gifts, each creation carries
              the time, patience and personality that makes handmade products
              truly unique.

            </p>

          </div>

        </Container>

      </section>



      {/* Values */}

      <section className="py-24">

        <Container>

          <div className="mb-14">

            <p className="mb-4 text-sm uppercase tracking-[0.3em] text-gray-500">
              What Matters To Us
            </p>

            <h2 className="text-4xl font-light md:text-5xl">
              Made differently.
            </h2>

          </div>


          <div className="grid gap-8 md:grid-cols-3">

            <div className="rounded-[30px] bg-[#f4d9dc] p-10">

              <span className="text-4xl">♡</span>

              <h3 className="mt-8 text-2xl">
                Handmade with care
              </h3>

              <p className="mt-4 leading-7 text-gray-600">
                Every product is thoughtfully crafted by hand instead of being
                mass produced.
              </p>

            </div>


            <div className="rounded-[30px] bg-[#e5ecd9] p-10">

              <span className="text-4xl">✿</span>

              <h3 className="mt-8 text-2xl">
                Made to bring joy
              </h3>

              <p className="mt-4 leading-7 text-gray-600">
                Our creations are designed to add warmth, personality and charm
                to everyday moments.
              </p>

            </div>


            <div className="rounded-[30px] bg-[#dde3f3] p-10">

              <span className="text-4xl">☼</span>

              <h3 className="mt-8 text-2xl">
                Thoughtfully created
              </h3>

              <p className="mt-4 leading-7 text-gray-600">
                From choosing colors to packaging orders, every small detail is
                carefully considered.
              </p>

            </div>

          </div>

        </Container>

      </section>



      {/* Closing */}

      <section className="pb-28 pt-16">

        <Container>

          <div className="relative overflow-hidden rounded-[40px] px-8 py-20 text-center text-white">

            {/* Background Image */}

            <Image
              src="/images/handmade.png"
              alt=""
              fill
              className="object-cover"
            />


            {/* Content */}

            <div className="relative z-10">

              <p className="text-sm uppercase tracking-[0.3em] text-gray-400">
                Handmade for you
              </p>

              <h2 className="mx-auto mt-6 max-w-3xl text-4xl font-light leading-tight md:text-6xl">

                Small stitches.

                <br />

                Big <span className="text-[#f1a7b0]">feelings.</span>

              </h2>

              <p className="mx-auto mt-6 max-w-xl text-lg text-gray-400">
                Discover handmade crochet pieces created to make everyday moments
                feel a little more special.
              </p>

              <Link href="/">
                <button
                  className="
                    mt-10
                    rounded-full
                    bg-white
                    px-8
                    py-3
                    text-black
                    transition-colors
                    duration-300
                    hover:bg-[#f1a7b0]
                  "
                >
                  Explore Collection
                </button>
              </Link>

            </div>

          </div>

        </Container>

      </section>

    </main>
  );
}