
import re
from pathlib import Path

source_file = Path("docs/examples/request_examples.md")
output_dir = Path("docs/examples/endpoints")
output_dir.mkdir(parents=True, exist_ok=True)

content = source_file.read_text(encoding="utf-8")

# Split by the header pattern
# We use a lookahead to keep the delimiter in the split or just re-add it
parts = re.split(r'(?=## 📋 Endpoint )', content)

for part in parts:
    part = part.strip()
    if not part.startswith("## 📋 Endpoint"):
        continue

    # Extract endpoint number
    match = re.search(r"Endpoint (\d+):", part)
    if match:
        num = int(match.group(1))
        filename = f"E{num:02d}.md"
        
        # Write to file
        (output_dir / filename).write_text(part + "\n", encoding="utf-8")
        print(f"Created {filename}")

print("Done splitting.")
