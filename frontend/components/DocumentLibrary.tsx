"use client";

import { useEffect, useState } from "react";
import { FileText, Trash2 } from "lucide-react";

interface Document {
  id: number;
  name: string;
  size: number;
}

export default function DocumentLibrary() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);

  async function loadDocuments() {
    try {
      const token = localStorage.getItem("access_token");

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/documents`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        console.error(data);
        setDocuments([]);
        return;
      }

      setDocuments(data);
    } catch (error) {
      console.error(error);
      setDocuments([]);
    } finally {
      setLoading(false);
    }
  }

  async function deleteDocument(id: number) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this document?"
    );

    if (!confirmed) return;

    try {
      const token = localStorage.getItem("access_token");

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/documents/${id}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Delete failed");
      }

      setDocuments((prev) =>
        prev.filter((doc) => doc.id !== id)
      );
    } catch (error) {
      console.error(error);
      alert("Failed to delete document.");
    }
  }

  useEffect(() => {
  // eslint-disable-next-line react-hooks/set-state-in-effect
  loadDocuments();
}, []);

  return (
    <div>
      <h2 className="mb-4 text-xl font-semibold text-white">
        Uploaded Documents
      </h2>

      {loading ? (
        <p className="text-gray-400">
          Loading...
        </p>
      ) : documents.length === 0 ? (
        <p className="text-gray-400">
          No documents uploaded yet.
        </p>
      ) : (
        <div className="space-y-4">
          {documents.map((doc) => (
            <div
              key={doc.id}
              className="flex items-center justify-between rounded-xl bg-[#1F2937] p-4"
            >
              <div className="flex items-center gap-4">
                <FileText
                  size={22}
                  className="text-purple-500"
                />

                <div>
                  <h3 className="font-medium text-white">
                    {doc.name}
                  </h3>

                  <p className="text-sm text-gray-400">
                    {doc.size} KB
                  </p>
                </div>
              </div>

              <button
                onClick={() => deleteDocument(doc.id)}
                className="rounded-lg p-2 text-red-500 transition hover:bg-red-500/10 hover:text-red-400"
                title="Delete document"
              >
                <Trash2 size={20} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}