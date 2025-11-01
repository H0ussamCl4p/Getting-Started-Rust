import os
import re

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
                if line.startswith("//"):
                    return line.lstrip("/ ").strip()
                elif line != "":
                    break
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
    
    table = generate_table(projects)
    
    # Check if "## 📚 Exercises" section exists
    if "## 📚 Exercises" in content and "## 🧰 Tools & Setup" in content:
        # Replace content between the two headers
        pattern = r"(## 📚 Exercises\n\n).*?(## 🧰 Tools & Setup)"
        replacement = f"\\1{table}\n\n\\2"
        content_final = re.sub(pattern, replacement, content, flags=re.DOTALL)
    elif "## 📚 Exercises" in content:
        # Only Exercises section exists, replace everything after it
        pattern = r"(## 📚 Exercises\n\n).*"
        replacement = f"\\1{table}\n"
        content_final = re.sub(pattern, replacement, content, flags=re.DOTALL)
    else:
        # No Exercises section, add it before Tools & Setup or at the end
        if "## 🧰 Tools & Setup" in content:
            content_final = content.replace(
                "## 🧰 Tools & Setup",
                f"## 📚 Exercises\n\n{table}\n\n## 🧰 Tools & Setup"
            )
        else:
            content_final = content + f"\n## 📚 Exercises\n\n{table}\n"
    
    with open(README_PATH, "w", encoding="utf-8", newline='') as f:
        f.write(content_final)
    
    print(f"✅ README.md updated successfully! {len(projects)} project(s) listed.")

if __name__ == "__main__":
    projects = get_projects()
    if projects:
        update_readme(projects)
        print(f"Found projects: {', '.join(projects)}")
    else:
        print("⚠️ No Rust projects found in current directory.")