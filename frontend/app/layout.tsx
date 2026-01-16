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
          <main className="app-main">{children}</main>
        </div>
      </body>
    </html>
  );
}
