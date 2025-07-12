import os

def load_corrections(filepath):
    corrections = {}
    if not os.path.exists(filepath):
        return corrections
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().lower().split("=", 1)
                corrections[k.strip()] = v.strip()
    return corrections

def normalize_text(text, corrections):
    lowered = text.lower()
    for alt, canonical in corrections.items():
        if alt in lowered:
            lowered = lowered.replace(alt, canonical)
    return lowered