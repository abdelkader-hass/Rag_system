import streamlit as st
import os,json,requests,boto3,time
from static_vars import SETTINGS_PATH,FEEDBACK_PATH,MESSAGE_ANSWER,Answerformat,system_prompt,LOCAL_IMG_DIR
import boto3
import requests
from litellm import completion
import litellm
import pymupdf4llm
import re
from PIL import Image
from io import BytesIO
import shutil


os.makedirs("images",exist_ok=True)
os.makedirs("tmp_images",exist_ok=True)


# st.set_page_config(layout='wide',page_title='AI4SAV')
def read_settings(path=SETTINGS_PATH):
    try:
        with open(path, 'r') as setting:
            data = json.load(setting)

        # var_env=data["var_env"][0]
        # for name,value in var_env:
        #     os.environ[name]=value
    except:
        data={
                "Llm_framework": "Litellm",
                "db_server": "",
                "images-server":"",
                "keys": {
                    "AWS_ACCESS_KEY_ID": "",
                    "AWS_SECRET_ACCESS_KEY": "",
                    "AWS_REGION_NAME": "us-east-1",
                    "AWS_Model_NAME": "",
                    "knowledge_base_id": [
                    ],
                    "data_source_id": [
                    ],
                    "s3_name": "",
                    "s3-images":""
                },
                "kn_query": [
                    10,
                    2,
                    "similarity"
                ],
                "devices":{"EL200":"","C500":""},
                "use_categories":"True",
                "categories":"",
                "Split_Type":"smart",
                "use_markdown":"True",
                "chunk_length":1000,
                "part_size":300,
                "search_type":"similarity"
                }
        try:
            json_data = json.dumps(data,indent=2)
                # write the JSON string to a file
            with open(path, 'w') as f:
                f.write(json_data)
        except Exception as e:
            print("failed to save settings",str(e))

    return data



data=read_settings()
devices_data = data['devices']
categories_list = data['categories']
use_categories=data['use_categories']
Split_Type=data['Split_Type']
use_markdow=data["use_markdown"]
chunk_length=data.get("chunk_length",1000)
part_size=data.get("part_size",300)
search_type=data.get("search_type","similarity")
k=data.get("kn_query",[10])[0]

SERVER_URL=data['db_server']
ACCESS_KEY=data['keys']['AWS_ACCESS_KEY_ID']
SECRET_KEY=data['keys']['AWS_SECRET_ACCESS_KEY']
REGION=data['keys']['AWS_REGION_NAME']

os.environ["AWS_ACCESS_KEY_ID"] = ACCESS_KEY
os.environ["AWS_SECRET_ACCESS_KEY"] = SECRET_KEY
os.environ["AWS_REGION_NAME"] = REGION

s3_BUCKET = data['keys']['s3_name'] 
MODEL_NAME=data['keys']['AWS_REGION_NAME']


