from pathlib import Path

outputDir = ""

output_file = Path(outputDir) / "hello_world.py"

with output_file.open("w") as f:
    f.write("hello world")

    



