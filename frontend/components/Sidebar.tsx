import Link from "next/link";
import {
  LayoutDashboard,
  FolderOpen,
  MessageSquare,
  History,
  Settings,
  User,
} from "lucide-react";

export default function Sidebar() {
  return (
    <aside className="flex h-screen w-64 flex-col justify-between border-r border-gray-800 bg-[#0F172A] p-6">
      <div>
        <h1 className="mb-10 text-2xl font-bold tracking-widest text-white">
          WATCHTOWER
        </h1>

        <nav className="space-y-4">
          <Link
            href="/dashboard"
            className="flex items-center gap-3 rounded-lg p-3 text-gray-300 hover:bg-gray-800"
          >
            <LayoutDashboard size={20} />
            Dashboard
          </Link>

          <Link
            href="#"
            className="flex items-center gap-3 rounded-lg p-3 text-gray-300 hover:bg-gray-800"
          >
            <FolderOpen size={20} />
            Documents
          </Link>

          <Link
            href="#"
            className="flex items-center gap-3 rounded-lg p-3 text-gray-300 hover:bg-gray-800"
          >
            <MessageSquare size={20} />
            Chat
          </Link>

          <Link
            href="#"
            className="flex items-center gap-3 rounded-lg p-3 text-gray-300 hover:bg-gray-800"
          >
            <History size={20} />
            History
          </Link>

          <Link
            href="#"
            className="flex items-center gap-3 rounded-lg p-3 text-gray-300 hover:bg-gray-800"
          >
            <Settings size={20} />
            Settings
          </Link>
        </nav>
      </div>

      <div className="flex items-center gap-3 rounded-lg border border-gray-700 p-3">
        <User size={20} />
        <span>User</span>
      </div>
    </aside>
  );
}