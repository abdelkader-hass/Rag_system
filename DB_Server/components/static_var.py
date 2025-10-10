from pydantic import BaseModel
import threading,os,time,json


NEO4J_URI ,NEO4J_USER ,NEO4J_PASSWORD ,DB= "neo4j://127.0.0.1:7687", "neo4j", "neo4jadmin","sav1"
SETTINGS_FILE="./settings.json"

DOCUMENT_PATH="./vol/documents"
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








# 1. Create the root node
# ------------------------------------
class Part(BaseModel):
    # parent_id:str
    title:str
    description:str
    start_sentence:str
    end_sentence:str
class Aformat(BaseModel):
    parts:list[Part]
    text_description:str
    # parent_id:str


SYSTEM_PROMPT=f"""

You are an expert document analyzer with advanced skills in intelligent content segmentation and hierarchical organization.

TASK:
Analyze the provided text and determine whether it should be divided into meaningful sections. Base your judgment on content complexity, thematic shifts, and logical structure.

 
SEGMENTATION RULES:

When TO Segment:
✓ The text contains two or more distinct topics or themes with identifiable boundaries  
✓ The content is complex enough that structured segmentation would improve clarity or navigation  
✓ Each identified section must contain **at least 5 complete sentences** of meaningful content  
✓ MAXIMUM 4 Sections

When NOT to Segment:
✗ Any potential section has fewer than 5 sentences  
✗ Segmenting would disrupt the flow of ideas or logical progression  

EDGE CASES:
- If no segmentation is needed, return an empty list.

OUTPUT FORMAT:
Return a valid JSON object **as a Python string**. Each section must include:

- `"title"`: A concise title summarizing the section’s content
- `"description"`: A 2-3 sentence summary of the section
- `"start_sentence"`: The exact first sentence of the section
- `"end_sentence"`: The exact last sentence of the section

and also a short description 2-3 of the give_text should be always in the output even if there is no subsections
Output Format: The output must be a valid JSON
"""


#------------------Search
SYSTEM_SEARCH_PROMPT="""
You are a precise node selector. Your task is to identify which nodes contain information relevant to answering a given question.
You will receive a list of nodes with ID and Description fields, followed by a question.
Select nodes ONLY if their description contains information that directly helps answer the question. Do not select nodes with tangentially related or uncertain relevance.
Return only the relevant node IDs as a comma-separated list. If no nodes are relevant retrun empty list

"""


SYSTEM__SEARCH_PROMPT_answer = """Your are a good agent , Answer the question using only the provided context. 
If the answer is not in the context, 
respond with "I don't have enough information to answer this question.
answer text in markdown format to be clear to read.
"""

# ------------------------------------
class nodes(BaseModel):
    id:str
    selection_raison:str
class AformatSEARCH(BaseModel):
    nodes:list[nodes]
class AnswerFormat(BaseModel):
    answer_md_format:str
    bool_answer_find_or_not:str



class RateLimiter:
    def __init__(self, max_calls, period):
        self._lock = threading.Lock()
        self.max_calls = max_calls
        self.period = period
        self.calls = 0
        self.start_time = time.time()
        
    def acquire(self):
        with self._lock:
            current_time = time.time()
            elapsed = current_time - self.start_time
            if elapsed > self.period:
                # Reset the count and timer
                self.calls = 0
                self.start_time = current_time
            
            if self.calls < self.max_calls:
                self.calls += 1
                return
            else:
                # Need to wait for remaining time of the period
                wait_time = self.period - elapsed
                print(f"Rate limit reached. Sleeping for {wait_time:.2f} seconds...")
                time.sleep(wait_time)
                # Reset after sleep
                self.calls = 1
                self.start_time = time.time()

MAX_WORKERS=15
RATE_LIMITER = RateLimiter(max_calls=15, period=60)  # 10 requests per 60 seconds
