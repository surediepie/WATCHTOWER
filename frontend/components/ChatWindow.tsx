"use client";

import { useState } from "react";

interface Source {
  text: string;
  source: string;
  distance: number;
}

interface Message {
  role: "user" | "assistant";
  text: string;
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
        "http://127.0.0.1:8000/chat",
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
          text: data.answer,
          sources: data.sources,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Unable to get a response.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-2xl border border-gray-800 bg-[#111827] p-6">
      <h2 className="mb-4 text-xl font-semibold text-white">
        AI Assistant
      </h2>

      <div className="mb-4 h-[350px] overflow-y-auto rounded-xl border border-gray-700 bg-[#1F2937] p-4 space-y-3">
        {messages.length === 0 ? (
          <p className="text-gray-400">
            Your conversation will appear here.
          </p>
        ) : (
          messages.map((msg, index) => (
            <div
              key={index}
              className={
                msg.role === "user"
                  ? "text-right"
                  : "text-left"
              }
            >
              <div
                className={
                  msg.role === "user"
                    ? "inline-block rounded-lg bg-purple-600 px-4 py-2 text-white"
                    : "inline-block rounded-lg bg-gray-700 px-4 py-2 text-white"
                }
              >
                {msg.text}
              </div>
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
          onChange={(e) => setQuestion(e.target.value)}
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
          className="rounded-lg bg-purple-600 px-6 py-3 font-medium text-white hover:bg-purple-700"
        >
          Send
        </button>
      </div>
    </div>
  );
}