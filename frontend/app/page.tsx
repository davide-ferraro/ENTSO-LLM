"use client";

import { useMemo, useRef, useState } from "react";
import { useEffect, useMemo, useRef, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
const MODEL_NAME = process.env.NEXT_PUBLIC_LLM_MODEL_NAME ?? "Qwen/Qwen2.5-7B-Instruct";

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
  kind?: "status" | "router" | "request";
  routerEndpoints?: string[];
  requestPayload?: Array<Record<string, unknown>>;
  codeLegend?: CodeLegendEntry[];
  results?: RequestResult[];
  summary?: Record<string, unknown>;
  files?: FileLink[];
};

type CsvPreview = {
  headers: string[];
  rows: string[][];
};

type CodeLegendEntry = {
  code: string;
  description: string;
};

const DOCUMENT_TYPE_LABELS: Record<string, string> = {
  A25: "Allocation result document",
  A44: "Price document",
  A61: "Estimated Net Transfer Capacity",
  A65: "System total load",
  A68: "Installed generation per type",
  A69: "Wind and solar generation forecast",
  A70: "Load forecast margin",
  A71: "Generation forecast",
  A73: "Actual generation per type",
  A74: "Wind and solar generation",
  A75: "Actual generation per generation unit",
  A77: "Scheduled generation",
  A78: "Unavailability of generation units",
  A79: "Unavailability of production units",
  A80: "Unavailability of offshore grid",
  A81: "Unavailability of transmission infrastructure",
  A85: "Imbalance volume",
  A86: "Imbalance prices",
};

const PROCESS_TYPE_LABELS: Record<string, string> = {
  A01: "Day ahead",
  A16: "Realised",
  A31: "Week ahead",
  A32: "Month ahead",
  A33: "Year ahead",
  A43: "Day ahead (balancing)",
  A44: "Intraday",
};

const BUSINESS_TYPE_LABELS: Record<string, string> = {
  A04: "Base load",
  A29: "Imports",
  A30: "Exports",
  B01: "Solar",
  B02: "Wind onshore",
  B03: "Wind offshore",
  B04: "Fossil gas",
  B05: "Fossil hard coal",
  B06: "Fossil lignite",
  B09: "Geothermal",
  B10: "Congestion income",
  B11: "Hydro pumped storage",
  B12: "Hydro run-of-river",
  B14: "Nuclear",
  B15: "Fossil oil",
  B16: "Solar",
  B17: "Biomass",
  B18: "Wind onshore",
  B19: "Wind offshore",
};

const PSR_TYPE_LABELS: Record<string, string> = {
  B01: "Biomass",
  B02: "Fossil brown coal/lignite",
  B03: "Fossil coal-derived gas",
  B04: "Fossil gas",
  B05: "Fossil hard coal",
  B06: "Fossil oil",
  B07: "Fossil oil shale",
  B08: "Fossil peat",
  B09: "Geothermal",
  B10: "Hydro pumped storage",
  B11: "Hydro run-of-river and poundage",
  B12: "Hydro water reservoir",
  B13: "Marine",
  B14: "Nuclear",
  B15: "Other renewable",
  B16: "Solar",
  B17: "Waste",
  B18: "Wind offshore",
  B19: "Wind onshore",
  B20: "Other",
};

