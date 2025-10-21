import pymupdf4llm
import re
import os,io
import uuid
import fitz
from .static_var import IMAGES_PATH,DOCUMENT_PATH,TEMP_MD_PATH
from PIL import Image

def markdown_tree(md_text):
    try :
        with open("t.md","w") as e:
            e.write(md_text)
        lines = md_text.splitlines()
        heading_regex = re.compile(r'^(#{1,6})\s+(.*)')
        bold_line_regex = re.compile(r'^\s*(?:\*\*|__)([^*]+?)(?:\*\*|__)\s*$')

        # Step 1: Find all headings
        sections = []
        headings_found = False

        for idx, line in enumerate(lines):
            match = heading_regex.match(line)
            if match:
                headings_found = True
                level = len(match.group(1))
                title = match.group(2).strip()
                sections.append({"index": idx, "title": title, "level": level})
        

        if not headings_found:
            full_text = md_text.strip()
            root = {
                "id": str(uuid.uuid4()),
                "title": "Full Text",
                "level": 0,
                "text": full_text,
                "children": []
            }
            return False,[],full_text

        # Step 4: Extract section texts by slicing lines between indices
        for i in range(len(sections)):
            start = sections[i]["index"]
            end = sections[i + 1]["index"] if i + 1 < len(sections) else len(lines)
            # Text is lines between heading line +1 and next heading start
            sections[i]["text"] = "\n".join(lines[start + 1:end]).strip()

        # Step 5: Build hierarchical tree using stack
        tree = []
        stack = []
        Titles=[]
        data={}
        cpt=0
        for section in sections:
            # str(uuid.uuid4())
            node = {
                "id": str(cpt),
                "title": section["title"],
                "text": section["text"],
                "level": section["level"],
                "children": []
            }
            Titles.append((cpt,section["title"]))

            data[cpt]=[section["title"],section["text"]]
            while stack and stack[-1]["level"] >= section["level"]:
                stack.pop()
            if stack:
                stack[-1]["children"].append(node)
            else:
                tree.append(node)

            stack.append(node)
            cpt+=1
        
        return True,Titles,stack
    except:
        return False,None,None

def read_pdf(file_path):
    doc = fitz.open(file_path)

    return doc
