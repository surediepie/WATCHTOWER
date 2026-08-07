"use client";

import { useEffect, useState } from "react";
import { FileText, MoreVertical } from "lucide-react";

interface Document {
  name: string;
  size: number;
}

export default function DocumentLibrary() {
  const [documents, setDocuments] = useState<Document[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/documents")
      .then((res) => res.json())
      .then((data) => setDocuments(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="rounded-2xl bg-[#111827] p-6">
      <h2 className="mb-6 text-xl font-semibold">
        Uploaded Documents
      </h2>

      {documents.length === 0 ? (
        <p className="text-gray-400">
          No documents uploaded yet.
        </p>
      ) : (
        <div className="space-y-4">
          {documents.map((doc, index) => (
            <div
              key={index}
              className="flex items-center justify-between rounded-xl bg-[#1F2937] p-4"
            >
              <div className="flex items-center gap-4">
                <FileText className="text-purple-500" />

                <div>
                  <h3 className="font-medium text-white">
                    {doc.name}
                  </h3>

                  <p className="text-sm text-gray-400">
                    {doc.size} KB
                  </p>
                </div>
              </div>

              <MoreVertical className="text-gray-400" />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}