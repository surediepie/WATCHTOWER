export default function LoginPage() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-[#0B0F19]">
      <div className="w-full max-w-md rounded-2xl border border-gray-700 bg-[#111827] p-8">
        <h1 className="text-3xl font-bold text-white text-center">
          Welcome Back
        </h1>

        <p className="mt-2 text-center text-gray-400">
          Sign in to continue to WATCHTOWER
        </p>

        <form className="mt-8 space-y-5">
          <input
            type="email"
            placeholder="Email"
            className="w-full rounded-lg bg-[#1F2937] p-3 text-white outline-none"
          />

          <input
            type="password"
            placeholder="Password"
            className="w-full rounded-lg bg-[#1F2937] p-3 text-white outline-none"
          />

          <button className="w-full rounded-lg bg-purple-600 py-3 font-semibold text-white hover:bg-purple-700">
            Sign In
          </button>
        </form>
      </div>
    </main>
  );
}