import streamlit as st
import requests
import json
import litellm
from typing import Optional
from components.static_var import SETTINGS_FILE
from pydantic import BaseModel
# --- CONFIGURATION ---
API_URL = "http://localhost:5009/add_file"
API_URL_context = "http://localhost:5009/get_context"
API_URL_QA = "http://localhost:5009/add_file_QA"

# --- PAGE SETUP ---
st.set_page_config(page_title="File Uploader", page_icon="📂", layout="wide")
st.title("📂 Document Management System")

# --- LOAD DEVICES ---
@st.cache_data
def load_devices():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.warning(f"Could not load devices: {e}")
        return {}

devices_data = load_devices()['devices']
categories_list = load_devices()['categories']
use_categories=load_devices()['use_categories']

# --- TABS ---
# tab1, tab2, tab3 = st.tabs(["📤 Add File", "🔍 Get Context", "💬 Chat"])

tab1, tab3 = st.tabs(["📤 Add File", "💬 Chat"])

    # ============= TAB 1: ADD FILE =============

with tab1:
    st.header("Upload Files")
    
    st.markdown("""
    Upload a file and send it to the Flask endpoint for processing.
    """)
    
    # Q&A Toggle
    is_qa_file = st.toggle("Q&A Files", value=False, help="Enable this if you're uploading Q&A CSV files")
    
    if not is_qa_file:
        # --- REGULAR FILE UPLOAD ---
        st.subheader("Upload Document")
        uploaded_file = st.file_uploader("Select a file", type=["pdf","txt"], key="regular_file")
        
        st.subheader("Optional Parameters")
        col1, col2, col3 = st.columns(3)
        with col1:
            split_type = st.selectbox(
                "Split Type",
                options=["smart", "standard"],
                index=0
            )
        with col2:
            use_md = st.selectbox(
                "Use Markdown Parsing",
                options=["True", "False"],
                index=0
            )
        with col3:
            device = st.selectbox(
                "Device model",
                options=list(devices_data.keys()),
                index=0
            )
        
        chunk_length = st.number_input("Chunk Length (words)", min_value=100, max_value=5000, value=1000, step=50)
        part_size=st.number_input("Chunk Length (words)", min_value=100, max_value=500, value=300, step=50)
        if st.button("🚀 Upload and Process", key="upload_regular"):
            if uploaded_file is None:
                st.error("Please upload a file first.")
            else:
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    data = {
                        "split_type": split_type,
                        "use_md": use_md,
                        "chunk_length": int(chunk_length),
                        "part_size":int(chunk_length),
                        "device": str(device),
                    }
                    if use_categories=="True" and len(categories_list)>2:
                        
                        data['categories'] = categories_list
                        print(categories_list)
                    with st.spinner("Uploading file and waiting for response..."):
                        response = requests.post(API_URL, files=files, data=data)
                    
                    if response.ok:
                        st.success("✅ File successfully uploaded!")
                        st.text_area("Server Response", response.text, height=200)
                    else:
                        st.error(f"❌ Error {response.status_code}")
                        st.text_area("Server Response", response.text, height=200)
                
                except Exception as e:
                    st.error(f"⚠️ An error occurred: {e}")
    
    else:
        # --- Q&A FILE UPLOAD ---
        st.subheader("Upload Q&A File")
        uploaded_file_qa = st.file_uploader("Select a Q&A CSV file", type=["csv"], key="qa_file")
        
        delimiter = st.text_input(
            "Delimiter",
            value=";",
            max_chars=1,
            placeholder='delimiter can be , ; -'
        )
        
        device_qa = st.selectbox(
            "Device model",
            options=list(devices_data.keys()),
            index=0,
            key="device_qa"
        )
        
        if st.button("🚀 Upload Q&A and Process", key="upload_qa"):
            if uploaded_file_qa is None:
                st.error("Please upload a file first.")
            else:
                try:
                    files = {"file": (uploaded_file_qa.name, uploaded_file_qa.getvalue())}
                    data = {
                        "device": str(device_qa),
                        "delimiter": delimiter
                    }
                    st.write("comne")
                    with st.spinner("Uploading Q&A file and waiting for response..."):
                        response = requests.post(API_URL_QA, files=files, data=data)
                    
                    if response.ok:
                        st.success("✅ Q&A file successfully uploaded!")
                        st.text_area("Server Response", response.text, height=200)
                    else:
                        st.error(f"❌ Error {response.status_code}")
                        st.text_area("Server Response", response.text, height=200)
                
                except Exception as e:
                    st.error(f"⚠️ An error occurred: {e}")

# ============= TAB 2: GET CONTEXT =============
# with tab2:
#     st.header("Get Context")
    
#     st.markdown("""
#     Send test queries to the Flask `/get_context` endpoint.
#     """)
    
#     question = st.text_area("📝 Enter your question:", height=100, placeholder="Type your question here...")
#     type_search = st.selectbox("🔎 Type of search:", ["smart", "similarity"])
    
#     if st.button("🚀 Send Request", key="get_context"):
#         if not question.strip():
#             st.error("Please enter a question before sending.")
#         else:
#             try:
#                 data = {
#                     "question": question,
#                     "type_search": type_search,
#                     "k": 3
#                 }
                
#                 with st.spinner("Contacting Flask API..."):
#                     response = requests.post(API_URL_context, data=data)
                
#                 if response.ok:
#                     st.success("✅ Request successful!")
#                     try:
#                         json_response = response.json()
#                         st.json(json_response)
#                     except Exception:
#                         st.text_area("Response Text:", response.text, height=300)
#                 else:
#                     st.error(f"❌ Error {response.status_code}")
#                     st.text_area("Server Response:", response.text, height=300)
            
