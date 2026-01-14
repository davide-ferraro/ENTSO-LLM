
import re
from pathlib import Path

source_file = Path("docs/api/ENTSOE_Transparency_API_Documentation.md")
output_dir = Path("docs/api/endpoints_doc")
output_dir.mkdir(parents=True, exist_ok=True)

content = source_file.read_text(encoding="utf-8")

# 1. Extract Chapter 1 (Introduction)
# It ends before "## Chapter 2: Market"
intro_match = re.search(r"(.*)(?=## Chapter 2: Market)", content, re.DOTALL)
if intro_match:
    intro_text = intro_match.group(1).strip()
    (Path("docs/api/CommonDefinitions.md")).write_text(intro_text, encoding="utf-8")
    print("Created CommonDefinitions.md")

# 2. Split Endpoints
# Look for headers like: #### 2.2.1 Congestion Income (12.1.E)
# Regex: ####\s+(\d+\.\d+\.\d+)\s+(.*?)\s+\((.*?)\)  -- logic might be simpler
# Let's just split by #### header
parts = re.split(r'(?=#### \d+\.\d+\.\d+ )', content)

for part in parts:
    part = part.strip()
    if not part.startswith("#### "):
        continue

    # Extract Title for filename
    # Line 1: #### 2.2.1 Congestion Income (12.1.E)
    first_line = part.split("\n")[0]
    
    # Clean up title: "Congestion Income"
    # match = re.search(r"#### \d+\.\d+\.\d+\s+(.*?)\s+\(", first_line)
    # simpler: just take the text after the number
    match = re.search(r"#### \d+\.\d+\.\d+\s+(.*)", first_line)
    if match:
        raw_title = match.group(1).strip()
        # Remove reference like (12.1.E)
        title = re.sub(r"\s*\(.*?\)$", "", raw_title).strip()
        
        # Safe filename
        safe_title = re.sub(r"[^a-zA-Z0-9]+", "_", title).lower()
        filename = f"{safe_title}.md"
        
        (output_dir / filename).write_text(part + "\n", encoding="utf-8")
        print(f"Created {filename}")

print("Done splitting API docs.")
