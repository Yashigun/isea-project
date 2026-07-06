import Container from "@/components/layout/Container";

export default function ContactPage() {
  return (
    <main>

      {/* Header */}

      <section className="pb-16 pt-24">

        <Container>

          <div className="max-w-3xl">

            <p className="mb-5 text-lg">
              Questions • <span className="text-[#ac142a]">Custom Orders</span> • Hello
            </p>

            <h1 className="text-5xl font-light leading-tight md:text-7xl">

              We'd love to

              <br />

              hear from <span className="text-[#657ab1]">you.</span>

            </h1>

            <p className="mt-8 max-w-xl text-lg leading-8 text-gray-600">
              Have a question about an order, a product or something you'd like
              made especially for you? Send us a message.
            </p>

          </div>

        </Container>

      </section>



      {/* Contact */}

      <section className="pb-28">

        <Container>

          <div className="grid gap-16 lg:grid-cols-[1fr_1.5fr]">

            {/* Contact Information */}

            <div>

              <div className="rounded-[30px] bg-[#f7f3ed] p-10">

                <p className="text-sm uppercase tracking-[0.3em] text-gray-500">
                  Contact
                </p>


                <div className="mt-10 space-y-8">

                  <div>

                    <p className="text-sm text-gray-500">
                      Email
                    </p>

                    <p className="mt-2 text-lg">
                      shopvimsical@gmail.com
                    </p>

                  </div>


                  <div>

                    <p className="text-sm text-gray-500">
                      Instagram
                    </p>

                    <p className="mt-2 text-lg">
                      <a href="https://www.instagram.com/shop.vimsy/?hl=en" target="_blank" rel="noopener noreferrer" className="underline">
                        @shop.vimsy
                      </a>
                    </p>

                  </div>


                  <div>

                    <p className="text-sm text-gray-500">
                      Response Time
                    </p>

                    <p className="mt-2 text-lg">
                      Usually within 1–2 business days.
                    </p>

                  </div>

                </div>

              </div>


              <div className="mt-8 rounded-[30px] bg-[#e5ecd9] p-10">

                <span className="text-4xl">
                  ✿
                </span>

                <h3 className="mt-6 text-2xl">
                  Custom crochet requests
                </h3>

                <p className="mt-4 leading-7 text-gray-600">
                  Looking for something unique? Tell us your idea, preferred
                  colors and size and we'll see what we can create.
                </p>

              </div>

            </div>



            {/* Form */}

            <form className="rounded-[40px] border border-gray-200 p-8 md:p-12">

              <div className="grid gap-8 md:grid-cols-2">

                <div>

                  <label className="text-sm text-gray-600">
                    First Name
                  </label>

                  <input
                    type="text"
                    placeholder="Your first name"
                    className="
                      mt-3
                      w-full
                      border-b
                      border-gray-300
                      bg-transparent
                      py-3
                      outline-none
                      transition-colors
                      duration-300
                      focus:border-black
                    "
                  />

                </div>


                <div>

                  <label className="text-sm text-gray-600">
                    Last Name
                  </label>

                  <input
                    type="text"
                    placeholder="Your last name"
                    className="
                      mt-3
                      w-full
                      border-b
                      border-gray-300
                      bg-transparent
                      py-3
                      outline-none
                      transition-colors
                      duration-300
                      focus:border-black
                    "
                  />

                </div>

              </div>


              <div className="mt-10">

                <label className="text-sm text-gray-600">
                  Email
                </label>

                <input
                  type="email"
                  placeholder="you@example.com"
                  className="
                    mt-3
                    w-full
                    border-b
                    border-gray-300
                    bg-transparent
                    py-3
                    outline-none
                    transition-colors
                    duration-300
                    focus:border-black
                  "
                />

              </div>


              <div className="mt-10">

                <label className="text-sm text-gray-600">
                  Subject
                </label>

                <select
                  className="
                    mt-3
                    w-full
                    border-b
                    border-gray-300
                    bg-transparent
                    py-3
                    outline-none
                    transition-colors
                    duration-300
                    focus:border-black
                  "
                >

                  <option>General Question</option>

                  <option>Order Question</option>

                  <option>Custom Crochet Request</option>

                  <option>Collaboration</option>

                </select>

              </div>


              <div className="mt-10">

                <label className="text-sm text-gray-600">
                  Message
                </label>

                <textarea
                  rows={6}
                  placeholder="Tell us what's on your mind..."
                  className="
                    mt-3
                    w-full
                    resize-none
                    rounded-[20px]
                    border
                    border-gray-300
                    p-5
                    outline-none
                    transition-colors
                    duration-300
                    focus:border-black
                  "
                />

              </div>


              <button
                type="submit"
                className="
                  mt-10
                  rounded-full
                  bg-black
                  px-10
                  py-4
                  text-white
                  transition-all
                  duration-300
                  hover:-translate-y-1
                  hover:bg-[#ac142a]
                "
              >
                Send Message
              </button>

            </form>

          </div>

        </Container>

      </section>

    </main>
  );
}