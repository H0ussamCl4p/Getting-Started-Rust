import os

README_PATH = "README.md"
EXCLUDED = {".git", "target", "__pycache__"}

def get_projects():
    projects = []
    for entry in sorted(os.listdir(".")):
        if os.path.isdir(entry) and entry not in EXCLUDED:
            if os.path.exists(os.path.join(entry, "Cargo.toml")):
                projects.append(entry)
    return projects

def generate_table(projects):
    lines = ["| # | Project | Description |", "|:-:|:--|:--|"]
    for i, name in enumerate(projects, 1):
        lines.append(f"| {i} | [`{name}`](./{name}) | Description coming soon |")
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

    if start_marker in content and end_marker in content:
        before = content.split(start_marker)[0]
        after = content.split(end_marker)[1]
        new_content = before + section + end_marker + after
    else:
        new_content = content + "\n" + section

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("✅ README.md updated successfully!")

if __name__ == "__main__":
    projects = get_projects()
    update_readme(projects)