# Professional styling
st.set_page_config(
    layout='wide',
    page_title='QRQC AI Assistant',
    page_icon='🤖',
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Hide Streamlit branding */
    # #MainMenu {visibility: hidden;}
    # footer {visibility: hidden;}
    # header {visibility: hidden;}
    
    /* Main container styling */
    .main > div {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* User message styling */
    .stChatMessage[data-testid="user"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
    }
    
    /* Assistant message styling */
    .stChatMessage[data-testid="assistant"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
    }
    gradient_cls {
    border: none;                 /* Remove default border */
    height: 4px;                   /* Thickness of the line */
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    border-radius: 2px;            /* Rounded edges (optional) */
    }
            

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Subtitle styling */
    .subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* File uploader styling */
    .stFileUploader {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
    }
    
    /* Progress bar styling */
    .stProgress .st-bo {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        border-radius: 10px;
        padding: 1rem;
        border: none;
        color: white;
    }
    
    .stError {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        border-radius: 10px;
        padding: 1rem;
        border: none;
        color: white;
    }
    
    /* Sidebar title styling */
    .sidebar-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-size: 1.5rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem;
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    /* Chat input styling */
    .stChatInputContainer {
        border: 2px solid #667eea;
        border-radius: 25px;
        background: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    /* Info box styling */
    .info-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    
    /* Loading spinner styling */
    .stSpinner {
        text-align: center;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

if "messsage" not in st.session_state:
    st.session_state.messsage=[("assistant","Hello 👋, How can i help you ? ")]

def get_context_server(question_input,selected_device,use_categories):
    try:
        

        context_data = {
            "question": question_input,
            "type_search": search_type,
            "k": k
        }
        
        if selected_device != "ALL":
            context_data["device"] = selected_device
        if use_categories=="True":
            context_data["use_categories"] = use_categories  
        with st.spinner("Retrieving context..."):
            context_response = requests.post(SERVER_URL+"/get_context", data=context_data)
        
        if not context_response.ok:
            error_msg = f"Error retrieving context: {context_response.status_code}"
            return "No context","No context"
            # st.session_state.messsage.append({"role": "assistant", "content": error_msg})
        else:
            try:
                context_json = context_response.json()
                # context_text = json.dumps(context_json, indent=2)
                context_QA=context_json["Q&A"]
                context_text=context_json["text"]
                return context_QA,context_text
            except Exception as e:
                print("Error get context",str(e))
                return "No context","No context"
    except:
        return "No context","No context"


def run_llm(user_message="no input"):
    response = litellm.completion(
        model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0",
        messages=[
            {"role": "user", "content": system_prompt},
            {"role": "assistant", "content": "now give me your question and the context"},
            {"role": "user", "content": user_message}
        ],response_format=Answerformat
    )
    result_json=json.loads(response.choices[0].message.content)
    return result_json

def answer_from_docs(question_input,context_text,is_used_categories):
    print("run answer from doc")

    user_message = f"""Context:
    {context_text}

    Question: {question_input}

    Please provide an answer based only on the context above."""

    # Call Bedrock via LiteLLM
    result_json=run_llm(user_message)
    answer = result_json['answer']
    is_a_good_answer=result_json['is_a_good_answer']
    reason=result_json['reason']
    print("result QA",result_json)

    if is_a_good_answer:
        try:
            return answer
        except Exception as e:
            print("error chat_stream",str(e))
            return "No answer found in knowledge base"
        
    else:
        # if categories is used and no answer so try to search in whole documents
        print("categories is used and no answer")
        if is_used_categories=="True":
            context_QA,context_text=get_context_server(user_message,selected_device,use_categories="False")
            user_message = f"""Context:
            {context_text}

            Question: {question_input}

            Please provide an answer based only on the context above."""

            # Call Bedrock via LiteLLM
            result_json=run_llm(user_message)
            answer = result_json['answer']
            is_a_good_answer=result_json['is_a_good_answer']
            reason=result_json['reason']
            print("result QA",result_json)

            if is_a_good_answer:
                try:
                    return answer
                except Exception as e:
                    print("error chat_stream",str(e))
                    return "No answer found in knowledge base"

            else:
                return "No answer found in knowledge base"

        else:
            return "No answer found in knowledge base"

    # st.rerun()


def answer_from_QA(question_input,context_QA,context_text,is_used_categories):
    print("run answer_from_QA")


    user_message = f"""
    Please provide an answer based only on the context above. and make sure to keep images
    
    **Question: {question_input}
    
    ------- 
    **Context:
    {context_QA}

    """

    # Call Bedrock via LiteLLM
    result_json=run_llm(user_message)

    answer = result_json['answer']
    is_a_good_answer=result_json['is_a_good_answer']
    reason=result_json['reason']
    print("result QA",result_json)
    if  is_a_good_answer=="True":

        try:
            return answer
        except Exception as e:
            print("error chat_stream",str(e))
            return "No answer found in knowledge base"

        # st.rerun()
    else:
        data=answer_from_docs(question_input,context_text,is_used_categories=is_used_categories)
        return data




# sys.stdout=open(LOG_PATH,"a")
# sys.stderr=open(LOGERROR_PATH,"a")

#images part S3
def convert_image_to_binary(image_path):
    with Image.open(image_path) as img:

        img_byte_array = BytesIO()

        img.save(img_byte_array, format=img.format)

        img_byte_array.seek(0)
    return img_byte_array

def save_images_s3():
    aws_settings=st.session_state.settings
    ACCESS_KEY=aws_settings['keys']['AWS_ACCESS_KEY_ID']
    SECRET_KEY=aws_settings['keys']['AWS_SECRET_ACCESS_KEY']
    REGION=aws_settings['keys']['AWS_REGION_NAME']
    aws_bucket_name=aws_settings['keys']['s3-images']
    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION
    )
    folder_path = "./images"
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                image_path=f"./images/{filename}"                
                image_data = convert_image_to_binary(image_path)
                try:
                    try:
                        s3_client.head_object(Bucket=aws_bucket_name, Key=filename)
                        print(f"Image exist already in {aws_bucket_name}/{filename}")

                    except :
                        s3_client.upload_fileobj(image_data,aws_bucket_name,filename)
                        print(f"Image successfully uploaded to S3 at {aws_bucket_name}/{filename}")
                except Exception as e:
                    print(f"Error uploading image: {e}")

        # Delete the folder after iteration
        shutil.rmtree(folder_path)
        print(f"Deleted folder: {folder_path}")
    else:
        print(f"Folder '{folder_path}' does not exist.")

def download_image_s3(image_name):
    aws_settings=st.session_state.settings
    ACCESS_KEY=aws_settings['keys']['AWS_ACCESS_KEY_ID']
    SECRET_KEY=aws_settings['keys']['AWS_SECRET_ACCESS_KEY']
    REGION=aws_settings['keys']['AWS_REGION_NAME']
    aws_bucket_name=aws_settings['keys']['s3-images']
    # Initialize S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION
    )

    # S3 bucket and file details
    bucket_name = aws_bucket_name
    object_key = image_name  # S3 key (path inside bucket)
    download_path = f"./tmp_images/{image_name}"            # Local filename to save

    try:
        s3_client.download_file(bucket_name, object_key, download_path)
        print(f"Downloaded: {object_key} → {download_path}")
    except Exception as e:
        print(f"Error downloading {object_key} from S3: {e}")

# download image from server 
def download_image(image_name):
    local_path = os.path.join(LOCAL_IMG_DIR, image_name)

    # 1️⃣ Check if image already exists locally
    if os.path.exists(local_path):
        print(f"✅ Image found locally at {local_path}")
        return local_path

    # 2️⃣ Otherwise, request it from the Flask API
    print(f"🕐 Image not found locally. Requesting from server...")
    response = requests.post(SERVER_URL+"/download_image", json={"image_name": image_name})

    if response.status_code == 200:
        # Save the received image
        os.makedirs(LOCAL_IMG_DIR, exist_ok=True)
        with open(local_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Image downloaded and saved to {local_path}")
        return local_path
    else:
        print(f"❌ Failed to download image: {response.text}")
        return None




def parse_content(s):
    # Pattern to match [imageurl:name.ext] and extract just name.ext
    pattern = r'\[imageurl:([^\[\]]+\.(?:jpg|jpeg|png|gif|bmp|webp))\]'
    parts = []
    last_index = 0

    for match in re.finditer(pattern, s, re.IGNORECASE):
        start, end = match.span()
        image_name = match.group(1)

        # Text before image
        if start > last_index:
            text_part = s[last_index:start].strip()
            if text_part:
                parts.append(("text", text_part))

        # Image part without "imageurl:"
        parts.append(("image", image_name.strip()))
        last_index = end

    # Remaining text after last image
    if last_index < len(s):
        remaining = s[last_index:].strip()
        if remaining:
            parts.append(("text", remaining))

    return parts



file_exists_feedback = os.path.isfile(FEEDBACK_PATH)


try:
    if st.query_params["id_page"] == "1":
        try:
            st.title("Admin")
        except Exception as e:
            print("Feedback Exception",str(e))

except:
    st.markdown('<h1 class="main-title">🤖 QRQC AI Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your intelligent assistant powered by advanced AI</p><hr class="gradient_cls">', unsafe_allow_html=True)
    selected_device=st.selectbox("Select device ",["ALL"]+list(devices_data.keys()),index=0)
    chat_tab=st.container()
    chat_container=chat_tab.container()

    for msg in st.session_state.messsage:
        list_parts=parse_content(str(msg[1]))
        bool_download_image=False
        with chat_container.chat_message(str(msg[0])):
            cpt=0
            for i in list_parts:
                
                if i[0]=="image":
                    cpt+=1    
                    print("image finded",cpt,i[1])
                    try:
                        image_path = os.path.join(LOCAL_IMG_DIR, i[1])
                        print("image path",image_path)
                        st.image(image_path)
                        # st.image(r"D:\projects\langchain_chat\Rag_system\DB_Server\vol\documents\imgs/"+i[1])
                        
                    except:
                        try:
                            path=download_image(i[1])
                            if path:
                                bool_download_image=True
                        except:
                            st.write(i[1])
                else:
                    st.write(i[1])
    if bool_download_image:
        st.rerun()
    user_message = st.chat_input(placeholder="💬 Type your message here...")

    # st.write("how to run reinitialization of RS485 Probes")

    if user_message:
        question_input=user_message
        st.session_state.messsage.append(("human",question_input))
        chat_container.chat_message("human").write(question_input)

        #Retrieve data
        context_QA,context_text=get_context_server(user_message,selected_device,use_categories)
        already_answer=False
        if context_QA.strip():
            already_answer=True
            with st.spinner("Generating answer..."):
                print("use questions first")

                try:
                    answer=answer_from_QA(question_input=question_input,context_QA=context_QA,context_text=context_text,is_used_categories=use_categories)
                    final_answer=chat_container.chat_message("assistant").markdown(answer)
                    st.session_state.messsage.append(("assistant",str(answer)))
                except Exception as e:
                    error_msg = f"⚠️ Error generating answer: {str(e)}"
                    print(error_msg)
                    st.session_state.messsage.append(("assistant","No answer found in knowledge base."))
            st.rerun()
        elif context_text.strip():
                
                print("use docs directly")
                already_answer=True
                with st.spinner("Generating answer..."):
                    try:
                        answer=answer_from_docs(question_input=question_input,context_text=context_text,is_used_categories=use_categories)
                        final_answer=chat_container.chat_message("assistant").markdown(answer)
                        st.session_state.messsage.append(("assistant",str(answer)))
                    except Exception as e:
                        error_msg = f"⚠️ Error generating answer: {str(e)}"
                        print(error_msg)
                        st.session_state.messsage.append(("assistant","No answer found in knowledge base."))

        if not context_text.strip() and use_categories=="True" and not already_answer:
            # search in whole document
            print("search in whole document this category is empty")
            context_QA,context_text=get_context_server(user_message,selected_device,"False")

            if context_text.strip():
                with st.spinner("Generating answer..."):
                    try:
                        answer=answer_from_docs(question_input=question_input,context_text=context_text,is_used_categories=use_categories)
                        final_answer=chat_container.chat_message("assistant").markdown(answer)
                        st.session_state.messsage.append(("assistant",str(answer)))
                    except Exception as e:
                        error_msg = f"⚠️ Error generating answer: {str(e)}"
                        print(error_msg)
                        st.session_state.messsage.append(("assistant","No answer found in knowledge base."))


            st.rerun()
        
        else:
            print("entred to last else")
            if st.session_state.messsage[-1][0] != "assistant":
                st.session_state.messsage.append(("assistant","No answer found in knowledge base."))
            st.rerun()


    def set_files_tab():
        Add_files_tab=st.sidebar.container()
        with Add_files_tab:
            st.markdown('<div class="sidebar-title">📁 File Management</div>', unsafe_allow_html=True)

            settings=read_settings()
            st.session_state.settings=settings

            mdp=st.text_input("Password",type="password")
            is_qa_file = st.toggle("Q&A Files", value=False, help="Enable this if you're uploading Q&A CSV files")
            # is_qa_file=False
            if not is_qa_file:
            # Add_files_tab.title("Upload files to knowledge base")
            # File uploader
                uploaded_files = st.file_uploader(
                    "📤 Upload Documents",
                    type=["pdf", "txt"],
                    accept_multiple_files=True,
                    help="Supported formats: PDF, Text files"
                )

            else:
                uploaded_files = st.file_uploader(
                    "📤 Upload Documents",
                    type=["csv"],
                    accept_multiple_files=True,
                    help="Supported formats:  CSV files"
                )

            if uploaded_files:
                if not is_qa_file:
                    # chunk_length = st.number_input("Chunk Length (words)", min_value=100, max_value=5000, value=1000, step=50)
                    # part_size=st.number_input("Chunk Length (words)", min_value=100, max_value=500, value=300, step=50)
                    st.subheader("Optional Parameters")
                    device = st.selectbox(
                        "Device model",
                        options=list(devices_data.keys()),
                        index=0
                    )
                else:

                    delimiter = st.text_input(
                        "Delimiter",
                        value=",",
                        max_chars=1,
                        placeholder='delimiter can be , ; -'
                    )
                    
                    device_qa = st.selectbox(
                        "Device model",
                        options=list(devices_data.keys()),
                        index=0,
                        key="device_qa"
                    )
                    

                if st.button("🚀 Upload Files or Q&A and Process", key="upload_qa") and mdp=="adminpass":
                    count_new_files=0
                    try:
                        progress_bar = st.progress(0)
                        total_files = len(uploaded_files)
                        for i, file in enumerate(uploaded_files):
                            if not is_qa_file:
                                try:
                                    files = {"file": (file.name, file.getvalue())}
                                    data = {
                                        "split_type": Split_Type,
                                        "use_md": use_markdow,
                                        "chunk_length": int(chunk_length),
                                        "part_size":int(part_size),
                                        "device": str(device),
                                    }
                                    if use_categories=="True" and len(categories_list)>2:
                                        
                                        data['categories'] = categories_list
                                        print(categories_list)
                                    with st.spinner("Uploading file and waiting for response..."):
                                        response = requests.post(SERVER_URL+"/add_file", files=files, data=data)
                                    if response.ok:
                                        st.success("✅ File successfully uploaded!")
                                        st.text_area("Server Response", response.text, height=200)
                                        st.success("Your files are now ready in the Knowledge Base! 🚀")
                                    else:
                                        # st.error(f"❌ Error {response.status_code}")
                                        st.error(f"❌ Error {response.status_code} ,{response.text},{file.name}")

                                except Exception as e:
                                    st.error(f"❌ Error {e} {file.name}")


                            else:
                                try:
                                    files = {"file": (file.name, file.getvalue())}
                                    data = {
                                        "device": str(device_qa),
                                        "delimiter": delimiter
                                    }
                                    st.write("comne")
                                    with st.spinner("Uploading Q&A file and waiting for response..."):
                                        response = requests.post(SERVER_URL+"/add_file_QA", files=files, data=data)
                                    
                                    if response.ok:
                                        st.success("✅ Q&A file successfully uploaded!")
                                        st.text_area("Server Response", response.text, height=200)
                                        st.success("Your files are now ready in the Knowledge Base! 🚀")
                                    else:
                                        st.error(f"❌ Error {response.status_code} {file.name}")
                                        st.text_area("Server Response", response.text, height=200)
                                
                                except Exception as e:
                                    st.error(f"❌ Error {e} {file.name}")



                            progress_bar.progress((i + 1) / total_files)

                    
                        

                    except:
                        st.error("Error durring uploading files to DB")
            
            else:
                st.error("Please upload a file to continue.")



    set_files_tab()

