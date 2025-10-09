import pymupdf4llm
import re
import os
import re
import re
import uuid
import fitz
from .static_var import IMAGES_PATH,DOCUMENT_PATH

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
    markdown_content = pymupdf4llm.to_markdown(doc=file_path,write_images=False,image_path=IMAGES_PATH)
    return markdown_content

def read_other(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def read_file(file_name,documents_folder=DOCUMENT_PATH):
    file_path=os.path.join(f"{documents_folder}",file_name)
    ext = os.path.splitext(file_name)[1].lower() 
    if ext == '.pdf':
        markdown_content=read_pdf(file_path)
        is_Md,titles,data= markdown_tree(markdown_content)
        return is_Md,titles,data
    else:
        text=read_other(file_path)
        return False,"",text

import re

def split_text_smart(text, max_chunk_size=500, overlap=50):
    """
    Split text into chunks without breaking sentences.
    
    Args:
        text (str): The text to split
        max_chunk_size (int): Maximum characters per chunk
        overlap (int): Number of characters to overlap between chunks
    
    Returns:
        list: List of text chunks
    """
    # Split text into sentences using regex
    # This handles periods, exclamation marks, and question marks
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # Check if adding this sentence would exceed the limit
        if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
            # Add sentence to current chunk
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence
        else:
            # Current chunk is ready, start a new one
            if current_chunk:
                chunks.append(current_chunk)
                
                # Handle overlap by taking last part of current chunk
                if overlap > 0 and len(current_chunk) > overlap:
                    overlap_text = current_chunk[-overlap:]
                    # Find the start of the last complete word in overlap
                    last_space = overlap_text.rfind(' ')
                    if last_space != -1:
                        current_chunk = overlap_text[last_space + 1:] + " " + sentence
                    else:
                        current_chunk = sentence
                else:
                    current_chunk = sentence
            else:
                current_chunk = sentence
    
    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks


def split_text_by_paragraphs(text, max_chunk_size=500):
    """
    Alternative approach: Split by paragraphs first, then sentences if needed.
    
    Args:
        text (str): The text to split
        max_chunk_size (int): Maximum characters per chunk
    
    Returns:
        list: List of text chunks
    """
    paragraphs = text.split('\n\n')
    chunks = []
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        if len(paragraph) <= max_chunk_size:
            chunks.append(paragraph)
        else:
            # Paragraph is too long, split by sentences
            para_chunks = split_text_smart(paragraph, max_chunk_size)
            chunks.extend(para_chunks)
    
    return chunks