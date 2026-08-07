"use client";

import { Bell } from "lucide-react";
import SearchBar from "./SearchBar";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

interface User {
  id: number;
  name: string;
  email: string;
}

export default function Topbar() {
  const router = useRouter();

  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");

    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  function handleLogout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");

    router.push("/");
  }

  return (
    <header className="flex items-center justify-between border-b border-gray-800 bg-[#111827] px-8 py-5">
      <div>
        <h2 className="text-2xl font-bold text-white">
          Dashboard
        </h2>

        <p className="text-sm text-gray-400">
          Welcome back{user ? `, ${user.name}` : ""}.
        </p>
      </div>

      <SearchBar />

      <div className="flex items-center gap-5">
        <Bell
          className="cursor-pointer text-gray-400 hover:text-white"
          size={22}
        />

        <div className="flex h-11 w-11 items-center justify-center rounded-full bg-purple-600 font-bold text-white">
          {user?.name?.charAt(0).toUpperCase() || "U"}
        </div>

        <button
          onClick={handleLogout}
          className="rounded-lg border border-red-500 px-4 py-2 text-sm font-medium text-red-400 transition hover:bg-red-500/10"
        >
          Logout
        </button>
      </div>
    </header>
  );
}