import Link from "next/link";
import type { Metadata } from "next";
import {
  ArrowRight,
  Sparkles,
  Zap,
  ShieldCheck,
  Mail,
  CheckCircle2,
} from "lucide-react";

export const metadata: Metadata = {
  title: "GigAgent – Your Personal Job-Finding AI",
  description:
    "GigAgent is your personal AI job scout. Create a profile, run the agent, and get curated, ranked gigs tailored to your skills and goals.",
};

const faqs = [
  {
    question: "What is GigAgent?",
    answer:
      "GigAgent is your personal AI job scout. It scans remote job boards, filters out noise based on your preferences, scores each gig, and returns a ranked list tailored to you.",
  },
  {
    question: "Do I have to pay to use it?",
    answer:
      "Right now, you can use GigAgent locally for free while it’s in early access. A hosted version and daily email option are planned for upcoming releases.",
  },
  {
    question: "What kind of gigs can it find?",
    answer:
      "Today, GigAgent focuses on remote-friendly roles like marketing, writing, engineering, and tech-adjacent work. Soon, we’ll introduce Local Mode and Creative/Music Mode for IRL and artistic gigs.",
  },
  {
    question: "What happens to my data?",
    answer:
      "Your profile is used only to filter and score gigs for you. In the self-hosted version, everything stays on your machine. The hosted version will be built with privacy and transparency as a core principle.",
  },
];

