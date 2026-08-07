"use client";

import { Upload } from "lucide-react";
import { useState } from "react";

export default function UploadButton() {
  const [uploading, setUploading] = useState(false);

  async function handleUpload(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const file = event.target.files?.[0];

    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploading(true);

      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      console.log(data);

      if (!response.ok) {
        throw new Error(JSON.stringify(data));
      }

      alert("✅ PDF uploaded successfully!");
    } catch (error) {
      console.error(error);
      alert("❌ Upload failed.");
    } finally {
      setUploading(false);
    }
  }

  return (
    <label className="inline-flex cursor-pointer items-center gap-3 rounded-xl bg-purple-600 px-5 py-3 font-medium text-white transition hover:bg-purple-700">
      <Upload size={20} />
      {uploading ? "Uploading..." : "Upload PDF"}

      <input
        type="file"
        accept=".pdf"
        className="hidden"
        onChange={handleUpload}
      />
    </label>
  );
}