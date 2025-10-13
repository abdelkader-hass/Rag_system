from pydantic import BaseModel
import threading,os,time,json


NEO4J_URI ,NEO4J_USER ,NEO4J_PASSWORD ,DB= "neo4j://127.0.0.1:7687", "neo4j", "neo4jadmin","sav1"
SETTINGS_FILE="./settings.json"

DOCUMENT_PATH="./vol/documents"
TEMP_MD_PATH="./vol/documents/temp.md"
IMAGES_PATH="./vol/documents/imgs"
EMB_MODEL_PATH="./vol/EMBmodel"
FEMB_MODEL_PATH="./vol/EMBmodel/all-MiniLM-L6-v2"
EMB_DEVICE="cpu"

DB_URL="./vol/dbs"
FEEDBACK_PATH="./vol/feedbackall.csv"

JSON_UIDS_PATH="./vol/uids_nodes.json"
if not os.path.exists(DB_URL):
# Create the directory
    os.makedirs(DB_URL,exist_ok=True)

if not os.path.exists(EMB_MODEL_PATH):
# Create the directory
    os.makedirs(EMB_MODEL_PATH,exist_ok=True)

if not os.path.exists(IMAGES_PATH):
# Create the directory
    os.makedirs(IMAGES_PATH,exist_ok=True) 






# ------------------------------------
def load_settings(setting_path):
    if os.path.exists(setting_path):
        with open(setting_path, "r") as f:
            return json.load(f)
    return {
        "llm_type": "Gemini",
        "gemini": {
            "key": "",
            "model_name": ""
        },
        "bedrock": {
            "key": "",
            "id": "",
            "region": "",
            "model_name": ""
        }
    }

def set_auth(setings_path=""):
    # litellm.set_verbose=True
    settings=load_settings(setings_path)
    global MODEL_NAME
    #------------------------------
    if settings["llm_type"] == "Gemini":
        os.environ["GEMINI_API_KEY"] = settings["gemini"].get("key", "")
        MODEL_NAME = settings["gemini"].get("model_name", "")
    #------------------------------
    elif settings["llm_type"] == "Openai":
        os.environ["OPENAI_API_KEY"] = settings["openai"].get("key", "")
        MODEL_NAME = settings["openai"].get("model_name", "")
    #------------------------------
    elif settings["llm_type"] == "Claude":
        os.environ["ANTHROPIC_API_KEY"] = settings["claude"].get("key", "")
        MODEL_NAME = settings["claude"].get("model_name", "")
    #------------------------------
    elif settings["llm_type"] == "Bedrock":
        os.environ["AWS_ACCESS_KEY_ID"] = settings["bedrock"].get("id", "")
        os.environ["AWS_SECRET_ACCESS_KEY"] = settings["bedrock"].get("key", "")
        os.environ["AWS_REGION_NAME"] = settings["bedrock"].get("region", "")
        MODEL_NAME = settings["bedrock"].get("model_name", "")
        
    return MODEL_NAME,settings["llm_type"]






MODEL_NAME,PROVIDER=set_auth(SETTINGS_FILE)