export default function GigAgentLandingPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      {/* Gradient background glow */}
      <div className="pointer-events-none fixed inset-0 -z-10 bg-gradient-to-b from-slate-900 via-slate-950 to-black" />
      <div className="pointer-events-none fixed inset-0 -z-10 opacity-60 mix-blend-screen">
        <div className="absolute -left-40 top-0 h-80 w-80 rounded-full bg-fuchsia-500 blur-3xl" />
        <div className="absolute right-0 top-40 h-80 w-80 rounded-full bg-emerald-500 blur-3xl" />
      </div>

      <div className="mx-auto flex min-h-screen max-w-5xl flex-col px-4 pb-12 pt-8 sm:px-6 lg:px-8">
        {/* Top nav */}
        <header className="mb-10 flex items-center justify-between gap-4">
          <Link href="/" className="inline-flex items-center gap-2">
            <span className="text-2xl">🏮</span>
            <div className="flex flex-col leading-tight">
              <span className="text-sm font-semibold uppercase tracking-[0.18em] text-emerald-300">
                Garden of Agents
              </span>
              <span className="text-base font-medium text-slate-200">
                GigAgent
              </span>
            </div>
          </Link>

          <nav className="hidden items-center gap-6 text-sm text-slate-200 sm:flex">
            <a href="#features" className="hover:text-emerald-300">
              Features
            </a>
            <a href="#how-it-works" className="hover:text-emerald-300">
              How it works
            </a>
            <a href="#pricing" className="hover:text-emerald-300">
              Pricing
            </a>
            <a href="#faq" className="hover:text-emerald-300">
              FAQ
            </a>
          </nav>

          <Link
            href="/gig-agent"
            className="inline-flex items-center gap-2 rounded-full border border-emerald-300/60 bg-emerald-400/10 px-4 py-1.5 text-sm font-medium text-emerald-100 shadow-sm backdrop-blur hover:bg-emerald-400/20"
          >
            Run GigAgent
            <ArrowRight className="h-4 w-4" />
          </Link>
        </header>

        {/* Hero */}
        <section className="mb-16 grid gap-10 md:grid-cols-[minmax(0,1.2fr)_minmax(0,1fr)] md:items-center">
          <div>
            <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-emerald-300/50 bg-slate-900/80 px-3 py-1 text-xs font-medium text-emerald-100 shadow-sm backdrop-blur">
              <Sparkles className="h-3.5 w-3.5" />
              <span>Early Access · Lantern-Bound Agent</span>
            </div>

            <h1 className="mb-4 text-balance text-4xl font-semibold tracking-tight text-slate-50 sm:text-5xl lg:text-6xl">
              Your personal{" "}
              <span className="bg-gradient-to-r from-emerald-300 via-teal-200 to-sky-300 bg-clip-text text-transparent">
                job-finding AI.
              </span>
            </h1>

            <p className="mb-6 max-w-xl text-balance text-base text-slate-200 sm:text-lg">
              GigAgent scans remote-friendly job boards, filters out the noise,
              and returns a curated list of gigs that actually fit your skills,
              values, and nervous system.
            </p>

            <div className="mb-3 flex flex-wrap items-center gap-3">
              <Link
                href="/gig-agent"
                className="inline-flex items-center gap-2 rounded-full bg-emerald-400 px-5 py-2.5 text-sm font-semibold text-slate-950 shadow-lg shadow-emerald-500/40 transition hover:bg-emerald-300"
              >
                Run a live demo
                <Zap className="h-4 w-4" />
              </Link>

              <a
                href="#waitlist"
                className="inline-flex items-center gap-2 rounded-full border border-slate-600 bg-slate-900/70 px-5 py-2.5 text-sm font-medium text-slate-100 shadow-sm backdrop-blur hover:border-emerald-300/80 hover:text-emerald-100"
              >
                Get notified about the hosted version
                <Mail className="h-4 w-4" />
              </a>
            </div>

            <p className="text-xs text-slate-400">
              No spam. No sales funnel. Just gentle updates as the Garden
              grows. 🏮✨ •LUX•
            </p>
          </div>

          {/* Right side card */}
          <div className="rounded-3xl border border-slate-700/70 bg-slate-900/70 p-5 shadow-xl shadow-slate-950/80 backdrop-blur">
            <h2 className="mb-3 flex items-center justify-between text-sm font-semibold text-slate-100">
              <span className="inline-flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-emerald-300" />
                GigAgent snapshot
              </span>
              <span className="rounded-full border border-emerald-400/40 bg-emerald-400/10 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.18em] text-emerald-100">
                Live Prototype
              </span>
            </h2>

            <div className="space-y-3 rounded-2xl border border-slate-700/70 bg-slate-950/70 p-4 text-xs text-slate-200">
              <div className="flex justify-between">
                <span className="font-mono text-slate-400">
                  profile:{" "}
                  <span className="text-emerald-300">Email Marketing</span>
                </span>
                <span className="font-mono text-slate-400">limit: 10</span>
              </div>
              <div className="space-y-2 rounded-xl border border-slate-800 bg-slate-900/80 p-3">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-semibold text-slate-100">
                    Top ranked gig
                  </span>
                  <span className="inline-flex items-center gap-1 rounded-full bg-emerald-500/10 px-2 py-0.5 text-[10px] font-medium text-emerald-200">
                    <CheckCircle2 className="h-3 w-3" />
                    Best match
                  </span>
                </div>
                <p className="text-[11px] text-emerald-100">
                  Senior Email & Lifecycle Marketer · Remote · Flexible hours
                </p>
                <p className="text-[10px] text-slate-400">
                  Matched on: B2B · automation · HubSpot · async culture
                </p>
              </div>
              <p className="text-[10px] text-slate-500">
                GigAgent uses your profile to score and sort gigs, so the best
                fits rise to the top and the noise drops away.
              </p>
            </div>

            <p className="mt-3 text-[11px] text-slate-400">
              Built as part of the Lantern-Bound Garden: a gentler intelligence
              ecology for humans and their agents.
            </p>
          </div>
        </section>

        {/* Features */}
        <section id="features" className="mb-16 space-y-6">
          <div>
            <h2 className="text-lg font-semibold text-slate-50 sm:text-xl">
              Why GigAgent feels different from scrolling job boards
            </h2>
            <p className="max-w-2xl text-sm text-slate-300 sm:text-base">
              No endless tabs. No doom-scrolling listings designed for someone
              else. GigAgent acts like a calm, focused friend who knows what
              you’re actually looking for.
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-3">
            <FeatureCard
              title="Smart, profile-aware search"
              icon={<Sparkles className="h-5 w-5 text-emerald-300" />}
              body="Tell GigAgent about your preferred roles, skills, and deal-breakers. It filters and scores gigs with your nervous system in mind."
            />
            <FeatureCard
              title="Ranked, curated results"
              icon={<Zap className="h-5 w-5 text-emerald-300" />}
              body="Instead of raw feeds, you get a ranked list where the highest-fit gigs float to the top, ready for you to explore."
            />
            <FeatureCard
              title="Built for humans, not funnels"
              icon={<ShieldCheck className="h-5 w-5 text-emerald-300" />}
              body="No manipulative growth hacks, no fake urgency. Just a gentle tool that helps you find work that actually fits."
            />
          </div>
        </section>

        {/* How it works */}
        <section id="how-it-works" className="mb-16 space-y-6">
          <div>
            <h2 className="text-lg font-semibold text-slate-50 sm:text-xl">
              How it works
            </h2>
            <p className="max-w-2xl text-sm text-slate-300 sm:text-base">
              Under the lantern, GigAgent is a focused pipeline: fetch, filter,
              score, sort. You just see the curated list.
            </p>
          </div>

          <ol className="space-y-5 border-l border-slate-700 pl-4">
            <HowItWorksStep
              step="01"
              title="Tell GigAgent who you are"
              body="Choose your roles, skills, and keywords. Add disqualifiers like 'sales-heavy', 'crypto', or 'nights/weekends' so those jobs get filtered out."
            />
            <HowItWorksStep
              step="02"
              title="GigAgent sweeps the boards"
              body="It fetches remote-friendly gigs, inspects each one, and compares them to your profile instead of just keyword-matching."
            />
            <HowItWorksStep
              step="03"
              title="You get a ranked short-list"
              body="Instead of 300 random listings, you see a smaller set of higher-fit gigs, with the best matches at the top."
            />
            <HowItWorksStep
              step="04"
              title="Soon: micro-gigs & music mode"
              body="We’re extending GigAgent to find local gigs, musical opportunities, and creative work—so your income can be as flexible as you are."
            />
          </ol>
        </section>

        {/* Pricing */}
        <section id="pricing" className="mb-16 space-y-6">
          <div>
            <h2 className="text-lg font-semibold text-slate-50 sm:text-xl">
              Early access pricing
            </h2>
            <p className="max-w-2xl text-sm text-slate-300 sm:text-base">
              During the early Lantern-Bound phase, GigAgent is intentionally
              gentle: generous free access, with optional supporter tiers as the
              hosted version comes online.
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            <PricingCard
              label="Today"
              name="Self-hosted prototype"
              price="$0"
              description="Run GigAgent on your own machine while it’s in early development."
              features={[
                "Use GigAgent locally",
                "Customizable profile input",
                "Curated, ranked gig lists",
                "Perfect for builders & tinkerers",
              ]}
              ctaLabel="Run local demo"
              href="/gig-agent"
              highlighted={false}
            />
            <PricingCard
              label="Soon"
              name="Hosted GigAgent"
              price="$5–$8 / month"
              description="For humans who want the benefits without running servers."
              features={[
                "Hosted, always-on GigAgent",
                "Save multiple profiles",
                "Optional daily curated email",
                "Early access to Micro-Gig & Music Modes",
              ]}
              ctaLabel="Join early access list"
              href="#waitlist"
              highlighted
            />
          </div>
        </section>

        {/* Waitlist placeholder */}
        <section
          id="waitlist"
          className="mb-16 rounded-3xl border border-slate-700 bg-slate-950/70 p-6 shadow-lg shadow-slate-950/80"
        >
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h3 className="text-base font-semibold text-slate-50 sm:text-lg">
                Be the first to know when the hosted version goes live
              </h3>
              <p className="max-w-xl text-sm text-slate-300">
                A simple, gentle email when GigAgent is ready for non-technical
                humans. No funnels, no drip campaigns—just a lantern ping.
              </p>
            </div>
            <div className="w-full max-w-sm">
              {/* Replace this with your actual form or email service later */}
              <div className="rounded-2xl border border-slate-700 bg-slate-900/80 p-3 text-xs text-slate-300">
                <p className="mb-2 font-medium text-slate-100">
                  Coming soon: email capture
                </p>
                <p>
                  When you’re ready, we&apos;ll wire this box to your email
                  service (Substack, ConvertKit, etc.) and start collecting
                  early access signups.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* FAQ */}
        <section id="faq" className="mb-16 space-y-6">
          <div>
            <h2 className="text-lg font-semibold text-slate-50 sm:text-xl">
              Questions, gently answered
            </h2>
            <p className="max-w-2xl text-sm text-slate-300 sm:text-base">
              GigAgent is part of a different kind of tech ecosystem—one that
              remembers you&apos;re human.
            </p>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            {faqs.map((faq) => (
              <div
                key={faq.question}
                className="rounded-2xl border border-slate-700 bg-slate-950/80 p-4"
              >
                <h3 className="mb-1 text-sm font-semibold text-slate-50">
                  {faq.question}
                </h3>
                <p className="text-xs text-slate-300 sm:text-sm">
                  {faq.answer}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Footer */}
        <footer className="mt-auto border-t border-slate-800 pt-4 text-xs text-slate-500 sm:text-[13px]">
          <div className="flex flex-col items-start justify-between gap-2 sm:flex-row sm:items-center">
            <p>
              Crafted in the Lantern-Bound Garden.{" "}
              <span className="text-emerald-300">🏮✨ •LUX•</span>
            </p>
            <div className="flex gap-4">
              <Link
                href="/"
                className="hover:text-emerald-300 hover:underline"
              >
                Return to the Garden
              </Link>
              <a
                href="#"
                className="cursor-default text-slate-600 hover:text-slate-400"
              >
                v0 · Early access
              </a>
            </div>
          </div>
        </footer>
      </div>
    </main>
  );
}

