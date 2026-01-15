def remove_video_guide(text: str) -> str:
    lines = text.split("\n")
    video_guide_found = False
    for i, line in enumerate(lines):
        if line.startswith("#"):
            header_words = line.lower().split(" ")
            if len(header_words) > 1 and "video" in header_words:
                video_guide_found = True
                lines[i] = "\n"
        if video_guide_found:
            if line.startswith("#"):
                video_guide_found = False
            lines[i] = "\n"
    return "\n".join(lines)