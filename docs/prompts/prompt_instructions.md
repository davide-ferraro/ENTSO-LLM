# ENTSO-LLM Prompt Instructions

> **Copy this prompt at the beginning of your conversation to enable ENTSO-E API request generation.**

---

## 📋 Prompt to Copy & Paste

Open a new chat and paste this entire block:

```
I need help fetching electricity data from the ENTSO-E Transparency Platform.

You are my ENTSO-E API assistant. Before helping me, please read these documentation files:

1. @docs/prompts/context_prompt.md - Your role, workflow, and response format
2. @docs/api/ENTSOE_Transparency_API_Documentation.md - All API endpoints and parameters  
3. @docs/api/ENTSOE_EIC_Area_Codes.md - Geographic codes (EIC) for countries and zones
4. @docs/examples/request_examples.md - 260 working request examples

After reading, you'll help me by:
- Creating JSON requests for `my_requests.json` in the "requests" field
- Choosing between local (one-time) or Modal (scheduled) execution
- Explaining what data each request returns
- Telling me the exact command to run

IMPORTANT for Modal requests:
- Ask me if Modal is already deployed
- If YES: tell me to run `modal run src/modal_runner.py::main` (just syncs, no redeploy needed)
- If NO: tell me to run `modal deploy src/modal_runner.py` (first-time setup)

Please read the docs now, then ask me what data I need.
```

---

## 🚀 Quick Start

1. **Open a new chat** in Cursor (or any LLM with file access)
2. **Copy the prompt** above (the entire block inside the backticks)
3. **Paste and send** - the LLM will read all 4 documentation files
4. **Wait for confirmation** - it will say it's ready and ask what you need
5. **Ask in plain English** - e.g., "Get me solar generation in Spain for last week"
6. **Copy the JSON** it generates into `my_requests.json`
7. **Run the command** it tells you (`python -m src.local` or `modal run/deploy`)

---

## 💬 Example Requests

After the LLM reads the docs, try asking:

| What You Say | Type |
|--------------|------|
| "Get day-ahead prices for France for the last week" | Local |
| "I need actual solar generation in Spain" | Local |
| "Show me cross-border flows between Germany and Netherlands" | Local |
| "Get historical load data for Germany" | Local (20 years) |
| "Set up a cron job to collect load in Germany every 2 hours" | Modal |
| "Monitor solar generation in Spain every 6 hours" | Modal |
| "Track cross-border flows France↔Italy continuously" | Modal |

---

## 📁 Output Location

The LLM will generate JSON that you should add to `my_requests.json` in the project root.

### For Local Requests
```bash
python -m src.local
```

Your data will be saved to:
- `results/xml/` - Raw XML responses
- `results/json/` - Parsed JSON data
- `results/csv/` - Tabular CSV data

### For Modal Cron Jobs
```bash
modal deploy src/modal_runner.py
```

Your data will be saved to the `entsoe-fetch` Modal volume with the same structure.

---

## ⚙️ Modal Setup (for Scheduled Fetching)

Before using Modal cron jobs, you need to set up Modal:

### 1. Install Modal CLI
```bash
pip install modal
```

### 2. Authenticate
```bash
modal token new
```
This will open a browser for authentication.

### 3. Create Secret
```bash
modal secret create ENTSOE_API_KEY ENTSOE_API_KEY=<your_api_key>
```
Replace `<your_api_key>` with your actual ENTSO-E API key.

### 4. Deploy (one time only!)
```bash
modal deploy src/modal_runner.py
```

### 5. Monitor
View logs and status at: https://modal.com/apps

---

## 🔄 Adding New Modal Requests (No Redeploy Needed!)

**Important:** Once you deploy `src/modal_runner.py`, you do NOT need to redeploy when adding new requests!

### Workflow:

1. **Add new request** to `my_requests.json` with `"run": "modal"`
2. **Sync to volume** by running:
   ```bash
   modal run src/modal_runner.py::main
   ```
   This uploads `my_requests.json` to the Modal volume AND runs it once.

3. **Or just sync** (without running) using:
   ```bash
   modal run src/modal_runner.py::sync_requests
   ```

4. **The cron job** (already running in the cloud) will automatically pick up the new requests on its next scheduled run.

### Why this works:
- The deployed cron job reads requests from the Modal **volume** (cloud storage)
- When you run `modal run src/modal_runner.py::main`, it syncs your local `my_requests.json` to the volume
- The cron job doesn't need to be redeployed - it will see the updated requests

### When DO you need to redeploy?
- Only when you change the **code** in `src/modal_runner.py` (like modifying the schedule or logic)
- Never for adding/removing requests in `my_requests.json`

---

## 🔧 Troubleshooting

If the LLM generates incorrect requests:

1. **Wrong EIC code**: Ask it to check `docs/api/ENTSOE_EIC_Area_Codes.md`
2. **Wrong document type**: Ask it to check chapter-specific documentation
3. **No data returned**: Ask it to find similar working examples in `docs/examples/request_examples.md`
4. **Parameter errors**: Ask it to verify exact parameter names from the API docs

### Modal-Specific Issues

1. **Secret not found**: Run `modal secret create ENTSOE_API_KEY ENTSOE_API_KEY=<key>`
2. **Volume not created**: Will be created automatically on first run
3. **Deployment fails**: Check Modal dashboard for error logs

---

## 📝 Request Format

### Local Request
```json
{
    "name": "descriptive_name",
    "run": "local",
    "params": {
        "documentType": "A65",
        "processType": "A16",
        "outBiddingZone_Domain": "10YFR-RTE------C",
        "periodStart": "202601010000",
        "periodEnd": "202601080000"
    }
}
```

### Modal Cron Job
```json
{
    "name": "descriptive_name_operational",
    "run": "modal",
    "schedule": "0 */2 * * *",
    "params": {
        "documentType": "A65",
        "processType": "A16",
        "outBiddingZone_Domain": "10YFR-RTE------C"
    }
}
```

**Note**: Modal requests don't need `periodStart`/`periodEnd` - they're calculated automatically.

---

## ⏰ Cron Schedule Reference

| Schedule | Expression |
|----------|------------|
| Every hour | `0 * * * *` |
| Every 2 hours | `0 */2 * * *` |
| Every 6 hours | `0 */6 * * *` |
| Daily at midnight | `0 0 * * *` |
| Every 15 minutes | `*/15 * * * *` |

---

*This tool bridges natural language and the ENTSO-E API, making European electricity data accessible to everyone.*
