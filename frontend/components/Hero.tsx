export default function Hero() {
  return (
    <section className="flex min-h-[85vh] items-center justify-between px-10">
      {/* Left */}
      <div className="max-w-xl">
        <h1 className="text-6xl font-extrabold uppercase leading-tight text-white">
          Every Answer
          <br />
          Verified
          <br />
          Every Source
          <br />
          Within Reach
        </h1>

        <p className="mt-8 text-lg text-gray-400">
          Search, understand, and verify institutional documents with confidence.
        </p>

        <button className="mt-8 rounded-full bg-purple-600 px-8 py-3 text-white transition hover:bg-purple-700">
          Get Started
        </button>
      </div>

      {/* Right */}
      <div className="flex items-center justify-center">
        <div className="h-[500px] w-[500px] rounded-2xl border border-gray-700 bg-[#111827] shadow-2xl">
          {/* Logo/Image goes here */}
        </div>
      </div>
    </section>
  );
}