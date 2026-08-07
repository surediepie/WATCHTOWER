"use client";

import { useState } from "react";
import CitationPanel from "./CitationPanel";

interface Source {
  text: string;
  source: string;
  page: number;
  distance: number;
}

interface Message {
  role: "user" | "assistant";
  text?: string;
  documentAnswer?: string;
  aiAnswer?: string;
  sources?: Source[];
}

export default function ChatWindow() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  async function sendQuestion() {
    if (!question.trim()) return;

    const userQuestion = question;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text: userQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const token = localStorage.getItem("access_token");

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            question: userQuestion,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Chat failed");
      }

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          documentAnswer: data.document_answer,
          aiAnswer: data.ai_answer,
          sources: data.sources,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          documentAnswer: "Unable to retrieve document information.",
          aiAnswer: "Unable to connect to the AI service.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h2 className="mb-4 text-xl font-semibold text-white">
        AI Assistant
      </h2>

      <div className="mb-4 h-[500px] overflow-y-auto rounded-xl border border-gray-700 bg-[#1F2937] p-4 space-y-6">

        {messages.length === 0 ? (
          <p className="text-gray-400">
            Your conversation will appear here.
          </p>
        ) : (
          messages.map((msg, index) => (
            <div key={index}>
              {msg.role === "user" ? (
                <div className="text-right">
                  <div className="inline-block max-w-[85%] rounded-lg bg-purple-600 px-4 py-3 text-white">
                    {msg.text}
                  </div>
                </div>
              ) : (
                <div className="rounded-xl bg-gray-800 p-6 space-y-6 border border-gray-700">

                  <div>
  <h3 className="mb-3 text-lg font-semibold text-purple-400">
    📄 From Uploaded Documents
  </h3>

  <div className="rounded-lg bg-gray-700 p-4 whitespace-pre-wrap text-gray-100">
    {msg.documentAnswer ?? (
      <span className="text-yellow-300">
        No relevant information was found in the uploaded documents.
      </span>
    )}
  </div>
</div>

                  {msg.sources &&
                    msg.sources.length > 0 && (
                      <div>
                        <h3 className="mb-3 text-lg font-semibold text-purple-400">
                          📚 Citations
                        </h3>

                        <CitationPanel
                          sources={msg.sources}
                        />
                      </div>
                    )}

                  <div>
                    <h3 className="mb-3 text-lg font-semibold text-purple-400">
                      💡 AI Explanation
                    </h3>

                    <div className="rounded-lg bg-gray-700 p-4 whitespace-pre-wrap text-gray-100">
                      {msg.aiAnswer}
                    </div>
                  </div>

                </div>
              )}
            </div>
          ))
        )}

        {loading && (
          <p className="text-gray-400">
            Thinking...
          </p>
        )}
      </div>

      <div className="flex gap-3">
        <input
          type="text"
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendQuestion();
            }
          }}
          placeholder="Ask anything..."
          className="flex-1 rounded-lg border border-gray-700 bg-[#0F172A] px-4 py-3 text-white outline-none"
        />

        <button
          onClick={sendQuestion}
          disabled={loading}
          className="rounded-lg bg-purple-600 px-6 py-3 font-medium text-white transition hover:bg-purple-700 disabled:opacity-50"
        >
          {loading ? "Thinking..." : "Send"}
        </button>
      </div>
    </div>
  );
}