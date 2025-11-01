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
                # Take first comment as description
                if line.startswith("//"):
                    return line.lstrip("/ ").strip()
                elif line != "":
                    break  # stop at first non-comment line
    return "Description coming soon"

def generate_table(projects):
    lines = ["| # | Project | Description |", "|:-:|:--|:--|"]
    for i, name in enumerate(projects, 1):
        desc = extract_description(name)
        lines.append(f"| {i} | [`{name}`](./{name}) | {desc} |")
    return "\n".join(lines)

def update_readme(projects):
    # Create README if it doesn't exist
    if not os.path.exists(README_PATH):
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write("# Getting-Started-Rust\n\n## 📚 Exercises\n\n## 🧰 Tools & Setup\n")

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "## 📚 Exercises"
    end_marker = "## 🧰 Tools & Setup"

    table = generate_table(projects)
    section = f"{start_marker}\n\n{table}\n\n"

    # Replace old table between start_marker and end_marker
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
