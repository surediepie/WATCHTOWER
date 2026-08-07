import { FileText, Search, ShieldCheck } from "lucide-react";

export default function Features() {
  const features = [
    {
      icon: <FileText size={28} />,
      title: "Upload Documents",
      description:
        "Upload institutional documents securely and organize them in one place.",
    },
    {
      icon: <Search size={28} />,
      title: "Ask Anything",
      description:
        "Search documents using natural language instead of manually reading PDFs.",
    },
    {
      icon: <ShieldCheck size={28} />,
      title: "Verified Answers",
      description:
        "Every response includes citations so users can verify the information themselves.",
    },
  ];

  return (
    <section className="px-10 py-24">
      <h2 className="mb-12 text-center text-4xl font-bold text-white">
        Why WATCHTOWER?
      </h2>

      <div className="grid gap-8 md:grid-cols-3">
        {features.map((feature, index) => (
          <div
            key={index}
            className="rounded-2xl border border-gray-700 bg-[#111827] p-8"
          >
            <div className="mb-5 text-purple-500">{feature.icon}</div>

            <h3 className="mb-3 text-xl font-semibold text-white">
              {feature.title}
            </h3>

            <p className="text-gray-400">
              {feature.description}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}