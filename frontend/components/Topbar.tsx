import { Bell } from "lucide-react";
import SearchBar from "./SearchBar";

export default function Topbar() {
  return (
    <header className="flex items-center justify-between border-b border-gray-800 p-6">
      <div className="w-[450px]">
        <SearchBar />
      </div>

      <div className="flex items-center gap-5">
        <Bell className="cursor-pointer text-gray-400 hover:text-white" />

        <div className="flex h-11 w-11 items-center justify-center rounded-full bg-purple-600 font-bold">
          S
        </div>
      </div>
    </header>
  );
}