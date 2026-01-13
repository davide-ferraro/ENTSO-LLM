"use client";

import { useMemo, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

type FileLink = {
  id: string;
  type: string;
  name: string;
  url: string;
};

type RequestSummary = {
  timeseries_count?: number;
  data_points?: number;
};

type RequestResult = {
  name: string;
  success: boolean;
  status_code?: number | null;
  summary: RequestSummary;
  error?: string | null;
  api_message?: string | null;
  files: FileLink[];
  csv_info?: Record<string, unknown> | null;
};

type ChatEntry = {
  id: string;
  role: "user" | "assistant";
  content: string;
  results?: RequestResult[];
  summary?: Record<string, unknown>;
  files?: FileLink[];
};

type CsvPreview = {
  headers: string[];
  rows: string[][];
};

const parseCsvPreview = (text: string, maxRows = 8): CsvPreview => {
  const lines = text.trim().split("\n");
  if (lines.length === 0) {
    return { headers: [], rows: [] };
  }
  const headers = lines[0].split(",");
  const rows = lines.slice(1, maxRows + 1).map((line) => line.split(","));
  return { headers, rows };
};

const ResultCard = ({ result }: { result: RequestResult }) => {
  const [activeTab, setActiveTab] = useState<"json" | "csv">("json");
  const [jsonPreview, setJsonPreview] = useState<string>("");
  const [csvPreview, setCsvPreview] = useState<CsvPreview | null>(null);

  const jsonFile = result.files.find((file) => file.type === "json");
  const csvFile = result.files.find((file) => file.type === "csv");

  const statusLabel = result.success ? "Success" : "Failed";
  const statusClass = result.success ? "status-success" : "status-failed";

  const loadJsonPreview = async () => {
    if (!jsonFile) {
      setJsonPreview("JSON output not available.");
      return;
    }
    const response = await fetch(`${API_BASE}${jsonFile.url}`);
    const data = await response.json();
    setJsonPreview(JSON.stringify(data, null, 2));
  };

  const loadCsvPreview = async () => {
    if (!csvFile) {
      setCsvPreview({ headers: [], rows: [] });
      return;
    }
    const response = await fetch(`${API_BASE}${csvFile.url}`);
    const text = await response.text();
    setCsvPreview(parseCsvPreview(text));
  };

  const tabContent = useMemo(() => {
    if (activeTab === "json") {
      if (!jsonPreview) {
        loadJsonPreview();
        return <p className="muted">Loading JSON preview…</p>;
      }
      return <pre>{jsonPreview}</pre>;
    }
    if (!csvPreview) {
      loadCsvPreview();
      return <p className="muted">Loading CSV preview…</p>;
    }
    if (csvPreview.headers.length === 0) {
      return <p className="muted">CSV preview not available.</p>;
    }
    return (
      <table>
        <thead>
          <tr>
            {csvPreview.headers.map((header) => (
              <th key={header}>{header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {csvPreview.rows.map((row, index) => (
            <tr key={`${result.name}-row-${index}`}>
              {row.map((value, cellIndex) => (
                <td key={`${result.name}-cell-${index}-${cellIndex}`}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  }, [activeTab, csvPreview, jsonPreview]);

  return (
    <section className="result-card">
      <header>
        <div>
          <h4>{result.name}</h4>
          <p className="muted">
            {result.summary?.timeseries_count ?? 0} series · {result.summary?.data_points ?? 0} points
          </p>
        </div>
        <span className={`pill ${statusClass}`}>{statusLabel}</span>
      </header>
      {result.error && <p className="error-text">{result.error}</p>}
      {result.api_message && <p className="muted">{result.api_message}</p>}
      <div className="file-links">
        {result.files.map((file) => (
          <a key={file.id} href={`${API_BASE}${file.url}`} target="_blank" rel="noreferrer">
            Download {file.type.toUpperCase()}
          </a>
        ))}
      </div>
      <div className="tabs">
        <button
          type="button"
          className={activeTab === "json" ? "active" : ""}
          onClick={() => setActiveTab("json")}
        >
          JSON
        </button>
        <button
          type="button"
          className={activeTab === "csv" ? "active" : ""}
          onClick={() => setActiveTab("csv")}
        >
          CSV Table
        </button>
      </div>
      <div className="preview">{tabContent}</div>
    </section>
  );
};

export default function HomePage() {
  const [messages, setMessages] = useState<ChatEntry[]>([]);
  const [input, setInput] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "error">("idle");
  const [error, setError] = useState<string | null>(null);

  const handleSend = async () => {
    if (!input.trim()) {
      return;
    }

    const userEntry: ChatEntry = {
      id: `${Date.now()}-user`,
      role: "user",
      content: input,
    };

    setMessages((prev) => [...prev, userEntry]);
    setInput("");
    setStatus("loading");
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userEntry.content,
          history: messages.map((entry) => ({ role: entry.role, content: entry.content })),
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail ?? "Chat request failed");
      }

      const data = await response.json();
      const assistantEntry: ChatEntry = {
        id: `${Date.now()}-assistant`,
        role: "assistant",
        content: "ENTSO-E requests executed. Review outputs below.",
        results: data.results,
        summary: data.summary,
        files: data.files,
      };

      setMessages((prev) => [...prev, assistantEntry]);
      setStatus("idle");
    } catch (err) {
      setStatus("error");
      setError(err instanceof Error ? err.message : "Unknown error");
    }
  };

  return (
    <div className="workspace">
      <aside className="sidebar">
        <div className="brand">
          <div className="logo-mark">entsoe</div>
          <span>Reliable · Sustainable · Connected</span>
        </div>
        <nav className="sidebar-nav">
          <button type="button" className="nav-item active">
            + New chat
          </button>
          <button type="button" className="nav-item">Search chats</button>
          <button type="button" className="nav-item">Library</button>
          <button type="button" className="nav-item">Apps</button>
          <button type="button" className="nav-item">Codex</button>
          <button type="button" className="nav-item">GPTs</button>
        </nav>
        <div className="sidebar-section">
          <p className="section-title">Projects</p>
          <button type="button" className="nav-item">New project</button>
          <button type="button" className="nav-item">Mathlens</button>
          <button type="button" className="nav-item">Writing LinkedIn content</button>
          <button type="button" className="nav-item">Rebase Documentation</button>
        </div>
        <div className="sidebar-section">
          <p className="section-title">Chats</p>
          <button type="button" className="nav-item">Request Clarification</button>
          <button type="button" className="nav-item">Push Repo to GitHub</button>
          <button type="button" className="nav-item">GTM Strategy Review</button>
        </div>
        <div className="sidebar-footer">
          <div className="profile">
            <div className="avatar">DF</div>
            <div>
              <strong>Davide Ferraro</strong>
              <span>Rebase Workspace</span>
            </div>
          </div>
          <button type="button" className="invite">+ Invite team members</button>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div className="model-selector">
            <span className="model-dot" />
            <span>ChatGPT 5.2</span>
          </div>
          <div className="top-actions">
            <button type="button" className="ghost-button">
              Share
            </button>
            <button type="button" className="ghost-button">⋯</button>
            <button type="button" className="request-pill">
              request
            </button>
          </div>
        </header>

        <section className="chat-area">
          {messages.length === 0 && (
            <article className="assistant-message">
              <p>
                Could you clarify what you mean by <strong>“request”</strong>?
              </p>
              <p className="muted">For example, are you trying to:</p>
              <ul>
                <li>make a work request (IT, ops, access, budget, etc.)</li>
                <li>draft a formal request (email or document)</li>
                <li>request information or a file</li>
                <li>trigger some internal process at ENTSO-E</li>
              </ul>
              <p className="muted">A short sentence with the goal is enough, and I’ll take it from there.</p>
              {status === "error" && <p className="error-text">{error}</p>}
            </article>
          )}

          {messages.map((entry) => (
            <article key={entry.id} className={`chat-message ${entry.role}`}>
              <div className="message-meta">
                <span className="role-tag">{entry.role === "user" ? "You" : "ENTSO-E"}</span>
              </div>
              <div className="message-body">
                <p>{entry.content}</p>
                {entry.summary && (
                  <div className="summary-grid">
                    {Object.entries(entry.summary).map(([key, value]) => (
                      <div key={key}>
                        <span>{key.replaceAll("_", " ")}</span>
                        <strong>{String(value)}</strong>
                      </div>
                    ))}
                  </div>
                )}
                {entry.results && (
                  <div className="results">
                    {entry.results.map((result) => (
                      <ResultCard key={result.name} result={result} />
                    ))}
                  </div>
                )}
              </div>
            </article>
          ))}
        </section>

        <footer className="composer">
          {status === "loading" && <span className="status-text">Running ENTSO-E request…</span>}
          {status === "idle" && <span className="status-text">Ready for a new prompt.</span>}
          {status === "error" && <span className="status-text error-text">{error}</span>}
          <div className="composer-bar">
            <span className="composer-icon">🔎</span>
            <textarea
              placeholder="Ask anything"
              value={input}
              onChange={(event) => setInput(event.target.value)}
              rows={1}
            />
            <button type="button" className="mic-button" aria-label="Record">
              🎙️
            </button>
            <button type="button" className="send-button" onClick={handleSend} disabled={status === "loading"}>
              ➤
            </button>
          </div>
          <p className="footnote">
            ChatGPT can make mistakes. ENTSO-E does not use your data to train its models.
          </p>
        </footer>
      </main>
    </div>
  );
}