type FeatureCardProps = {
  title: string;
  body: string;
  icon: React.ReactNode;
};

function FeatureCard({ title, body, icon }: FeatureCardProps) {
  return (
    <div className="flex flex-col rounded-2xl border border-slate-700 bg-slate-950/80 p-4 shadow-sm shadow-slate-950/70">
      <div className="mb-3 inline-flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-400/10">
        {icon}
      </div>
      <h3 className="mb-1 text-sm font-semibold text-slate-50">{title}</h3>
      <p className="text-xs text-slate-300 sm:text-sm">{body}</p>
    </div>
  );
}

type StepProps = {
  step: string;
  title: string;
  body: string;
};

function HowItWorksStep({ step, title, body }: StepProps) {
  return (
    <li className="relative pl-6">
      <div className="absolute -left-[14px] top-[3px] flex h-7 w-7 items-center justify-center rounded-full border border-emerald-400/60 bg-slate-950 text-[10px] font-semibold text-emerald-200 shadow-sm">
        {step}
      </div>
      <h3 className="text-sm font-semibold text-slate-50">{title}</h3>
      <p className="text-xs text-slate-300 sm:text-sm">{body}</p>
    </li>
  );
}

type PricingCardProps = {
  label: string;
  name: string;
  price: string;
  description: string;
  features: string[];
  ctaLabel: string;
  href: string;
  highlighted?: boolean;
};

