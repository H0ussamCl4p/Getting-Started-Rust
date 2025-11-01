import os

README_PATH = "README.md"
EXCLUDED = {".git", "target", "__pycache__", "update_readme.py"}

def get_projects():
    projects = []
    for entry in sorted(os.listdir(".")):
        if os.path.isdir(entry) and entry not in EXCLUDED:
            if os.path.exists(os.path.join(entry, "Cargo.toml")):
                projects.append(entry)
    return projects

def extract_description(project):
    main_rs = os.path.join(project, "src", "main.rs")
    if os.path.exists(main_rs):
        with open(main_rs, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Look for a comment on the first few lines
                if line.startswith("//"):
                    return line.lstrip("/ ").strip()
                elif line != "":
                    break  # stop if we hit code before a comment
    return "Description coming soon"

def generate_table(projects):
    lines = ["| # | Project | Description |", "|:-:|:--|:--|"]
    for i, name in enumerate(projects, 1):
        desc = extract_description(name)
        lines.append(f"| {i} | [`{name}`](./{name}) | {desc} |")
    return "\n".join(lines)

def update_readme(projects):
    if not os.path.exists(README_PATH):
        print("No README.md found, creating a new one.")
        with open(README_PATH, "w") as f:
            f.write("# 🦀 Getting Started with Rust\n\n")

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "## 📚 Exercises"
    end_marker = "## 🧰 Tools & Setup"

    table = generate_table(projects)
    section = f"{start_marker}\n\n{table}\n\n"

    if start_marker in content:
        # Replace existing section or append new
        parts = content.split(start_marker)
        before = parts[0]
        after = parts[1] if len(parts) > 1 else ""
        new_content = before + section + after
    else:
        new_content = content + "\n" + section

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("✅ README.md updated successfully!")

if __name__ == "__main__":
    projects = get_projects()
    update_readme(projects)
