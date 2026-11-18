
"use client";

import { useRouter } from "next/navigation";
import {
  BriefcaseBusiness,
  UsersRound,
  Volume2,
  Hotel,
  Sparkles,
} from "lucide-react";

export default function HomePage() {
  const router = useRouter();

  const speak = () => {
    if (!("speechSynthesis" in window)) return;

    window.speechSynthesis.cancel();

    const message = new SpeechSynthesisUtterance(
      "Are you looking for a job, or looking for workers?"
    );

    message.lang = "en-US";
    message.rate = 0.85;

    window.speechSynthesis.speak(message);
  };

  return (
    <main className="min-h-dvh bg-gradient-to-br from-sky-500 via-blue-600 to-blue-900 px-5 py-8 text-white">
      <div className="mx-auto flex min-h-[calc(100dvh-4rem)] max-w-lg flex-col">
        <header className="flex justify-end">
          <button
            type="button"
            onClick={speak}
            aria-label="Listen to options"
            className="rounded-full border border-white/40 bg-white/15 p-4 transition hover:bg-white/25"
          >
            <Volume2 size={28} />
          </button>
        </header>

        <section className="flex flex-1 flex-col justify-center">
          <div className="mb-12 text-center">
            <div className="mb-5 flex justify-center">
              <div className="relative">
                <Hotel size={76} strokeWidth={1.5} />
                <Sparkles
                  size={25}
                  className="absolute -right-6 top-0 text-sky-200"
                />
              </div>
            </div>

            <h1 className="text-3xl font-bold tracking-tight">
              Welcome!
            </h1>

            <p className="mt-2 text-lg text-blue-100">
              What are you looking for?
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <button
              type="button"
              onClick={() => router.push("/worker")}
              className="flex min-h-64 flex-col items-center justify-center gap-6 rounded-3xl bg-white p-5 text-blue-800 shadow-xl transition active:scale-95"
            >
              <div className="rounded-3xl bg-sky-100 p-6">
                <BriefcaseBusiness
                  size={65}
                  strokeWidth={1.5}
                />
              </div>

              <span className="text-center text-xl font-bold">
                Find a Job
              </span>
            </button>

            <button
              type="button"
              onClick={() => router.push("/employer")}
              className="flex min-h-64 flex-col items-center justify-center gap-6 rounded-3xl bg-white p-5 text-blue-800 shadow-xl transition active:scale-95"
            >
              <div className="rounded-3xl bg-sky-100 p-6">
                <UsersRound
                  size={65}
                  strokeWidth={1.5}
                />
              </div>

              <span className="text-center text-xl font-bold">
                Find Workers
              </span>
            </button>
          </div>
        </section>

        <footer className="pt-10 text-center text-sm text-blue-100">
          Hospitality jobs made simple
        </footer>
      </div>
    </main>
  );
}
