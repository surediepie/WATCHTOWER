import Image from "next/image";
import Link from "next/link";

export default function Hero() {
  return (
    <section className="mx-auto flex min-h-[90vh] max-w-7xl flex-col items-center justify-center gap-12 px-6 lg:flex-row lg:justify-between">
      {/* Left */}
      <div className="max-w-2xl">
        <h1 className="text-6xl font-extrabold leading-tight text-white">
          Every Answer
          <br />
          <span className="text-purple-500">Verified</span>
          <br />
          Every Source
          <br />
          Within Reach
        </h1>

        <p className="mt-8 text-lg text-gray-400">
          Search, understand, and verify institutional documents with
          confidence.
        </p>

        <div className="mt-10 flex gap-4">
          <Link
            href="/register"
            className="rounded-full bg-purple-600 px-8 py-3 font-semibold text-white transition hover:bg-purple-700"
          >
            Create Account
          </Link>

          <Link
            href="/login"
            className="rounded-full border border-gray-600 px-8 py-3 font-semibold text-white transition hover:bg-gray-800"
          >
            Sign In
          </Link>
        </div>
      </div>

      {/* Right */}
      <div className="flex shrink-0 items-center justify-center">
        <div className="flex h-[400px] w-[400px] items-center justify-center rounded-2xl border border-gray-700 bg-[#111827] shadow-2xl lg:h-[500px] lg:w-[500px]">
          <Image
            src="/WATCHTOWER_logo.jpg"
            alt="WATCHTOWER Logo"
            width={420}
            height={420}
            priority
            className="object-contain"
          />
        </div>
      </div>
    </section>
  );
}