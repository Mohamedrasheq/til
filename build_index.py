"""Rebuild the README index from the Markdown notes in each topic folder."""
import pathlib, re, subprocess

root = pathlib.Path(__file__).parent
skip = {"README.md", "TEMPLATE.md"}

def created(path):
    out = subprocess.run(["git", "log", "--diff-filter=A", "--format=%as", "--", str(path)],
                         capture_output=True, text=True, cwd=root).stdout.split()
    return out[-1] if out else ""

notes = []
for p in sorted(root.glob("*/*.md")):
    if p.name in skip or p.parts[-2].startswith("."):
        continue
    first = p.read_text(encoding="utf-8").splitlines()[0] if p.read_text(encoding="utf-8").strip() else p.stem
    title = first.lstrip("# ").strip()
    notes.append((p.parent.name, title, p.relative_to(root).as_posix(), created(p)))

lines = [f"**{len(notes)} note{'' if len(notes) == 1 else 's'} so far.**", ""]
recent = sorted(notes, key=lambda n: n[3], reverse=True)[:5]
if recent:
    lines += ["## Latest", ""] + [f"- [{t}]({u}) · {topic} · {d}" for topic, t, u, d in recent] + [""]
for topic in sorted({n[0] for n in notes}):
    lines += [f"## {topic}", ""]
    lines += [f"- [{t}]({u}) · {d}" for tp, t, u, d in sorted(notes, key=lambda n: n[3]) if tp == topic]
    lines.append("")

readme = root / "README.md"
text = readme.read_text(encoding="utf-8")
new = re.sub(r"<!-- index starts -->.*<!-- index ends -->",
             "<!-- index starts -->\n" + "\n".join(lines) + "\n<!-- index ends -->", text, flags=re.S)
readme.write_text(new, encoding="utf-8")
