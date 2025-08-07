import subprocess
from pathlib import Path

# === CONFIGURATION ===
input_font = "ChillJinshuMinchoJPCompactRegular.otf"           # Replace with your input font file
unicode_list_file = "unicodes.txt"     # List of codepoints like 0x0041
output_base = "trimmed-font"           # Output name prefix
char_file = "unicodes_chars.txt"       # Temp file with characters

# === Step 1: Convert 0x... to real characters ===
with open(unicode_list_file, "r", encoding="utf-8") as f:
    codepoints = [line.strip() for line in f if line.strip()]

try:
    characters = "".join([chr(int(cp, 16)) for cp in codepoints])
except ValueError as e:
    print(f"❌ Error converting Unicode values: {e}")
    exit(1)

with open(char_file, "w", encoding="utf-8") as f:
    f.write(characters)
print(f"✅ Wrote characters to '{char_file}'")

# === Step 2: Export OTF ===
subset_otf_cmd = [
    "pyftsubset",
    input_font,
    f"--text-file={char_file}",
    f"--output-file={output_base}.otf",
    "--glyph-names",
    "--symbol-cmap",
    "--legacy-cmap",
    "--notdef-glyph",
    "--notdef-outline",
    "--recommended-glyphs",
    "--name-IDs=*",
    "--name-legacy",
    "--name-languages=*",
    "--drop-tables+=DSIG",  # Remove digital signature
]

print("🔧 Subsetting to OTF...")
result_otf = subprocess.run(subset_otf_cmd, capture_output=True, text=True)
if result_otf.returncode != 0:
    print("❌ Error creating OTF:")
    print(result_otf.stderr)
    exit(1)
print(f"✅ Created valid OTF: '{output_base}.otf'")

# === Step 3: Export WOFF2 ===
subset_woff2_cmd = [
    "pyftsubset",
    input_font,
    f"--text-file={char_file}",
    f"--output-file={output_base}.woff2",
    "--flavor=woff2",
    "--drop-tables+=DSIG",
    "--no-hinting",
]

print("🔧 Subsetting to WOFF2...")
result_woff2 = subprocess.run(subset_woff2_cmd, capture_output=True, text=True)
if result_woff2.returncode != 0:
    print("❌ Error creating WOFF2:")
    print(result_woff2.stderr)
    exit(1)
print(f"✅ Created valid WOFF2: '{output_base}.woff2'")

# === Cleanup ===
try:
    Path(char_file).unlink()
except Exception:
    pass

print("\n🎉 Done! You can now use the fonts.")
