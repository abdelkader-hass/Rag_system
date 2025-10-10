import streamlit as st
import requests
import pymupdf4llm
from werkzeug.utils import secure_filename
# --- CONFIGURATION ---
API_URL = "http://localhost:5009/add_file"  # Change this to your Flask server URL
API_URL_context="http://localhost:5009/get_context"
import fitz
import re,os


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
    device = st.selectbox(
        "Device model",
        options=["EL200", "C500"],
        index=0
    )
    use_categories=st.toggle("Use categories")

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
                "chunk_length": str(chunk_length),
                "device":str(device),
                
            }
            if use_categories:
                data['categories']="general information,installation,Troubleshooting,update"
            
            with st.spinner("Uploading file and waiting for response..."):
                response = requests.post(API_URL, files=files, data=data)

            if response.ok:
                st.success("✅ File successfully uploaded!")
                st.text_area("Server Response", response.text, height=200)
            else:
                st.error(f"❌ Error {response.status_code}")
                st.text_area("Server Response", response.text, height=200)



                # filename = secure_filename(uploaded_file.filename)
                # uploaded_file.save(os.path.join("temp.pdf", filename))

                # doc = fitz.open(pdf_path)
                
                # markdown_content=get_markdown(doc=doc)
                # # markdown_content = pymupdf4llm.to_markdown(doc="temp.pdf",page_separators=True,table_strategy="lines",write_images=True,image_path="img_pd")
                # markdown_content=markdown_content.replace("|"," ").replace("</br>","\n").strip()

                # chunks=split_by_headers_and_bolds(markdown_content,chunk_size=1000)
                # final_chunks=get_formated_chunks(chunks,n=300,doc_name=uploaded_file.name,min_words_merge=20)
                # st.write(final_chunks)


        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")


st.markdown("""
Use this page to send test queries to your Flask `/get_context` endpoint.
""")

# --- INPUT FIELDS ---
question = st.text_area("📝 Enter your question:", height=100, placeholder="Type your question here...")
type_search = st.selectbox("🔎 Type of search:", ["smart", "similarity"])
Node_id = st.text_input("🧩 Node ID (optional):", placeholder="e.g. ROOT-001-124")
use_device=st.toggle("use device")
# --- BUTTON TO SEND REQUEST ---
if st.button("🚀 Send Request"):
    if not question.strip():
        st.error("Please enter a question before sending.")
    else:
        try:
            data = {
                "question": question,
                "type_search": type_search,
                "Node_id": Node_id,
            }

            if use_device:
                data["device"]=device
            with st.spinner("Contacting Flask API..."):
                response = requests.post(API_URL_context, data=data)

            if response.ok:
                st.success("✅ Request successful!")
                # Try to pretty-print JSON if possible
                try:
                    json_response = response.json()
                    st.json(json_response)
                except Exception:
                    st.text_area("Response Text:", response.text, height=300)
            else:
                st.error(f"❌ Error {response.status_code}")
                st.text_area("Server Response:", response.text, height=300)

        except Exception as e:
            st.error(f"⚠️ Error connecting to API: {e}")

