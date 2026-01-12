# 🔌 ENTSO-LLM

> **Natural language access to European electricity market data**

ENTSO-LLM is a tool that lets you retrieve data from the [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/) using natural language. Simply describe what data you need, and an LLM will craft the API request for you.

---

## ✨ Features

- **Natural Language Requests**: Ask for data in plain English
- **Local & Modal API Fetching**: One-time requests or on-demand Modal API runs
- **Historical Data**: Automatic 20-year data collection
- **Comprehensive Documentation**: 3,700+ lines of API documentation for LLM context
- **260 Working Examples**: Pre-tested request patterns across all 65 endpoints
- **Multi-Format Output**: XML, JSON, and CSV exports
- **EIC Code Reference**: Complete geographic identifier database

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/ENTSO-LLM.git
cd ENTSO-LLM
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
cp .env.example .env
# Edit .env and add your ENTSO-E API key
```

Get your API key at: https://transparency.entsoe.eu/ (register → request API access)

### 3. Create Requests with LLM

Open your preferred LLM (Claude, GPT, etc.) and paste the prompt from `docs/prompts/prompt_instructions.md`.

Then ask for what you need:
> "Get me day-ahead prices for Germany for the last week"

The LLM will generate a request like:
```json
{
    "name": "prices_dayahead_germany_7days",
    "run": "local",
    "params": {
        "documentType": "A44",
        "in_Domain": "10Y1001A1001A82H",
        "out_Domain": "10Y1001A1001A82H",
        "periodStart": "202601010000",
        "periodEnd": "202601080000"
    }
}
```

### 4. Add to my_requests.json

```json
{
    "requests": [
        // paste your request here
    ]
}
```

### 5. Run

```bash
python -m src.local
```

### 6. Get Your Data

- **XML**: `results/xml/prices_dayahead_germany_7days.xml`
- **JSON**: `results/json/prices_dayahead_germany_7days.json`
- **CSV**: `results/csv/prices_dayahead_germany_7days.csv`

---

## ⚡ On-Demand Modal API

ENTSO-LLM supports **on-demand data collection** using a Modal-hosted HTTP API.

### Setup Modal

```bash
# 1. Install Modal
pip install modal

# 2. Authenticate (opens browser)
modal token new

# 3. Create secret with your API key
modal secret create ENTSOE_API_KEY ENTSOE_API_KEY=your_key_here
```

### Deploy the API (one time only!)

```bash
modal deploy src/modal_api.py
```

Modal will print the HTTPS endpoint URL. Use it to trigger requests on-demand:

```bash
curl -X POST "<YOUR_MODAL_ENDPOINT>" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "load_germany_operational",
    "params": {
      "documentType": "A65",
      "processType": "A16",
      "outBiddingZone_Domain": "10Y1001A1001A82H",
      "periodStart": "202601010000",
      "periodEnd": "202601080000"
    }
  }'
```

### What Happens

1. **On-demand run**: The API fetches data when the HTTP request arrives
2. **Storage**: Data saved to the `entsoe-fetch` Modal volume (same structure as `results/`)
3. **No scheduling**: Use your chat/LLM workflow to decide when to call the endpoint

---

## 📁 Project Structure

```
ENTSO-LLM/
├── src/                        # Python source code
│   ├── __init__.py             # Package initialization
│   ├── local.py                # Local execution script
│   ├── modal_api.py            # Modal on-demand API service
│   └── parser.py               # XML to JSON/CSV parser
├── archived/
│   └── modal_runner.py         # Archived Modal cron job script
│
├── docs/                       # Documentation for LLM context
│   ├── api/                    # Technical API documentation
│   │   ├── ENTSOE_Transparency_API_Documentation.md
│   │   ├── ENTSOE_EIC_Area_Codes.md
│   │   └── ENTSOE_XML_Parsing_Guide.md
│   ├── examples/               # Request examples and references
│   │   ├── request_examples.md
│   │   └── natural_language_examples.md
│   └── prompts/                # LLM prompts
│       ├── context_prompt.md
│       └── prompt_instructions.md
│
├── results/                    # Output (gitignored)
│   ├── xml/
│   ├── json/
│   └── csv/
│
├── my_requests.json            # Your API requests go here
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
└── README.md
```

---

## 📊 Available Data

| Domain | Examples |
|--------|----------|
| **Load** | Actual consumption, day/week/month/year-ahead forecasts |
| **Generation** | By type (solar, wind, nuclear, etc.), by unit, forecasts |
| **Prices** | Day-ahead, intraday market prices |
| **Transmission** | Cross-border flows, transfer capacities |
| **Outages** | Planned/unplanned unavailability |
| **Balancing** | Imbalance prices, reserve procurement |

---

## 🔧 Request Format

### Local Request
```json
{
    "name": "descriptive_name",
    "run": "local",
    "params": {
        "documentType": "A65",
        "periodStart": "202601010000",
        "periodEnd": "202601080000",
        ...
    }
}
```

### Modal API Payload
```json
{
    "name": "descriptive_name",
    "params": {
        "documentType": "A65",
        ...
    }
}
```

---

## 📖 Documentation

The `docs/` folder contains comprehensive documentation:

- **API Documentation** (`docs/api/`): All 69 endpoints with parameters and examples
- **EIC Codes** (`docs/api/`): Geographic identifiers for all European areas
- **Request Examples** (`docs/examples/`): 260 tested requests with working parameters
- **XML Parsing Guide** (`docs/api/`): Understanding API response structure
- **LLM Prompts** (`docs/prompts/`): Instructions for setting up LLM assistance

---

## 🤝 How It Works

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   You (human)   │────▶│   LLM + Docs    │────▶│ my_requests.json│
│ "Get wind data  │     │ Reads docs,     │     │ Valid API       │
│  for Spain"     │     │ crafts request  │     │ request         │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                              ┌──────────┴──────────┐
                                              │                     │
                                    ┌─────────▼─────────┐ ┌─────────▼─────────┐
                                    │  python -m        │ │  modal deploy     │
                                    │  src.local        │ │  src/modal_api    │
                                    └─────────┬─────────┘ └─────────┬─────────┘
                                              │                     │
                                    ┌─────────▼─────────┐ ┌─────────▼─────────┐
                                    │  results/         │ │  Modal Volume     │
                                    │  xml/json/csv     │ │  entsoe-fetch     │
                                    └───────────────────┘ └───────────────────┘
```

---

## ⚠️ Limitations

- **API Rate Limits**: Be respectful of ENTSO-E servers
- **Time Range**: Most endpoints limited to ~1 year per request (auto-chunked for historical)
- **Data Availability**: Not all data available for all regions/periods

---

## 📜 License

MIT License - see LICENSE file

---

## 🙏 Acknowledgments

- [ENTSO-E](https://www.entsoe.eu/) for providing the Transparency Platform
- [Modal](https://modal.com/) for serverless API runtime
- Data provided under EU Regulation 543/2013

---

## 📬 Support

- Check `docs/examples/request_examples.md` for working examples
- Open an issue for bugs or feature requests

---

*Making European electricity data accessible to everyone* ⚡
