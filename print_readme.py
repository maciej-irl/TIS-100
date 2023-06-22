from pathlib import Path
import re

SEGMENTS = {
    # Row 1
    "00150": "Self-Test Diagnostic",
    "10981": "Signal Amplifier",
    "20176": "Differential Converter",
    "21340": "Signal Comparator",
    "22280": "Signal Multiplexer",
    # Row 2
    "30647": "Sequence Generator",
    "31904": "Sequence Counter",
    "32050": "Signal Edge Detector",
    "33762": "Interrupt Handler",
    # Row 3
    "40196": "Signal Pattern Detector",
    "41427": "Sequence Peak Decetor",
    "42656": "Sequence Reverser",
    "43786": "Signal Multiplier",
    # Row 4
    "50370": "Image Test Pattern 1",
    "51781": "Image Test Pattern 2",
    "52544": "Exposure Mask Viewer",
    "53897": "Histogram Viewer",
    # Row 5
    "60099": "Signal Window Filter",
    "61212": "Signal Divider",
    "62711": "Sequence Indexer",
    "63534": "Sequence Sorter",
    "70601": "Stored Image Decoder",
}


def find_name(save: Path) -> str | None:
    if match := re.search(r"##\s*(.+)", save.read_text()):
        return match[1]


def parse_save_dat() -> dict[str, int]:
    out = {}
    for line in Path("save.dat").read_text().splitlines():
        key, value = line.split(" = ")
        if key not in ("TutorialSeen", "SynchronizationSeen"):
            out[key] = int(value)
    return out


def cin_tuple(save_dat, key) -> str | None:
    if key + ".Cycles" in save_dat:
        cycles = save_dat[key + ".Cycles"]
        nodes = save_dat[key + ".Nodes"]
        insts = save_dat[key + ".Instructions"]
        return f"{cycles} / {nodes} / {insts}"


def print_listing():
    save_dat = parse_save_dat()
    for segment, segment_name in SEGMENTS.items():
        print()
        print(f"### {segment} {segment_name}")

        if best_cin := cin_tuple(save_dat, f"Best.{segment}"):
            print(f"**Best** — {best_cin}  ")

        saves = sorted(Path("save/").glob(f"{segment}.*.txt"))
        for save in saves:
            program = save.stem.split(".")[1]
            line = f"[Program {program}]({save})"
            if cin := cin_tuple(save_dat, f"Last.{segment}.{program}"):
                line += f" — {cin}"
            else:
                line += f" — Incomplete"
            if name := find_name(save):
                line += f" — “{name}”  "
            print(line + "  ")

        if not saves:
            print("**To Be Solved**")


def main():
    print(Path("readme_intro.md").read_text(), end="")
    print_listing()


if __name__ == "__main__":
    main()
