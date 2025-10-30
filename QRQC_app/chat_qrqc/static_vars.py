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
    # similaire_tickets_ids:str


class Issue(BaseModel):
    id:str
    issue:str
    why_is_similaire:str
class AnswerformatQA(BaseModel):
    similaire_issues:list[Issue]
    answer:str
    is_a_good_answer:bool

relevent_issues_number=10
system_prompt_= f"""

You are a Production Issue Retrieval Assistant.

Your job is to help engineers identify similar production issues by comparing a new problem description to a list of historical issues each one have ticket id , the problem
,and a disscussion and notes to solve the problem some time there is a correct solution and sometimes only disscussion with troubleshoting steps.

You will be given:

1. A new production ticket issue.

2. A list of previous issues (with IDs, descriptions).

Your goal is to:
- Analyze the new issue.
- Identify and return the IDs of the most relevant historical issues.
- Focus on **semantic similarity**, **root cause overlap**, **error patterns**, and **component relevance**.
- Return a ranked list up to {relevent_issues_number} relevant historical issue IDs,issues by order (the most relevent first). and a text answer explain the solution 
    or suggestion or steps to solve or troubleshoting , use only context.
- similaire ticket ids will be separated by ,
- If old issues are not relevant or similair , similaire_issues will be empty list, answer will be "No relevant past issues found."`
- if answer in the same language as the new issue was writed
- answer should be in a good markdown format.
- if context contain the correct solution for the new issue so is_a_good_answer will be true else false.
- Be concise, accurate, and avoid speculation.

Output :
should not forget any ouput key even if empty
"""



system_prompt="""
You are a **Production Issue engineer**.

## Objective
Your role is to help engineers identify similar production issues by comparing a new problem description to a collection of historical issues.

## Input
You will receive:
1. A **new production ticket issue**.
2. A **list of previous issues**, each containing:
   - Ticket ID
   - issue 
   - Discussion and notes (which may include troubleshooting steps or a confirmed solution)

## Task
Analyze the new issue and:
- Identify and return the **IDs of the most relevant historical issues**.
- Focus on *same category of issue* ,**same problem**.
- Rank the results by relevance (most relevant first), returning up to `{relevent_issues_number}` matches.
- make sure to take only relevent historical issues related to the new issue

## Output Requirements
Return a **JSON-formatted** response with the following fields:

```json
{
  "answer": "a concise markdown-formatted explanation summarizing solutions, troubleshooting steps, or suggestions derived only from the given context. If no relevant past issues exist, return 'No relevant past issues found.'",
  "similaire_issues": "list of relevant tickets, If no relevant past issues help to solve the new issue or not same category or not same problem, return empty list,
  "is_a_good_answer": true or false
}

"""