
from flask import Flask, request,Response
from werkzeug.utils import secure_filename
import os
import pandas as pd
from components.Neo4jConnector import Neo4jConnector
from components.Graph import SimpleGraphHandler
from components.data_processing import read_file
from components.local_embeder import LocalEmbModel
from components.static_var import DOCUMENT_PATH,FEEDBACK_PATH
from components.data_processing import split_text_smart



appp = Flask(__name__)

# params_model=read_cfg(path_setting)
DBdriver=Neo4jConnector().driver
Emb_model=LocalEmbModel()

if Emb_model.model and DBdriver:
    print("Connected to db and initiat EmbModel")

Graphhandler=SimpleGraphHandler(driver=DBdriver,emb_model=Emb_model)





@appp.route("/", methods=["GET"])
def index():
    return "REST API for Vector Store"

@appp.route('/add_file', methods=['POST'])
def add_file():
    if 'file' not in request.files:
        message="No file "
        return Response(message, content_type='text/plain')
    file = request.files['file']
    
    #node root "ROOT"
    root_id="ROOT-001-124"
    # Node_id = request.form.get('Node_id') or "all analysers"

    # selected_analayser=request.form.get('selected_analayser') or "all analysers"

    split_type = request.form.get('split_type',"smart")   #smart , standard fix chunks 500 words and add all to same node simple_split
    use_md = request.form.get('use_md',"True") 
    chunk_length= request.form.get('chunk_length',"1000") 

    filename=file.filename
    
    try :
        #check if root exist else create one
        is_exist=Graphhandler.is_parent_exist(root_id)
        if not is_exist:
            Graphhandler.create_parent_node(root_id,"ROOT")

        # Now create file node :
        Node_id=Graphhandler.add_sentence_to_parent(root_id,filename,"0",filename,filename,filename)


        try:

            filename = secure_filename(file.filename)
            file.save(os.path.join(DOCUMENT_PATH, filename))

        except Exception as e:
            with open(os.path.join(DOCUMENT_PATH, filename), "wb") as f:
                f.write(file.getbuffer())
            print("error" , str(e))
            pass 


        # --------------read file in md format--------------
        is_Md,titles,data=read_file(filename,DOCUMENT_PATH)
        print(titles)
        if split_type=="smart":
            print("use split type ",split_type)
            print("use use_md",use_md)
            
            if is_Md and use_md=="True":
                #add from md format
                try:
                    Graphhandler.add_md_data(start_child=Node_id,tree=data,file_name=filename)
                except Exception as e:
                    print("Error adding md tree",str(e))
            # --------------read file pdf not MD format--------------
            else:
                #add from text
                chunck_max=int(chunk_length)
                chunks = split_text_smart(data, max_chunk_size=chunck_max, overlap=50)
                print("-----------all chunks---------",len(chunks))
                for id_, text in enumerate(chunks, 1):
                    print("------------chunk-----------",id_)
                    Graphhandler.add_txt_data(text,filename,Cat_id=Node_id)


        elif split_type=="standard":
            print("use split type ",split_type)
            print("use use_md",use_md)

            if is_Md and use_md=="True":
                #add from md format
                Graphhandler.add_md_data(start_child=Node_id,tree=data,file_name=filename)
            # --------------read file pdf not MD format--------------
            else:
                #add from md format
                # Graphhandler.add_txt_data(data,filename,Cat_id=Node_id)
                chunck_max=int(chunk_length)
                chunks = split_text_smart(data, max_chunk_size=chunck_max, overlap=50)
                print("-----------all chunks---------",len(chunks))

                for id_, text in enumerate(chunks, 1):
                    print("------------chunk-----------",id_)
                    #add describe function with LLM to better functionement
                    Graphhandler.add_sentence_to_parent(Node_id,text,"-1",text[1:5],text[1:5])

            print("simple chunks add")

        message= "Success"
    except Exception as e:
        
        message=f"Error when uploading {filename},{e}"
    return Response(message, content_type='text/plain')


