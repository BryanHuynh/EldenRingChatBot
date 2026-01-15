def append_h4_to_subheaders(text: str) -> str:
    h2_found = None
    h4_found = None
    footer_found = False
    split_text = text.split("\n")

    for i, line in enumerate(split_text):  # Use enumerate to get index
        if not line.startswith("#"):
            continue
        
        if footer_found and not line.startswith("#### "):
            h2_found = None
            h4_found = None
            footer_found = False
        
        if line.startswith("## "):
            h2_found = line
            h4_found = None
            continue
        
        if line.startswith("#### ") and h2_found is not None and h4_found is None:
            h4_found = line.lstrip("####").strip()
            continue
        
        if line.startswith("#### ") and h2_found is not None and h4_found is not None:
            footer_found = True
            split_text[i] = f"{line} ({h4_found})"
            continue
        
        if h2_found is not None and h4_found is None:
            h2_found = None
            continue
        
        if line.startswith("#") and h2_found is not None and h4_found is not None:
            if line.endswith(f"({h4_found})"):
                continue
            split_text[i] = f"{line} ({h4_found})"

    return "\n".join(split_text)