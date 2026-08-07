"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

export default function Navbar() {
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    setLoggedIn(!!token);
  }, []);

  function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    window.location.href = "/";
  }

  return (
    <nav className="flex items-center justify-between border-b border-gray-800 px-10 py-6">
      {/* Logo */}
      <Link
        href="/"
        className="text-2xl font-bold tracking-widest text-white"
      >
        WATCHTOWER
      </Link>

      {/* Navigation */}
      <div className="flex items-center gap-10 text-sm uppercase tracking-widest text-gray-300">
        <Link href="/">Home</Link>

        <Link
          href="https://github.com/surediepie/WATCHTOWER"
          target="_blank"
        >
          GitHub
        </Link>

        <Link href="/about">
          About Us
        </Link>
      </div>

      {/* Auth Buttons */}
      {loggedIn ? (
        <div className="flex items-center gap-4">
          <Link
            href="/dashboard"
            className="rounded-full bg-purple-600 px-6 py-2 text-white transition hover:bg-purple-700"
          >
            Dashboard
          </Link>

          <button
            onClick={logout}
            className="rounded-full border border-red-500 px-6 py-2 text-red-400 transition hover:bg-red-500/10"
          >
            Logout
          </button>
        </div>
      ) : (
        <div className="flex items-center gap-3">
          <Link
            href="/login"
            className="rounded-full border border-gray-600 px-6 py-2 text-white transition hover:bg-gray-800"
          >
            Sign In
          </Link>

          <Link
            href="/register"
            className="rounded-full bg-purple-600 px-6 py-2 text-white transition hover:bg-purple-700"
          >
            Create Account
          </Link>
        </div>
      )}
    </nav>
  );
}