const EIC_CODE_LABELS: Record<string, string> = {
  "10YAT-APG------L": "Austria (APG control area)",
  "10YBE----------2": "Belgium",
  "10YDE-VE-------2": "Germany (50Hertz)",
  "10YFR-RTE------C": "France (RTE)",
  "10YES-REE------0": "Spain (REE)",
  "10YIT-GRTN-----B": "Italy (Terna)",
  "10Y1001A1001A82H": "Germany-Luxembourg",
  "10YGB----------A": "Great Britain",
  "10YNL----------L": "Netherlands",
  "10YDK-1--------W": "Denmark (DK1)",
  "10YDK-2--------M": "Denmark (DK2)",
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

const buildCodeLegend = (requests: Array<Record<string, unknown>> | undefined): CodeLegendEntry[] => {
  if (!requests) {
    return [];
  }

  const legend = new Map<string, string>();
  const addLegend = (code: string, description: string | undefined) => {
    if (description && !legend.has(code)) {
      legend.set(code, description);
    }
  };

  requests.forEach((request) => {
    const params = request.params as Record<string, unknown> | undefined;
    if (!params) {
      return;
    }

    Object.entries(params).forEach(([key, value]) => {
      if (typeof value !== "string") {
        return;
      }
      if (key === "documentType") {
        addLegend(value, DOCUMENT_TYPE_LABELS[value]);
      }
      if (key === "processType") {
        addLegend(value, PROCESS_TYPE_LABELS[value]);
      }
      if (key === "businessType") {
        addLegend(value, BUSINESS_TYPE_LABELS[value]);
      }
      if (key === "psrType") {
        addLegend(value, PSR_TYPE_LABELS[value]);
      }
      if (key.toLowerCase().includes("domain")) {
        addLegend(value, EIC_CODE_LABELS[value]);
      }
    });
  });

  return Array.from(legend.entries()).map(([code, description]) => ({ code, description }));
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
  const [statusMessage, setStatusMessage] = useState("Ready for a new prompt.");
  const [error, setError] = useState<string | null>(null);
  const statusEntryRef = useRef<string | null>(null);

  const statusTimersRef = useRef<number[]>([]);
  const statusRef = useRef(status);
  const statusEntryRef = useRef<string | null>(null);

  useEffect(() => {
    statusRef.current = status;
  }, [status]);

  const updateStatusEntry = (nextMessage: string) => {
    const statusId = statusEntryRef.current;
    if (!statusId) {
      return;
    }
    setMessages((prev) =>
      prev.map((entry) => (entry.id === statusId ? { ...entry, content: nextMessage } : entry)),
    );
  };

  const handleEvent = (event: string, data: Record<string, unknown>) => {
    if (event === "status" && typeof data.message === "string") {
      setStatusMessage(data.message);
      updateStatusEntry(data.message);
    }
    if (event === "router" && Array.isArray(data.endpoints)) {
      const routerEntry: ChatEntry = {
        id: `${Date.now()}-router`,
        role: "assistant",
        content: "Router selected the following endpoint(s):",
        kind: "router",
        routerEndpoints: data.endpoints as string[],
      };
      setMessages((prev) => [...prev, routerEntry]);
    }
    if (event === "request" && Array.isArray(data.request_payload)) {
      const requestPayload = data.request_payload as Array<Record<string, unknown>>;
      const requestEntry: ChatEntry = {
        id: `${Date.now()}-request`,
        role: "assistant",
        content: "Generated JSON request payload:",
        kind: "request",
        requestPayload,
        codeLegend: buildCodeLegend(requestPayload),
      };
      setMessages((prev) => [...prev, requestEntry]);
    }
    if (event === "results" && typeof data === "object") {
      const assistantEntry: ChatEntry = {
        id: `${Date.now()}-assistant`,
        role: "assistant",
        content: "ENTSO-E requests executed. Review outputs below.",
        results: data.results as RequestResult[],
        summary: data.summary as Record<string, unknown>,
        files: data.files as FileLink[],
      };
      setMessages((prev) => [...prev, assistantEntry]);
      setStatus("idle");
      setStatusMessage("Ready for a new prompt.");
    }
    if (event === "error" && typeof data.detail === "string") {
      setStatus("error");
      setError(data.detail);
      setStatusMessage(data.detail);
    }
  };

  const streamChat = async (payload: { message: string; history: Array<{ role: string; content: string }> }) => {
    const response = await fetch(`${API_BASE}/chat/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "text/event-stream" },
      body: JSON.stringify(payload),
    });

    if (!response.ok || !response.body) {
      const data = await response.json();
      throw new Error(data.detail ?? "Chat request failed");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let buffer = "";
    let currentEvent = "message";

    while (true) {
      const { value, done } = await reader.read();
      if (done) {
        break;
      }
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() ?? "";

      for (const line of lines) {
        if (line.startsWith("event:")) {
          currentEvent = line.replace("event:", "").trim();
          continue;
        }
        if (line.startsWith("data:")) {
          const raw = line.replace("data:", "").trim();
          if (!raw) {
            continue;
          }
          try {
            const data = JSON.parse(raw) as Record<string, unknown>;
            handleEvent(currentEvent, data);
          } catch {
            // Ignore malformed data payloads.
          }
        }
      }
    }
  const clearStatusTimers = () => {
    statusTimersRef.current.forEach((timer) => window.clearTimeout(timer));
    statusTimersRef.current = [];
  };

  const scheduleStatusUpdates = () => {
    clearStatusTimers();
    const steps = [
      `Loading Qwen...${MODEL_NAME} for the first time`,
      "Finding the right endpoint",
      "Writing the request",
      "Connecting to ENTSO-E APIs",
    ];

    setStatusMessage(steps[0]);
    updateStatusEntry(steps[0]);

    steps.slice(1).forEach((step, index) => {
      const timer = window.setTimeout(() => {
        if (statusRef.current !== "loading") {
          return;
        }
        setStatusMessage(step);
        updateStatusEntry(step);
      }, (index + 1) * 1200);
      statusTimersRef.current.push(timer);
    });
  };

  const handleSend = async () => {
    if (!input.trim()) {
      return;
    }

    const userEntry: ChatEntry = {
      id: `${Date.now()}-user`,
      role: "user",
      content: input,
    };

    const statusEntry: ChatEntry = {
      id: `${Date.now()}-status`,
      role: "assistant",
      content: "Starting request…",
      content: `Loading Qwen...${MODEL_NAME} for the first time`,
      kind: "status",
    };
    statusEntryRef.current = statusEntry.id;
    setMessages((prev) => [...prev, userEntry, statusEntry]);
    setInput("");
    setStatus("loading");
    setError(null);
    scheduleStatusUpdates();

    try {
      const history = messages
        .filter((entry) => entry.kind !== "status" && entry.kind !== "router" && entry.kind !== "request")
        .map((entry) => ({ role: entry.role, content: entry.content }));
      await streamChat({ message: userEntry.content, history });
      const response = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userEntry.content,
          history,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail ?? "Chat request failed");
      }

      const data = await response.json();
      const routerEntry: ChatEntry | null = data.router_endpoints?.length
        ? {
            id: `${Date.now()}-router`,
            role: "assistant",
            content: "Router selected the following endpoint(s):",
            kind: "router",
            routerEndpoints: data.router_endpoints,
          }
        : null;
      const requestPayload = data.request_payload as Array<Record<string, unknown>> | undefined;
      const requestEntry: ChatEntry | null = requestPayload
        ? {
            id: `${Date.now()}-request`,
            role: "assistant",
            content: "Generated JSON request payload:",
            kind: "request",
            requestPayload,
            codeLegend: buildCodeLegend(requestPayload),
          }
        : null;
      const assistantEntry: ChatEntry = {
        id: `${Date.now()}-assistant`,
        role: "assistant",
        content: "ENTSO-E requests executed. Review outputs below.",
        results: data.results,
        summary: data.summary,
        files: data.files,
      };

      setMessages((prev) => [
        ...prev,
        ...(routerEntry ? [routerEntry] : []),
        ...(requestEntry ? [requestEntry] : []),
        assistantEntry,
      ]);
      setStatus("idle");
      setStatusMessage("Ready for a new prompt.");
    } catch (err) {
      setStatus("error");
      setError(err instanceof Error ? err.message : "Unknown error");
      setStatusMessage("Request failed. Please try again.");
    } finally {
      clearStatusTimers();
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
            <article key={entry.id} className={`chat-message ${entry.role} ${entry.kind ?? ""}`}>
              <div className="message-meta">
                <span className="role-tag">{entry.role === "user" ? "You" : "ENTSO-E"}</span>
              </div>
              <div className="message-body">
                {entry.kind === "status" && <p className="muted">{entry.content}</p>}
                {entry.kind === "router" && (
                  <>
                    <p>{entry.content}</p>
                    <div className="tag-list">
                      {entry.routerEndpoints?.map((endpoint) => (
                        <span key={endpoint} className="tag">
                          {endpoint}
                        </span>
                      ))}
                    </div>
                  </>
                )}
                {entry.kind === "request" && (
                  <>
                    <p>{entry.content}</p>
                    {entry.requestPayload && (
                      <div className="request-payload">
                        <pre>{JSON.stringify(entry.requestPayload, null, 2)}</pre>
                      </div>
                    )}
                    {entry.codeLegend && entry.codeLegend.length > 0 && (
                      <div className="code-legend">
                        {entry.codeLegend.map((legend) => (
                          <div key={legend.code} className="legend-row">
                            <span className="tag">{legend.code}</span>
                            <span>{legend.description}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </>
                )}
                {!entry.kind && <p>{entry.content}</p>}
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
          {status === "loading" && <span className="status-text">{statusMessage}</span>}
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