def read_other(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def read_file(file_name,documents_folder=DOCUMENT_PATH,is_md="True",chunk_length=1000,part_size=300):
    file_path=os.path.join(f"{documents_folder}",file_name)
    ext = os.path.splitext(file_name)[1].lower() 
    if ext in ['.pdf','.txt']  :
        doc=read_pdf(file_path)
        if is_md=="True":
            markdown_content=get_markdown(doc=doc,md_output=TEMP_MD_PATH,file_name=file_name)
            markdown_content=markdown_content.replace("|"," ").replace("</br>","\n").strip()
            chunks=split_by_headers_and_bolds(markdown_content,chunk_size=chunk_length)
            final_chunks=get_formated_chunks(chunks,n=part_size,doc_name=file_name,min_words_merge=20)
            return final_chunks
            
    else:
        return []
        # text=read_other(file_path)
        # return text


#-----------------------new methode


import re
import os
import math 

# md_output = "{DOCUMENT_PATH}/example.md"
image_folder = IMAGES_PATH


def split_by_headers_and_bolds(markdown_text: str, chunk_size: int = 300,min_size=15):
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
            # print("type1",type(buffer_count),type(chunk_size),type(chunk["word_count"]))
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


def save_md_temp_old(md_output="temp.md",doc=None,file_name=None):
    if file_name:
        file_name= file_name.replace(".","ext!")
    else:
        file_name=""
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
                        image_name=f"{file_name}_page{page_num}_{xref}.png"
                        image_filename = os.path.join(image_folder,image_name)
                        with open(image_filename, "wb") as img_file:
                            img_file.write(image_bytes)
                        f_md.write(f"![imageurl:{image_name}]\n\n")
                        used_xrefs.add(xref)
                        break

            f_md.write("\n---\n\n")  # page separator

def save_md_temp(md_output="temp.md", doc=None, file_name=None):
    if file_name:
        file_name = file_name.replace(".", "ext!")
    else:
        file_name = ""
    
    header_map = map_font_sizes_to_headers(doc)
    
    with open(md_output, "w", encoding="utf-8") as f_md:

        for page_num, page in enumerate(doc, start=1):

            blocks = sort_blocks(page.get_text("dict")["blocks"])
            # blocks = page.get_text("dict")["blocks"]

            used_xrefs = set()
            DPI = 150

            current_image_block = []

            for block_id,b in enumerate(blocks):
                # --- TEXT BLOCK ---
                if b["type"] == 0:
                    # Save current image block if any
                    line_out=""
                    line_out_img=""
                    # --- Process text ---
                    if is_table_block(b):
                        lines=""
                        for line in b.get("lines", []):
                            line_text = re.sub(r"\s{2,}", "|||", " ".join(span["text"] for span in line["spans"]))
                            line_text = re.sub(r"\|\|\|\|+", "|||", line_text)
                            if line_text.strip():
                                lines+=line_text.strip() + "\n"
                        line_out=lines.strip()
                    else:
                        lines=""
                        for line in b.get("lines", []):
                            line_text_parts = []
                            for span in line["spans"]:
                                fontname = span.get("font", "").lower()
                                size = round(span.get("size", 0), 1)
                                text = span["text"].strip()
                                if not text:
                                    continue
                                if "bold" in fontname:
                                    text = f"**{text}**"
                                header_prefix = header_map.get(size, "")
                                if header_prefix and len(text) > 2 and "bold" in fontname:
                                    text = f"{header_prefix} {text}"
                                line_text_parts.append(text)
                            line_text = " ".join(line_text_parts).strip()+"\n"
                            if line_text:
                                lines+="\n"+line_text
                        line_out=lines.strip() + "\n"


                    # print("line,",line_out ,"\n -----s")
                    if current_image_block and len(line_out.strip())>3:
                        # Merge or save single image
                        x0 = min(rect.x0 for _, rect in current_image_block)
                        y0 = min(rect.y0 for _, rect in current_image_block)
                        x1 = max(rect.x1 for _, rect in current_image_block)
                        y1 = max(rect.y1 for _, rect in current_image_block)
                        merged_rect = fitz.Rect(x0, y0, x1, y1)

                        pix = page.get_pixmap(clip=merged_rect, dpi=DPI)
                        if pix.alpha:
                            pix = fitz.Pixmap(fitz.csRGB, pix)
                        img_data = pix.tobytes("png")
                        pil_img = Image.open(io.BytesIO(img_data))
                        if pil_img.mode != 'RGB':
                            pil_img = pil_img.convert('RGB')

                        image_name = f"{file_name}_page{page_num}_block{block_id}.png"
                        image_filename = os.path.join(image_folder, image_name)
                        pil_img.save(image_filename, 'PNG')
                        # f_md.write(f"![imageurl:{image_name}]\n\n")
                        line_out_img=f"![imageurl:{image_name}]\n\n"
                        current_image_block = []

                    f_md.write("\n")

                    if len(line_out.strip())>3:
                        f_md.write(line_out_img)
                        f_md.write(line_out)
                    
                # --- IMAGE BLOCK ---
                elif b["type"] == 1:
                    if "image" in b:  # Some PDFs may store image xref directly
                        xref =b.get('number',())
                        if xref in used_xrefs:
                            continue
                        img_rects =fitz.Rect(*b.get('bbox',()))
                        # Add image to current block
                        current_image_block.append((xref, img_rects))
                        used_xrefs.add(xref)

                else:
                    print("other type",b["type"],b)
            # Save any remaining image block at the end of page
            if current_image_block and len(line_out.strip())>2:
                x0 = min(rect.x0 for _, rect in current_image_block)
                y0 = min(rect.y0 for _, rect in current_image_block)
                x1 = max(rect.x1 for _, rect in current_image_block)
                y1 = max(rect.y1 for _, rect in current_image_block)
                merged_rect = fitz.Rect(x0, y0, x1, y1)

                pix = page.get_pixmap(clip=merged_rect, dpi=DPI)
                if pix.alpha:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                img_data = pix.tobytes("png")
                pil_img = Image.open(io.BytesIO(img_data))
                if pil_img.mode != 'RGB':
                    pil_img = pil_img.convert('RGB')

                image_name = f"{file_name}_page{page_num}_block_{block_id}.png"
                image_filename = os.path.join(image_folder, image_name)
                pil_img.save(image_filename, 'PNG')
                f_md.write(f"![imageurl:{image_name}]\n\n")

            f_md.write("\n---\n\n")  # page separator

def get_markdown(md_output="temp.md",doc=None,file_name=""):
    save_md_temp(doc=doc,md_output=md_output,file_name=file_name)
    with open(md_output,"r",encoding="utf-8") as e:
        markdown_content=e.read()
    return markdown_content


def get_formated_chunks(chunks,n=300,doc_name="",min_words_merge=20):
    result_chunks = []
    for chunk in chunks:
        # Extract titles and merge
        titles = [chunk.get(f'lv{i}') for i in range(1, 10) if chunk.get(f'lv{i}')]
        text = chunk.get('text', '')
        chunk_id = chunk.get('chunk_id')

        # Merge titles except last one
        merged_titles = '!-!'.join(titles[:-1]) if len(titles) > 1 else (titles[0] if titles else '')
        last_title = titles[-1] if titles else ''

        # Full text to consider: last title + text
        full_text = f'{last_title}\n{text}' if last_title else text

        # Count words
        words = re.findall(r'\b\w+\b', full_text)
        total_words = len(words)
        # print("typ2",type(total_words),type(n))

        if total_words <= n:
            result_chunks.append({
                'chunk_id': chunk_id,
                'doc_name': doc_name,
                'titles': merged_titles,
                'text': full_text,
                'word_count': total_words,
                'is_has_other_part': False
            })
        else:
            # Split into balanced parts by lines
            lines = full_text.split('\n')
            num_parts = math.ceil(total_words / n)
            target_words_per_part = math.ceil(total_words / num_parts)

            current_text = ''
            current_words = 0
            temp_chunks = []

            for line in lines:
                line_words = re.findall(r'\b\w+\b', line)
                if current_words + len(line_words) > target_words_per_part and current_text:
                    temp_chunks.append({'text': current_text.strip(), 'word_count': current_words})
                    current_text = ''
                    current_words = 0

                current_text += line + '\n'
                current_words += len(line_words)

            if current_text.strip():
                temp_chunks.append({'text': current_text.strip(), 'word_count': current_words})

            # Further split sentences if needed
            final_chunks = []
            for chunk_part in temp_chunks:
                if chunk_part['word_count'] > n:
                    sentences = re.split(r'(?<=[.!?])\s+', chunk_part['text'])
                    temp_text = ''
                    temp_words = 0
                    for sentence in sentences:
                        sentence_words = re.findall(r'\b\w+\b', sentence)
                        if temp_words + len(sentence_words) > n and temp_text:
                            final_chunks.append({'text': temp_text.strip(), 'word_count': temp_words})
                            temp_text = sentence + ' '
                            temp_words = len(sentence_words)
                        else:
                            temp_text += sentence + ' '
                            temp_words += len(sentence_words)
                    if temp_text.strip():
                        final_chunks.append({'text': temp_text.strip(), 'word_count': temp_words})
                else:
                    final_chunks.append(chunk_part)

            # Merge last chunk if too small or < min_words_merge
            i = len(final_chunks) - 1
            while i > 0 and final_chunks[i]['word_count'] < min_words_merge:
                final_chunks[i-1]['text'] += '\n' + final_chunks[i]['text']
                final_chunks[i-1]['word_count'] += final_chunks[i]['word_count']
                final_chunks.pop(i)
                i -= 1

            # Add to result with proper flags
            for i, fc in enumerate(final_chunks):
                result_chunks.append({
                    'chunk_id': chunk_id,
                    'doc_name': doc_name,
                    'titles': merged_titles,
                    'text': fc['text'],
                    'word_count': fc['word_count'],
                    'is_has_other_part': i < len(final_chunks) - 1
                })

    """
    Refine chunks: merge any chunk with word_count < min_words_merge
    with the next chunk if titles (levels) are the same, else with previous.
    """
    if not chunks:
        return []

    chunks=result_chunks
    refined_chunks = []
    i = 0
    while i < len(chunks):
        current = chunks[i]
        if current['word_count'] < min_words_merge:
            merged = False
            # Try merge with next chunk if titles match
            if i + 1 < len(chunks) and current['titles'] == chunks[i + 1]['titles']:
                next_chunk = chunks[i + 1]
                merged_chunk = {
                    'chunk_id': current['chunk_id'],
                    'doc_name': current['doc_name'],
                    'titles': current['titles'],
                    'text':current['titles']+" \n -----\n"+ current['text'] + '\n' + next_chunk['text'],
                    'word_count': current['word_count'] + next_chunk['word_count'],
                    'is_has_other_part': next_chunk['is_has_other_part']
                }
                refined_chunks.append(merged_chunk)
                i += 2
                merged = True
            # Else try merge with previous chunk if exists
            elif refined_chunks:
                prev_chunk = refined_chunks[-1]
                prev_chunk['text'] += '\n' + current['text']
                prev_chunk['text'] =prev_chunk['titles']+" \n -----\n"+ prev_chunk['text']
                prev_chunk['word_count'] += current['word_count']
                prev_chunk['is_has_other_part'] = current['is_has_other_part']
                i += 1
                merged = True

            # If cannot merge, just keep it
            if not merged:
                current['text'] =current['titles']+" \n -----\n"+ current['text']

                refined_chunks.append(current)
                i += 1
        else:
            current['text'] =current['titles']+" \n -----\n"+ current['text']

            refined_chunks.append(current)
            i += 1

    return refined_chunks




