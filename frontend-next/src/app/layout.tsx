import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "@/providers";
import { Navbar } from "@/components/layout/Navbar";
import { Toaster } from "@/components/ui/toaster";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: { default: "Innovation Discovery Platform", template: "%s | IDP" },
  description: "AI-powered multi-agent innovation discovery and strategic analysis platform",
  keywords: ["AI", "Innovation", "Business Strategy", "Technology", "Patent Analysis"],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning className="dark">
      <body
        className={`${inter.variable}`}
        style={{
          fontFamily: "var(--font-inter), Inter, system-ui, sans-serif",
          background: "linear-gradient(135deg, #020817 0%, #0f172a 50%, #020817 100%)",
          minHeight: "100vh",
          color: "#f1f5f9",
        }}
      >
        <Providers>
          {/* Fixed background gradient blobs */}
          <div
            aria-hidden
            style={{
              position: "fixed",
              inset: 0,
              pointerEvents: "none",
              zIndex: 0,
              overflow: "hidden",
            }}
          >
            <div style={{ position: "absolute", top: "10%", left: "15%", width: 500, height: 500, background: "radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%)", borderRadius: "50%" }} />
            <div style={{ position: "absolute", bottom: "10%", right: "15%", width: 400, height: 400, background: "radial-gradient(circle, rgba(168,85,247,0.10) 0%, transparent 70%)", borderRadius: "50%" }} />
            <div style={{ position: "absolute", top: "50%", left: "50%", transform: "translate(-50%,-50%)", width: 800, height: 800, background: "radial-gradient(circle, rgba(59,130,246,0.06) 0%, transparent 70%)", borderRadius: "50%" }} />
          </div>

          {/* Navbar sits on top */}
          <div style={{ position: "relative", zIndex: 50 }}>
            <Navbar />
          </div>

          {/* All page content, padded below navbar */}
          <main
            style={{
              position: "relative",
              zIndex: 10,
              paddingTop: "4rem", /* 64px = h-16 navbar height */
            }}
          >
            {children}
          </main>

          <Toaster />
        </Providers>
      </body>
    </html>
  );
}
