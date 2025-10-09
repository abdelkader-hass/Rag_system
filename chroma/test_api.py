import streamlit as st
import requests

# Your Flask API base URL
API_BASE = "http://localhost:5009"  # change if deployed elsewhere

# ---------------- Streamlit UI ---------------- #
st.title("📄 PDF System Client")

# Upload file section
st.header("Upload a File")
uploaded_file = st.file_uploader("Choose a PDF", type=["pdf","csv"])

if uploaded_file is not None:
    if st.button("Upload to Server"):
        try:
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(f"{API_BASE}/add_file", files={"file": (uploaded_file.name, uploaded_file.getvalue())})
            
            if response.status_code == 200:
                st.success(response.text)
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")


# Get context section
st.header("Get Context")
question = st.text_input("Enter your question")
k = st.number_input("k (default = 10)", min_value=1, value=10)
n = st.number_input("n (default = 2)", min_value=1, value=2)



if st.button("Get Context"):
    if not question:
        st.warning("⚠️ Please enter a question.")
    else:
        try:
            data = {"question": question, "k": k, "n": n,"type_kb":"kB_text"}
            response = requests.post(f"{API_BASE}/get_context", data=data)
            
            if response.status_code == 200:
                st.text_area("Context Result", response.text, height=200)
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")
        try:
            data = {"question": question, "k": k, "n": n,"type_kb":"KB_QA"}
            response = requests.post(f"{API_BASE}/get_context", data=data)
            
            if response.status_code == 200:
                st.text_area("Context Result", response.text, height=200)
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")


page_id = st.number_input("page id", min_value=0, value=1)
pdf_name=st.text_input("pdf name")
if st.button("Get chunkes in page"):
        try:
            data = {"pdf_name": pdf_name, "page_id": page_id}
            response = requests.post(f"{API_BASE}/get_chunks_inpage", data=data)
            
            if response.status_code == 200:
                st.text_area("Context Result", response.text, height=200)
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")