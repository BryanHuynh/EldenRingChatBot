def remove_empty_sections(text: str) -> str:
    lines = text.split("\n")
    for i in range(len(lines)):
        if lines[i].startswith("#"):
            header_end_index = i
            empty_check = True
            for j in range(i + 1, len(lines)):
                header_end_index = j
                if lines[j] == "\n" or lines[j].strip() == "":
                    continue
                elif lines[j].startswith("#"):
                    break
                else:
                    empty_check = False
                    break
            if empty_check:
                for j in range(i, header_end_index):
                    lines[j] = ""
    return "\n".join(lines)



        