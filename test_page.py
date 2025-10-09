import streamlit as st
import requests
import pymupdf4llm
# --- CONFIGURATION ---
API_URL = "http://localhost:5009/add_file"  # Change this to your Flask server URL


import fitz

import re

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
                'title':str.join("-",[str(section.get(k)) for k in level_keys]).replace("None",""),
                'title_':[str(section.get(k)) for k in level_keys]
            }
            all_chunks.append(chunk)

    # -------------------------------------------------------------
    # Step 4: Merge small chunks only within the same section hierarchy
    # -------------------------------------------------------------
    def same_section(chunk_a, chunk_b):
        for k in level_keys[:-1]:
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
            # (buffer_count <min_size or chunk["word_count"]<min_size)
            if ((buffer_count + chunk["word_count"] <= chunk_size) )  and same_section(chunk, buffer_section):
                if chunk["title_"][-1]!="None":
                    buffer_text += "\n" +chunk["title_"][-1]+"\n"+chunk["text"]
                else:
                    buffer_text+= "\n" +chunk["text"]
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

# --- PAGE SETUP ---
st.set_page_config(page_title="File Uploader", page_icon="📂", layout="centered")
st.title("📂 Upload a File to Flask API")

st.markdown("""
This Streamlit interface allows you to upload a file and send it to the Flask endpoint  
**`/add_file`** for processing.
""")

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Select a file", type=["pdf","docx", "csv", "json", "md", "html"])

# --- FORM PARAMETERS ---
st.subheader("Optional Parameters")

col1, col2 = st.columns(2)
with col1:
    split_type = st.selectbox(
        "Split Type",
        options=["smart", "standard",],
        index=0
    )

with col2:
    use_md = st.selectbox(
        "Use Markdown Parsing",
        options=["True", "False"],
        index=0
    )

chunk_length = st.number_input("Chunk Length (words)", min_value=100, max_value=5000, value=1000, step=100)

# --- SEND FILE ---
if st.button("🚀 Upload and Process"):
    if uploaded_file is None:
        st.error("Please upload a file first.")
    else:
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            data = {
                "split_type": split_type,
                "use_md": use_md,
                "chunk_length": str(chunk_length)
            }

            with st.spinner("Uploading file and waiting for response..."):
                # response = requests.post(API_URL, files=files, data=data)
                with open("temp.pdf", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                import fitz  # PyMuPDF
                import os
                import re

                pdf_path = "temp.pdf"
                md_output = "example.md"
                image_folder = "pdf_images"

                os.makedirs(image_folder, exist_ok=True)
                doc = fitz.open(pdf_path)


                def sort_blocks(blocks):
                    """Sort top-to-bottom, then left-to-right (handles multi-column layout)."""
                    return sorted(blocks, key=lambda b: (b["bbox"][1], b["bbox"][0]))


                def is_table_block(block):
                    """Heuristic to detect if a text block looks like a table (many spaces)."""
                    lines = block.get("lines", [])
                    if len(lines) < 2:
                        return False
                    avg_chars = sum(len(" ".join(span["text"] for span in line["spans"])) for line in lines) / len(lines)
                    avg_spaces = sum(" ".join(span["text"] for span in line["spans"]).count(" ") for line in lines) / len(lines)
                    return avg_spaces > avg_chars * 0.2  # e.g., 20% spaces → likely table


                def map_font_sizes_to_headers(doc):
                    """Collect all font sizes and map to Markdown header levels."""
                    sizes = set()
                    for page in doc:
                        for block in page.get_text("dict")["blocks"]:
                            if block["type"] == 0:
                                for line in block["lines"]:
                                    for span in line["spans"]:
                                        sizes.add(round(span["size"], 1))

                    sorted_sizes = sorted(sizes, reverse=True)
                    header_map = {}
                    for i, size in enumerate(sorted_sizes):
                        if size < 12:
                            header_map[size] = ""  # no header
                        else:
                            header_map[size] = "#" * (i + 1)  # larger size = fewer #
                    return header_map


                header_map = map_font_sizes_to_headers(doc)

                with open(md_output, "w", encoding="utf-8") as f_md:
                    for page_num, page in enumerate(doc, start=1):
                        blocks = sort_blocks(page.get_text("dict")["blocks"])
                        used_xrefs = set()

                        for b in blocks:
                            # --- TEXT BLOCK ---
                            if b["type"] == 0:
                                if is_table_block(b):
                                    # Treat as table → single line, columns separated by |||
                                    for line in b.get("lines", []):
                                        line_text = re.sub(r"\s{2,}", "|||", " ".join(span["text"] for span in line["spans"]))
                                        line_text = re.sub(r"\|\|\|\|+", "|||", line_text)
                                        if line_text.strip():
                                            f_md.write(line_text.strip() + "\n")
                                    f_md.write("\n")
                                else:
                                    # Regular text block
                                    for line in b.get("lines", []):
                                        line_text_parts = []
                                        for span in line["spans"]:
                                            fontname = span.get("font", "").lower()
                                            size = round(span.get("size", 0), 1)
                                            text = span["text"].strip()

                                            if not text:
                                                continue

                                            # Handle bold text
                                            if "bold" in fontname:
                                                text = f"**{text}**"

                                            # Handle headers by font size
                                            header_prefix = header_map.get(size, "")
                                            if header_prefix and len(text)>2 and "bold" in fontname:
                                                text = f"{header_prefix} {text}"

                                            line_text_parts.append(text)

                                        line_text = " ".join(line_text_parts).strip()
                                        if line_text:
                                            f_md.write(line_text + "\n\n")

                            # --- IMAGE BLOCK ---
                            elif b["type"] == 1:
                                for img in page.get_images(full=True):
                                    xref = img[0]
                                    if xref in used_xrefs:
                                        continue
                                    base_image = doc.extract_image(xref)
                                    image_bytes = base_image["image"]
                                    ext = base_image["ext"]
                                    image_filename = os.path.join(image_folder, f"page{page_num}_{xref}.{ext}")
                                    with open(image_filename, "wb") as img_file:
                                        img_file.write(image_bytes)
                                    f_md.write(f"![image_{xref}]({image_filename})\n\n")
                                    used_xrefs.add(xref)
                                    break

                        f_md.write("\n---\n\n")  # page separator

                with open("example.md","r",encoding="utf-8") as e:
                    markdown_content=e.read()
                # markdown_content = pymupdf4llm.to_markdown(doc="temp.pdf",page_separators=True,table_strategy="lines",write_images=True,image_path="img_pd")
                markdown_content=markdown_content.replace("|"," ").replace("</br>","\n").strip()
                with open("tt.md","w",encoding="utf-8") as e:
                    e.write(markdown_content)
                chunks=split_by_headers_and_bolds(markdown_content)
                st.write(chunks)
            # if response.ok:
            #     st.success("✅ File successfully uploaded!")
            #     st.text_area("Server Response", response.text, height=200)
            # else:
            #     st.error(f"❌ Error {response.status_code}")
            #     st.text_area("Server Response", response.text, height=200)

        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")
