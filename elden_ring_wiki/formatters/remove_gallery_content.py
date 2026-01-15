def remove_gallery_content(text: str) -> str:
    lines = text.split("\n")
    gallery_found = False
    for i, line in enumerate(lines):
        if line.startswith("#"):
            header_words = line.lower().split(" ")
            if len(header_words) > 1 and "gallery" in header_words:
                gallery_found = True
                lines[i] = ""
                continue
        if gallery_found:
            if line.startswith("#"):
                gallery_found = False
            else:
                lines[i] = ""
    return "\n".join(lines)