#             except Exception as e:
#                 st.error(f"⚠️ Error connecting to API: {e}")








class Answerformat(BaseModel):
    is_a_good_answer:bool
    answer:str
    reason:str




def answer_from_docs(question_input,context_text):
    print("run answer from doc")
    system_prompt = """You are a helpful assistant. Answer the user's question based ONLY on the provided context. 
    If the answer cannot be found in the context, respond with: "No answer found in knowledge base." and is_a_good_answer is False
    Be concise and accurate."""

    user_message = f"""Context:
    {context_text}

    Question: {question_input}

    Please provide an answer based only on the context above."""

    # Call Bedrock via LiteLLM
    response = litellm.completion(
        model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],response_format=Answerformat
    )
    result_json=json.loads(response.choices[0].message.content)

    answer = result_json['answer']
    is_a_good_answer=result_json['is_a_good_answer']
    reason=result_json['reason']

    if is_a_good_answer:
        # Add assistant message to history with context
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Docs:"+answer,
            "context": context_text
        })
        
    else:
              
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "No answer found in knowledge base.",
            "context": "No context"
        })
    st.rerun()


def answer_from_QA(question_input,context_QA,context_text):
    print("run answer_from_QA")
    system_prompt = """You are a helpful assistant. Answer the user's question based ONLY on the provided context. 
    If the answer cannot be found in the context, respond with: "No answer found in knowledge base." and is_a_good_answer is False
    Be concise and accurate."""

    user_message = f"""Context:
    {context_QA}

    Question: {question_input}

    Please provide an answer based only on the context above."""

    # Call Bedrock via LiteLLM
    response = litellm.completion(
        model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],response_format=Answerformat
    )
    result_json=json.loads(response.choices[0].message.content)

    answer = result_json['answer']
    is_a_good_answer=result_json['is_a_good_answer']
    reason=result_json['reason']
    print("result QA",result_json)
    if  is_a_good_answer=="True":
        # Add assistant message to history with context
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "FQ&A"+answer,
            "context": context_QA
        })
        st.rerun()
    else:
        answer_from_docs(question_input,context_text)


with tab3:
    st.header("💬 Chat with AI")
    
    # --- INITIALIZE CHAT HISTORY AND STATE ---
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # --- TOP ROW: SETTINGS ---
    st.subheader("Chat Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        device_options = ["ALL"] + list(devices_data.keys()) if devices_data else ["ALL"]
        selected_device = st.radio(
            "📱 Select Device:",
            options=device_options,
            horizontal=True,
            label_visibility="collapsed"
        )
    
    with col2:
        # Load search types from JSON if available
        search_types = list(devices_data.get("search_types", ["smart", "similarity"])) if isinstance(devices_data, dict) else ["smart", "similarity"]
        # Fallback if search_types not in JSON
        if not search_types or search_types == ["search_types"]:
            search_types = ["smart", "similarity"]
        
    st.divider()
    
    # --- MESSAGES CONTAINER ---
    st.subheader("Conversation")
    messages_container = st.container(height=400, border=True)
    
    with messages_container:
        if not st.session_state.chat_history:
            st.info("💭 No messages yet. Ask your first question!")
        else:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    if message["role"] == "user":
                        st.markdown(message["content"])
                    else:
                        st.markdown(message["content"])
                        if "context" in message:
                            with st.expander("📚 Context used"):
                                st.markdown(message["context"])
    
    st.divider()
    
    # --- QUESTION INPUT AT BOTTOM ---
    if question_input := st.chat_input("Ask a question about your documents..."):
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": question_input})
        
        # Generate response
        try:
            # Step 1: Get context from Flask API
            settings = load_devices()
            selected_search_type=settings.get("search_type","similarity")
            use_categories_bo=settings.get("use_categories",None)

            context_data = {
                "question": question_input,
                "type_search": selected_search_type,
                "k": 5
            }
            
            if selected_device != "ALL":
                context_data["device"] = selected_device
            if use_categories_bo=="True":
                context_data["use_categories"] = use_categories_bo  
            with st.spinner("Retrieving context..."):
                context_response = requests.post(API_URL_context, data=context_data)
            
            if not context_response.ok:
                error_msg = f"Error retrieving context: {context_response.status_code}"
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
            else:
                try:
                    context_json = context_response.json()
                    # context_text = json.dumps(context_json, indent=2)
                    context_QA=context_json["Q&A"]
                    context_text=context_json["text"]

                except Exception:
                    context_text = context_response.text
                
                # Step 2: Use LiteLLM with Bedrock to generate answer
                # if not context_text.strip() or context_text == "{}":
                #     answer = "❌ No relevant context found in knowledge base for this question."
                #     st.session_state.chat_history.append({"role": "assistant", "content": answer})
                # else:
                if context_QA.strip():
                    with st.spinner("Generating answer..."):
                        try:
                            # Construct prompt
                            answer_from_QA(question_input=question_input,context_QA=context_QA,context_text=context_text)
                            
                        except Exception as e:
                            error_msg = f"⚠️ Error generating answer: {str(e)}"
                            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
                elif context_text.strip():
                    with st.spinner("Generating answer..."):
                        try:
                            # Construct prompt
                            answer_from_docs(question_input=question_input,context_text=context_text)
                            
                        except Exception as e:
                            error_msg = f"⚠️ Error generating answer: {str(e)}"
                            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})

        except Exception as e:
            error_msg = f"⚠️ Error: {e}"
            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        
        st.rerun()