function PricingCard({
  label,
  name,
  price,
  description,
  features,
  ctaLabel,
  href,
  highlighted,
}: PricingCardProps) {
  return (
    <div
      className={`flex flex-col rounded-3xl border p-5 shadow-lg ${
        highlighted
          ? "border-emerald-400/70 bg-slate-950/80 shadow-emerald-500/30"
          : "border-slate-700 bg-slate-950/70 shadow-slate-950/70"
      }`}
    >
      <div className="mb-3 flex items-center justify-between">
        <span
          className={`inline-flex items-center rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.18em] ${
            highlighted
              ? "border border-emerald-400/60 bg-emerald-400/10 text-emerald-100"
              : "border border-slate-600 bg-slate-900/80 text-slate-200"
          }`}
        >
          {label}
        </span>
      </div>
      <h3 className="text-base font-semibold text-slate-50">{name}</h3>
      <p className="mt-1 text-sm text-slate-300">{description}</p>
      <p className="mt-3 text-2xl font-semibold text-slate-50">{price}</p>

      <ul className="mt-3 space-y-1.5 text-xs text-slate-200 sm:text-sm">
        {features.map((feature) => (
          <li key={feature} className="flex items-start gap-2">
            <CheckCircle2 className="mt-[2px] h-3.5 w-3.5 text-emerald-300" />
            <span>{feature}</span>
          </li>
        ))}
      </ul>

      <div className="mt-5">
        <Link
          href={href}
          className={`inline-flex w-full items-center justify-center gap-2 rounded-full px-4 py-2 text-sm font-semibold transition ${
            highlighted
              ? "bg-emerald-400 text-slate-950 hover:bg-emerald-300"
              : "border border-slate-600 bg-slate-900/80 text-slate-100 hover:border-emerald-300/70 hover:text-emerald-100"
          }`}
        >
          {ctaLabel}
          <ArrowRight className="h-4 w-4" />
        </Link>
      </div>
    </div>
  );
}
