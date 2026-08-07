import { Search } from "lucide-react";

export default function SearchBar() {
  return (
    <div className="relative w-full">
      <Search
        className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500"
        size={18}
      />

      <input
        type="text"
        placeholder="Search documents..."
        className="w-full rounded-xl bg-[#1F2937] py-3 pl-12 pr-4 text-white outline-none border border-gray-700"
      />
    </div>
  );
}