"""Rebuild the README index from the Markdown notes in each topic folder."""
import pathlib, re, subprocess

root = pathlib.Path(__file__).parent
skip = {"README.md", "TEMPLATE.md"}

def created(path):
    out = subprocess.run(["git", "log", "--diff-filter=A", "--format=%as", "--", str(path)],
                         capture_output=True, text=True, cwd=root).stdout.split()
    return out[-1] if out else ""

SEASON = {"early": "03", "mid": "06", "late": "10"}

def learned(text):
    m = re.search(r"_Learned:\s*([^_]+)_", text)
    if not m:
        return "", ""
    label = m.group(1).strip()
    d = re.search(r"(\d{4})-(\d{2})(?:-(\d{2}))?", label)
    if d:
        return label, d.group(0)
    y = re.search(r"(\d{4})", label)
    w = re.search(r"(early|mid|late)", label, re.I)
    key = f"{y.group(1)}-{SEASON[w.group(1).lower()] if w else '06'}" if y else ""
    return label, key

notes = []
for p in sorted(root.glob("*/*.md")):
    if p.name in skip or p.parts[-2].startswith("."):
        continue
    first = p.read_text(encoding="utf-8").splitlines()[0] if p.read_text(encoding="utf-8").strip() else p.stem
    title = first.lstrip("# ").strip()
    label, key = learned(p.read_text(encoding="utf-8"))
    notes.append((p.parent.name, title, p.relative_to(root).as_posix(), key or created(p), label or created(p)))

lines = [f"**{len(notes)} note{'' if len(notes) == 1 else 's'} so far.**", ""]
recent = sorted(notes, key=lambda n: n[3], reverse=True)[:5]
if recent:
    lines += ["## Most recent", ""] + [f"- [{t}]({u}) · {topic} · {lbl}" for topic, t, u, d, lbl in recent] + [""]
for topic in sorted({n[0] for n in notes}):
    lines += [f"## {topic}", ""]
    lines += [f"- [{t}]({u}) · {lbl}" for tp, t, u, d, lbl in sorted(notes, key=lambda n: n[3]) if tp == topic]
    lines.append("")

readme = root / "README.md"
text = readme.read_text(encoding="utf-8")
new = re.sub(r"<!-- index starts -->.*<!-- index ends -->",
             "<!-- index starts -->\n" + "\n".join(lines) + "\n<!-- index ends -->", text, flags=re.S)
readme.write_text(new, encoding="utf-8")
