import Link from "next/link";

const team = [
  {
    name: "Priyam Kumar",
    role: "Team Lead • Backend & AI Engineer",
    email: "priyam.stu@gmail.com",
  },
  {
    name: "Pritam Nayak",
    role: "System Integration Engineer",
    email: "nayakpritam321@gmail.com",
  },
  {
    name: "Somesh Jena",
    role: "Frontend Engineer",
    email: "someshjena014@gmail.com",
  },
  {
    name: "Somanath Kundu",
    role: "UI Engineer",
    email: "kundusomanath918@gmail.com",
  },
];

export default function AboutPage() {
  return (
    <main className="min-h-screen bg-black text-white">
      <div className="mx-auto max-w-7xl px-6 py-16">
        <h1 className="mb-6 text-center text-5xl font-extrabold">
          About <span className="text-purple-500">WATCHTOWER</span>
        </h1>

        <p className="mx-auto mb-16 max-w-4xl text-center text-lg text-gray-400">
          WATCHTOWER is an AI-powered document intelligence platform designed to
          help students, faculty, and institutions search, understand, and
          verify information across institutional documents using semantic
          search, Retrieval-Augmented Generation (RAG), and Google Gemini AI.
        </p>

        <h2 className="mb-8 text-3xl font-bold">Our Team</h2>

        <div className="grid gap-8 md:grid-cols-2">
          {team.map((member) => (
            <div
              key={member.name}
              className="rounded-2xl border border-gray-800 bg-[#111827] p-8 transition duration-300 hover:border-purple-500 hover:shadow-xl hover:shadow-purple-500/20"
            >
              <h3 className="text-2xl font-bold">{member.name}</h3>

              <p className="mt-2 font-medium text-purple-400">
                {member.role}
              </p>

              <p className="mt-5 text-gray-300">
                📧 {member.email}
              </p>
            </div>
          ))}
        </div>

        <div className="mt-20 rounded-2xl border border-gray-800 bg-[#111827] p-10">
          <h2 className="mb-6 text-3xl font-bold">
            Project Information
          </h2>

          <div className="grid gap-8 md:grid-cols-2">
            <div>
              <h3 className="mb-2 font-semibold text-purple-400">
                Project
              </h3>
              <p>WATCHTOWER</p>
            </div>


            <div>
              <h3 className="mb-2 font-semibold text-purple-400">
                Repository
              </h3>

              <Link
                href="https://github.com/surediepie/WATCHTOWER"
                target="_blank"
                className="text-blue-400 hover:underline"
              >
                github.com/surediepie/WATCHTOWER
              </Link>
            </div>

            <div>
              <h3 className="mb-2 font-semibold text-purple-400">
                Tech Stack
              </h3>

              <p>
                Next.js • FastAPI • ChromaDB • Sentence Transformers • Gemini AI
                • Tailwind CSS
              </p>
            </div>
          </div>
        </div>

        <div className="mt-20 rounded-2xl border border-purple-700 bg-purple-900/10 p-10">
          <h2 className="mb-4 text-3xl font-bold">
            Our Mission
          </h2>

          <p className="text-lg leading-8 text-gray-300">
            WATCHTOWER empowers students and institutions with trustworthy,
            AI-powered access to institutional knowledge through intelligent
            document search, semantic retrieval, and citation-backed responses.
          </p>
        </div>
      </div>
    </main>
  );
}