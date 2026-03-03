from pathlib import Path

outputDir = ""

output_path = Path(outputDir) / "combine.py"

with output_path.open("w") as f:
    f.write("It bloody works")