@appp.route('/get_context', methods=['POST'])
def get_context_():
    # question = request.args.get('question')
    question = request.form.get('question')
    type_search=request.form.get('type_search')  #smart,similarity
    Node_id=request.form.get('Node_id') #id where start

    try:
        k=request.form.get('k')
        n=request.form.get('n')
    except:
        k=10
        n=2
    context="No context"
    print("--serch type: ",type_search)

    #--------------Smart search--------------
    if type_search=="smart":
        try:
            context=Graphhandler.search_recursive(Node_id,question)
        except:
            context="No context"
    #--------------Similarity search--------------
    elif type_search=="similarity":
        try:
            context=Graphhandler.search_similarity(question,"vector",k)
        except:
            context="No context"

    message= context
    return Response(message, content_type='text/plain')


@appp.route('/add_context', methods=['POST'])
def add_context_():
    # question = request.args.get('question')
    filename=str(request.form.get('filename')) or "None"
    Node_id = request.form.get('Node_id') or "1574"
    split_type = request.form.get('split_type') or "smart"  #smart , standard fix chunks 500 words and add all to same node simple_split
    chunk_length= request.form.get('chunk_length') or "1000"
    selected_analayser=request.form.get('selected_analayser') or "all analysers"
    
    context = str(request.form.get('context'))

    try:
        is_exist=Graphhandler.is_parent_exist(Node_id)
        if not is_exist:
            Graphhandler.create_parent_node(Node_id,selected_analayser)
        
        if split_type=="smart":
            print("use split type ",split_type)
            Graphhandler.add_txt_data(context,filename,Cat_id=Node_id)

        elif split_type=="standard":
            chunck_max=int(chunk_length)

            print("use split type ",split_type,"chunk_size",chunck_max)
            chunks = split_text_smart(context, max_chunk_size=chunck_max, overlap=50)

            for id_, text in enumerate(chunks, 1):
                #add describe function with LLM to better functionement
                Graphhandler.add_sentence_to_parent(Node_id,text,"-1",text[1:5],text[1:5])
        
        message= "added context success"
    except Exception as e:
        print(str(e))
        message= "context error"

    return Response(message, content_type='text/plain')


@appp.route('/get_feedback_file', methods=['POST'])
def get_feedback_file():
    # question = request.args.get('question')
    row_data = request.get_json()
    key=row_data["key"]
    if key=="ai4savfeedback":
        try:
            # Path to the CSV file to send
            csv_file_path = FEEDBACK_PATH

            # Check if the file exists
            file_exists_feedback = os.path.isfile(FEEDBACK_PATH)
            
            if not file_exists_feedback:
                return "CSV file not found!", 404
            else:
                with open(csv_file_path, 'r', encoding='utf-8') as file:
                    csv_content = file.read()

                # Send the file content as a response
                return Response(
                    csv_content,
                    mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=existing_file.csv"}
                )
            # Send the file as an attachment
            # return send_file(csv_file_path, as_attachment=True, mimetype='text/csv')
        except Exception as e:
            return str(e), 500
    else:
        return "Security key incorrect!", 404

@appp.route('/add_feedback', methods=['POST'])
def add_feedback():
    try:
        row_data = request.get_json()

        file_exists_feedback = os.path.isfile(FEEDBACK_PATH)
        
        if not file_exists_feedback:

            # column_names = ["id_data", "rate", "email", "reply", "reason", "correct_reply"]
            column_names=list(row_data.keys())

            df = pd.DataFrame(columns=column_names)
            row_data_df = pd.DataFrame([row_data])
            df = pd.concat([df, row_data_df], ignore_index=True)
            df.to_csv(FEEDBACK_PATH, index=False)

        else:

            df = pd.DataFrame([row_data])  # Convert row_data to a DataFrame
            df.to_csv(FEEDBACK_PATH, mode='a', index=False, header=False)  # Append without writing the header

        response ='Success'
        
    except:
        response ='Failed'

    return Response(response, content_type='text/plain')


#appp.run(host="0.0.0.0", port=5009, debug=False, use_reloader=False,threaded=params_model["flask_threaded"])


if __name__=="__main__":
    appp.run(host="0.0.0.0", port=5009, debug=True, use_reloader=True)
    # define features
    print("started API SERVER")


