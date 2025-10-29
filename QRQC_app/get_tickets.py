import requests
import os
import pandas as pd
import time 



#Header Parameters  X-Redmine-API-Key
APIKEY="68d67a301ef022e8df4a31e96ac44806b4f7ee5a"



#-------------------------------
def request(url,headers={},params={}):

    max_retries = 10
    backoff_factor = 3  # each retry waits 2x longer than the previous one
    retry_count = 0

    while retry_count < max_retries:
        try:
            response = requests.get(url, headers=headers,params=params, timeout=20)

            # ✅ If request succeeded
            if response.status_code == 200:
                data = response.json()
                # print("✅ Success:", data)
                return response

            # 🚦 Handle rate limiting
            elif response.status_code == 429:
                wait_time = (2 ** retry_count) * backoff_factor
                print(f"⚠️ Too many requests (429). Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                retry_count += 1
                continue

            # 🔁 Handle server-side temporary errors
            elif response.status_code in [500, 502, 503, 504]:
                wait_time = (2 ** retry_count) * backoff_factor
                print(f"⚠️ Server error {response.status_code}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                retry_count += 1
                continue

            # ❌ Other errors (don’t retry)
            else:
                print(f"❌ Failed with status {response.status_code}: {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            wait_time = (2 ** retry_count) * backoff_factor
            print(f"⚠️ Request failed ({e}). Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            retry_count += 1

    else:
        print("❌ Max retries reached. Giving up.")

#-------------------------------
def get_count_tickets(project_id,offset=0,limit=1,Apikey=""):
    URL=f"http://hfrredmine.jy.fr/issues.json?project_id={project_id}&include=journals&offset={offset}&limit={limit}&status_id=closed"
    # Set up headers
    headers = {
        "X-Redmine-API-Key": Apikey,        # custom header name
        "Accept": "application/json"
    }

    response=request(URL,headers)
    if response:
        # print("Success!")
        # print(response.json())  # or response.text
        json_response=response.json()
        # print(json_response)
        total_count=json_response.get("total_count",None)
        return total_count
    else:
        print(f"Error {response}: {response}")
        return None

#-------------------------------
def get_chunks(total_count):
    if not total_count:
        return []
    chunk_size = 100
    result = []
    for offset in range(0, total_count, chunk_size):
        result.append({
                "offset": offset,
                "limit": chunk_size})
    
    # return equivalent
    return result

#-------------------------------
def get_tickets(project_id,offset=0,limit=1,Apikey=""):
    #use header parameters
    URL=f"http://hfrredmine.jy.fr/issues.json?project_id={project_id}&include=journals&offset={offset}&limit={limit}&status_id=closed"
    headers = {
        "X-Redmine-API-Key": Apikey,        # custom header name
        "Accept": "application/json"
    }

    # Make the GET request
    # response = requests.get(URL, headers=headers)
    response=request(URL,headers)

    # Check the response
    if response:
        tickets=response.json()
        return tickets
    else:
        print(f"Error {response}: {response}")
        return None

#-------------------------------
def get_notes(ticket_id,Apikey=""):
    #use header parameters
    URL=f"http://hfrredmine.jy.fr/issues/{ticket_id}.json"

    headers = {
        "X-Redmine-API-Key": Apikey,        # custom header name
        "Accept": "application/json"
    }
    # Add parameters to include journals (notes)
    params = {"include": "journals,attachments"}

    # Make the GET request
    # response = requests.get(URL, headers=headers, params=params)
    response=request(URL,headers,params)

    
    # Check the response
    if response:
        # Convert XML to Python dict
        data_json =response.json()
        # json_response.get("total_count",None)
        return data_json
    else:
        print(f"Error {response}: {response}")
        return None

#-------------------------------
def load_data_ids(file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)

        # Get all IDs from the 'ticket_id' column
        # (use .dropna() to ignore any empty rows)
        ticket_ids = df["ticket_id"].dropna().tolist()

        print("🎟️ All ticket IDs:", len(ticket_ids))

        # If you only want unique IDs:
        unique_ticket_ids = df["ticket_id"].dropna().unique().tolist()
    else:
        unique_ticket_ids=[]
    return unique_ticket_ids

#-------------------------------
def save_data(file_path,new_data):
    new_df = pd.DataFrame(new_data)

    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)

        # Find any new columns that exist in new_df but not in existing_df
        new_columns = [col for col in new_df.columns if col not in existing_df.columns]
        if new_columns:
            print(f"🆕 Adding new columns: {new_columns}")
            for col in new_columns:
                # Add missing columns to existing data and fill with 0
                existing_df[col] = 0

        # Also ensure new_df has all old columns (in case they are missing)
        for col in existing_df.columns:
            if col not in new_df.columns:
                new_df[col] = 0

        # Merge them
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df
    combined_df = combined_df.drop_duplicates(keep="last")

    # Save to CSV
    combined_df.to_csv(file_path, index=False)

#-------------------------------
def run_process(project_id,file_path):
    Uids_list=load_data_ids(file_path)
    # print(Uids_list)
    print(f"projet {project_id}, save at {file_path}")
    count=get_count_tickets(project_id=project_id,Apikey=APIKEY)
    if count:
        print(f"we have {count} tickets")
    chunks=get_chunks(count)
    rows=[]
    for idx,chunk in enumerate(chunks):
        offset=chunk.get("offset")
        limit=chunk.get("limit")
        tickets=get_tickets(project_id=project_id,offset=offset,limit=limit,Apikey=APIKEY)
        tickets=tickets.get("issues","")
        if tickets:
            # print(f"retreive {len(tickets)} started from {offset}")
            for ticket in tickets:
                row={}
                ticket_id=ticket.get('id')
                if int(ticket_id) in Uids_list:
                    # print("exist already")
                    continue
                custom_fields=ticket.get('custom_fields',[])
                row['ticket_id']=ticket_id
                row["author"]=ticket.get("author","").get("name","")
                for field in custom_fields:
                    row[field['name']]=field['value']
                # ticket_id="51415"
                notes=get_notes(ticket_id,Apikey=APIKEY)
                note_txt=""
                if notes:
                    issue=notes.get("issue")
                    journals=issue.get('journals')
                    for journal in journals:
                        note=journal.get("notes")
                        if note :
                            note_txt+="\n"+str(note)
                row["notes"]=note_txt
                rows.append(row)
    
            # print(tickets)
        print(f"finish chunk {idx}")
        time.sleep(5)

    print("Sucess",len(rows))
    save_data(file_path,rows)



#-------------------------------
if __name__=="__main__":
    PROJECT_id_raman ="redmine2027" #raman
    file_path="raman_qrqc_data.csv"


    PROJECT_id_emission="redmine2031" #emission
    file_path="emission_qrqc_data.csv"


    run_process(PROJECT_id_emission,file_path)