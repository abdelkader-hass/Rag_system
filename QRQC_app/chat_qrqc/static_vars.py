from pydantic import BaseModel
import litellm
import json



SETTINGS_PATH="./settings.json"
LOCAL_IMG_DIR="./tmp_images"


FEEDBACK_PATH=""


SYSTEM_PROMPT_ANSWER = """
Your are a good agent , Answer the Question using only the provided context. 

Rules:
- keep images url in answer if exist in same format [imageurl:]
whene you should not answer:
    If the answer is not in the context or context is not enough, 
    respond with "I don't have enough information to answer this question.

answer should be in clear Markdown format each step in line 
"""


MESSAGE_ANSWER=[{"role": "user","content":SYSTEM_PROMPT_ANSWER},
                    {"role":"assistant","content":"now please give me the Context"}]




#------------------------------------------- LLM Answer part
class Answerformat(BaseModel):
    is_a_good_answer:bool
    answer:str
    reason:str



system_prompt= """
Your are a good agent , Answer the Question using only the provided context. 

Rules:
- context can contain images in this format ![imageurl:image_name] so make sure to keep images url in answer if exist in same format [imageurl:image_name] and in the right possition.
- Be concise and accurate.
whene you should not answer:
    If the answer cannot be found in the context, 
    respond respond with: "No answer found in knowledge base." and is_a_good_answer is False.

answer should be in clear Markdown format and add lines to more readable

Rules:
- put images url in answer if exist in same format ![imageurl:] and in the right position in text.
- If the answer cannot be found in the context, respond with: "No answer found in knowledge base." and is_a_good_answer is False.
- Be concise and accurate.
- answer should be in clear Markdown format and add lines to more readable
"""

