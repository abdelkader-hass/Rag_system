def split_by_headers_and_bolds(markdown_text: str, chunk_size: int = 150,min_size=15):
    """
    Dynamically split markdown text by header levels (#, ##, ###, …),
    then split each section by bold titles (**Title**),
    and merge small chunks (only within the same section hierarchy).
    """

    # -------------------------------------------------------------
    # Step 1: Detect max header level dynamically
    # -------------------------------------------------------------
    header_level_matches = re.findall(r"^(#+)\s+.+$", markdown_text, flags=re.MULTILINE)
    max_level = max((len(m) for m in header_level_matches), default=1)
    level_keys = [f"lv{i}" for i in range(1, max_level + 1)]

    # Build a regex that matches up to the detected number of levels
    header_pattern = re.compile(r"^(#{1," + str(max_level) + r"})\s+(.+)$")

    # -------------------------------------------------------------
    # Step 2: Split into sections by headers
    # -------------------------------------------------------------
    lines = markdown_text.splitlines()
    sections = []
    current_section = {key: None for key in level_keys}
    current_section["content"] = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        header_match = header_pattern.match(line)
        if header_match:
            level = len(header_match.group(1))
            title = header_match.group(2).strip()

            # Save current section if it has accumulated content
            if current_section["content"]:
                sections.append(current_section)
                current_section = current_section.copy()
                current_section["content"] = []

            # Reset deeper levels
            for i in range(level, max_level + 1):
                current_section[f"lv{i}"] = None

            # Assign the title at its level
            current_section[f"lv{level}"] = title
        else:
            current_section["content"].append(line)

    if current_section["content"]:
        sections.append(current_section)

    # -------------------------------------------------------------
    # Step 3: Split each section by bold titles
    # -------------------------------------------------------------
    def split_bold_lines(text_lines):
        chunks = []
        current_title = None
        current_text = []
        bold_title_pattern = re.compile(r"^\s*(\*\*.+?\*\*)(\s*\*\*.+?\*\*)*\s*$")
        for line in text_lines:
            if bold_title_pattern.match(line):
                if current_title or current_text:
                    chunks.append((current_title, current_text))
                current_title = line
                current_text = []
            else:
                current_text.append(line)
        if current_title or current_text:
            chunks.append((current_title, current_text))
        return chunks

    all_chunks = []
    for section in sections:
        section_lines = section["content"]
        bold_chunks = split_bold_lines(section_lines)
        for title, lines_text in bold_chunks:
            text = f"{title}\n" + " ".join(lines_text).strip() if title else " ".join(lines_text).strip()
            word_count = len(re.findall(r"\b\w+\b", text))
            chunk = {
                **{k: section.get(k) for k in level_keys},
                "text": text.strip(),
                "word_count": word_count,
            }
            all_chunks.append(chunk)

    # -------------------------------------------------------------
    # Step 4: Merge small chunks only within the same section hierarchy
    # -------------------------------------------------------------
    def same_section(chunk_a, chunk_b):
        for k in level_keys[:]:
            if chunk_a.get(k) != chunk_b.get(k):
                return False
        return True

    merged_chunks = []
    buffer_text = ""
    buffer_count = 0
    buffer_section = None

    for chunk in all_chunks:
        if not buffer_text:
            buffer_text = chunk["text"]
            buffer_count = chunk["word_count"]
            buffer_section = {k: chunk.get(k) for k in level_keys}
        else:
            if ((buffer_count + chunk["word_count"] <= chunk_size)  or (buffer_count <min_size or chunk["word_count"]<min_size))  and same_section(chunk, buffer_section):
                buffer_text += "\n" + chunk["text"]
                buffer_count += chunk["word_count"]
            else:
                merged_chunks.append({
                    "chunk_id": len(merged_chunks) + 1,
                    **buffer_section,
                    "text": buffer_text.strip(),
                    "word_count": buffer_count
                })
                buffer_text = chunk["text"]
                buffer_count = chunk["word_count"]
                buffer_section = {k: chunk.get(k) for k in level_keys}

    if buffer_text:
        merged_chunks.append({
            "chunk_id": len(merged_chunks) + 1,
            **buffer_section,
            "text": buffer_text.strip(),
            "word_count": buffer_count
        })

    return merged_chunks

