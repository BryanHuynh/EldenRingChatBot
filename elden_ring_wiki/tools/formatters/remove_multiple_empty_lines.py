def remove_multiple_empty_lines(text: str) -> str:
    lines = text.split("\n")
    result = []
    prev_empty = False
    
    for line in lines:
        is_empty = line.strip() == ''
        
        # Skip if this is an empty line and previous was also empty
        if is_empty and prev_empty:
            continue
            
        result.append(line)
        prev_empty = is_empty
    return "\n".join(result)