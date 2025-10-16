from pydantic import BaseModel
import threading,os,time,json
from datetime import datetime


# NEO4J_URI ,NEO4J_USER ,NEO4J_PASSWORD ,DB= "neo4j://127.0.0.1:7687", "neo4j", "neo4jadmin","sav1"
# NEO4J_URI ,NEO4J_USER ,NEO4J_PASSWORD ,DB= "neo4j://172.31.14.92:7687", "neo4j", "adminneo4j","neo4j"
# MAIN_FOLDER="volume_sav_palaiseau"

MAIN_FOLDER = os.getenv("MAIN_FOLDER")
if not MAIN_FOLDER:
    timestamp = datetime.now().strftime("%d%m%H%M%S")
    MAIN_FOLDER = f"volume_{timestamp}"


SETTINGS_FILE=f"./{MAIN_FOLDER}/settings.json"
DOCUMENT_PATH=f"./{MAIN_FOLDER}/documents"
TEMP_MD_PATH=f"./{MAIN_FOLDER}/documents/temp.md"
IMAGES_PATH=f"./{MAIN_FOLDER}/documents/imgs"
EMB_MODEL_PATH=f"./{MAIN_FOLDER}/EMBmodel"
FEMB_MODEL_PATH=f"./{MAIN_FOLDER}/EMBmodel/all-MiniLM-L6-v2"
EMB_DEVICE="cpu"

DB_URL=f"./{MAIN_FOLDER}/dbs"
FEEDBACK_PATH=f"./{MAIN_FOLDER}/feedbackall.csv"

JSON_UIDS_PATH=f"./{MAIN_FOLDER}/uids_nodes.json"
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
        },
        "neo4j_auth":["neo4j://127.0.0.1:7687", "neo4j", "neo4jadmin","sav1"]        
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



neo4j_auth=load_settings(SETTINGS_FILE)["neo4j_auth"]
NEO4J_URI ,NEO4J_USER ,NEO4J_PASSWORD ,DB= neo4j_auth[0],neo4j_auth[1],neo4j_auth[2],neo4j_auth[3]


MODEL_NAME,PROVIDER=set_auth(SETTINGS_FILE)


