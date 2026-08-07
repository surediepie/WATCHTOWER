import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between px-10 py-6">
      {/* Logo */}
      <h1 className="text-xl font-bold tracking-[0.3em] text-white">
        WATCHTOWER
      </h1>

      {/* Navigation */}
      <div className="flex items-center gap-10 text-sm uppercase tracking-widest text-gray-300">
        <Link href="/">Home</Link>
        <Link href="https://github.com/surediepie/WATCHTOWER" target="_blank">
          GitHub
        </Link>
        <Link href="/about">About Us</Link>
      </div>

      {/* Sign Up */}
      <Link
  href="/login"
  className="rounded-full border border-purple-500/40 bg-purple-500/10 px-6 py-2 text-sm text-white transition hover:bg-purple-500/20"
>
  Sign Up
</Link>
    </nav>
  );
}