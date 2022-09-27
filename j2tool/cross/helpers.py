import os


def ensure_dir(file_path):
    file_dir = os.path.dirname(file_path)
    os.makedirs(file_dir, exist_ok=True)


def ident_text(content: str, ident: int):
    ident_str = " " * ident
    result = ""
    content_lines = content.split("\n")
    for line in content_lines:
        line_ident = ident_str
        if line == "\n":
            line_ident = ""
        result += f"{line_ident}{line}\n"

    return result
