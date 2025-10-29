import requests
import xmltodict
import json

PROJECT_id_raman ="redmine2027" #raman
PROJECT_id_emission="redmine2031" #emission

# URL_REDMINE_count=f"http://hfrredmine.jy.fr/issues.json?project_id={project_id}&include=journals&offset=0&limit=1&status_id=closed"
# URL_="http://hfrredmine.jy.fr/issues.json?project_id={project_id}&include=journals&offset={{$json.offset}}&limit=100&status_id=closed"

#Header Parameters  X-Redmine-API-Key
APIKEY="68d67a301ef022e8df4a31e96ac44806b4f7ee5a"


def xml_to_json(xml):
    pass

#-------------------------------

def get_count_tickets(project_id,offset=0,limit=1,Apikey=""):
    URL=f"http://hfrredmine.jy.fr/issues.json?project_id={project_id}&include=journals&offset={offset}&limit={limit}&status_id=closed"
    # Set up headers
    headers = {
        "X-Redmine-API-Key": Apikey,        # custom header name
        "Accept": "application/json"
    }
    # Make the GET request
    response = requests.get(URL, headers=headers)
    # Check the response
    if response.status_code == 200:
        # print("Success!")
        # print(response.json())  # or response.text
        json_response=response.json()
        # print(json_response)
        total_count=json_response.get("total_count",None)
        return total_count
    else:
        print(f"Error {response.status_code}: {response.text}")
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
    response = requests.get(URL, headers=headers)

    # Check the response
    if response.status_code == 200:
        print("Success!")
        # print(response.json())  # or response.text
        tickets=response.json()
        return tickets
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
#-------------------------------

def get_notes(ticket_id,key="86c551df5b12cfa86a93d2646d0dc89481df5edc",Apikey=""):
    #use header parameters
    URL=f"http://hfrredmine.jy.fr/issues/{ticket_id}.json"

    headers = {
        "X-Redmine-API-Key": Apikey,        # custom header name
        "Accept": "application/json"
    }
    # Add parameters to include journals (notes)
    params = {"include": "journals,attachments"}

    # Make the GET request
    response = requests.get(URL, headers=headers, params=params)

    
    # Check the response
    if response.status_code == 200:
        # Convert XML to Python dict
        data_json =response.json()
        # json_response.get("total_count",None)
        return data_json
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

#-------------------------------
if __name__=="__main__":
    project_id=PROJECT_id_raman
    count=get_count_tickets(project_id=project_id,Apikey=APIKEY)
    if count:
        print(f"we have {count} tickets")
    chunks=get_chunks(count)
    if chunks:
        print(f"we have {len(chunks)} chunk")
    for chunk in chunks:
        offset=chunk.get("offset")
        limit=chunk.get("limit")
        tickets=get_tickets(project_id=project_id,offset=offset,limit=limit,Apikey=APIKEY)
        tickets=tickets.get("issues","")
        if tickets:
            print(f"retreive {len(tickets)} started from {offset}")
            for ticket in tickets:
                row={}
                ticket_id=ticket.get('id')
                print("ticket id",ticket_id)
                custom_fields=ticket.get('custom_fields',[])
                row["author"]=ticket.get("author","").get("name","")
                for field in custom_fields:
                    row[field['name']]=field['value']
                # ticket_id="51415"
                notes=get_notes(ticket_id,Apikey=APIKEY)
                note_txt=""
                if notes:
                    print("---------------ticket")
                    issue=notes.get("issue")
                    journals=issue.get('journals')
                    for journal in journals:
                        note=journal.get("notes")
                        if note :
                            note_txt+="\n"+str(note)
                row["notes"]=note_txt
                print(row)
                break

            # print(tickets)
        break

