import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatScore(score: number): string {
  return `${Math.round(score)}/100`;
}

export function formatConfidence(conf: number): string {
  return `${Math.round(conf * 100)}%`;
}

export function getScoreColor(score: number): string {
  if (score >= 80) return "text-emerald-400";
  if (score >= 60) return "text-amber-400";
  return "text-rose-400";
}

export function getScoreBg(score: number): string {
  if (score >= 80) return "from-emerald-500 to-teal-500";
  if (score >= 60) return "from-amber-500 to-orange-500";
  return "from-rose-500 to-red-500";
}

export function getRecommendationColor(rec: string): string {
  const upper = rec.toUpperCase();
  if (upper.includes("YES") || upper.includes("GO") && !upper.includes("NO")) return "text-emerald-400";
  if (upper.includes("PIVOT") || upper.includes("CONDITIONAL")) return "text-amber-400";
  return "text-rose-400";
}

export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString("en-US", {
    year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit",
  });
}

export function truncate(str: string, max: number): string {
  return str.length > max ? str.slice(0, max) + "..." : str;
}
