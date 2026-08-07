import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import Features from "@/components/Features";

export default function Home() {
  return (
    <main className="relative min-h-screen bg-[#0B0F19] overflow-hidden">
      <div className="hero-bg" />

      <Navbar />
      <Hero />
      <Features />
    </main>
  );
}