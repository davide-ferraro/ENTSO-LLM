import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "ENTSO-LLM",
  description: "Chat-first UI for ENTSO-E data",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="app-shell">
          <header className="app-header">
            <div>
              <h1>ENTSO-LLM</h1>
              <p>Chat-first access to ENTSO-E data exports</p>
            </div>
            <div className="status-pill" aria-live="polite">
              Backend ready
            </div>
          </header>
          <main className="app-main">{children}</main>
        </div>
      </body>
    </html>
  );
}
