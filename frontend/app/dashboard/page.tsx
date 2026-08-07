import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import DocumentLibrary from "@/components/DocumentLibrary";
import ChatWindow from "@/components/ChatWindow";
import UploadButton from "@/components/UploadButton";

export default function Dashboard() {
  return (
    <main className="flex min-h-screen bg-[#0B0F19] text-white">
      <Sidebar />

      <section className="flex-1">
        <Topbar />

        <div className="p-8">
          <div className="mb-8 flex items-center justify-between">
  <h1 className="text-4xl font-bold">
    Dashboard
  </h1>

  <UploadButton />
</div>

          <div className="grid grid-cols-3 gap-8">
            <div className="col-span-1">
              <DocumentLibrary />
            </div>

            <div className="col-span-2">
              <ChatWindow /> 
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}