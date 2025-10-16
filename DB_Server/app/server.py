
from flask import Flask, request,Response,jsonify,send_file
from werkzeug.utils import secure_filename
import os
import pandas as pd
from components.Neo4jConnector import Neo4jConnector
from components.Graph import SimpleGraphHandler
from components.data_processing import read_file
from components.local_embeder import LocalEmbModel
from components.static_var import DOCUMENT_PATH,FEEDBACK_PATH,JSON_UIDS_PATH,IMAGES_PATH,SETTINGS_FILE
import json
from components.LLM import classify_text_with_bedrock



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
        return Response(message,status=500, content_type='text/plain')
    file = request.files['file']

    if os.path.exists(JSON_UIDS_PATH):
        with open(JSON_UIDS_PATH, "r", encoding="utf-8") as f:
            nodes_uids = json.load(f)
    else:
        nodes_uids = {"root": {"nodes_uids":{}}}
    #node root "ROOT"
    root_id="ROOT-001-124"
    # Node_id = request.form.get('Node_id') or "all analysers"

    # selected_analayser=request.form.get('selected_analayser') or "all analysers"

    split_type = request.form.get('split_type',"smart")   #smart , standard fix chunks 500 words and add all to same node simple_split
    use_md = request.form.get('use_md',"True") 
    chunk_length= int(request.form.get('chunk_length',1000))
    part_size=int(request.form.get('part_size',300))
    extract_image= request.form.get('extract_image',"True")

    try:
        categories_received=request.form.get('categories').split(",")
    except:
        categories_received=[]
    device=request.form.get('device',None)

    filename=file.filename
    
    try :
        #check if root exist else create one
        is_exist=Graphhandler.is_parent_exist(root_id)
        if not is_exist:
            Graphhandler.create_parent_node(root_id,"ROOT")

        if device not in nodes_uids["root"]["nodes_uids"]:
            # Now create file node :
            Device_id,_=Graphhandler.add_sentence_to_parent(parent_id=root_id,parent_name="root",description=device)
            nodes_uids["root"]["nodes_uids"][device]={"id":Device_id,"categories":{}}

        else:
            Device_id=nodes_uids["root"]["nodes_uids"][device]['id']
        try:
            
            filename = secure_filename(file.filename)
            if os.path.exists(os.path.join(DOCUMENT_PATH, filename)):
                return Response('File exist already',status=500, content_type='text/plain') 
            file.save(os.path.join(DOCUMENT_PATH, filename))

        except Exception as e:
            with open(os.path.join(DOCUMENT_PATH, filename), "wb") as f:
                f.write(file.getbuffer())
            print("error" , str(e))
            pass
        categories=categories_received+["ALL","Q&A"]
        for cat in categories:
            if cat not in nodes_uids["root"]["nodes_uids"][device]['categories']:
                # Now create file node :
                Cat_id,_=Graphhandler.add_sentence_to_parent(parent_id=Device_id,parent_name="root!-!"+device,description=cat)

                nodes_uids["root"]["nodes_uids"][device]["categories"][cat]=Cat_id

        categories_ids=nodes_uids["root"]["nodes_uids"][device]["categories"]
        with open(JSON_UIDS_PATH, "w", encoding="utf-8") as f:
            json.dump(nodes_uids, f, indent=4)
        # --------------read file in md format--------------
        # is_Md,titles,data=read_file(filename,DOCUMENT_PATH,use_md)
        #add categories&Equipements get it from request

        chunks=read_file(file_name=filename,documents_folder=DOCUMENT_PATH,is_md=use_md,chunk_length=chunk_length,part_size=part_size)

        previous_cat_id=None
        previous_cat_name=None
        previous_reason=None
        embedding=None
        cpt=0
        cpt1=0
        for chunk in chunks:
            cpt1+=1
            chunk_id=chunk["chunk_id"]
            doc_name=chunk["doc_name"]
            titles=chunk["titles"]
            text=chunk["text"]
            is_has_other_part=chunk["is_has_other_part"]
            chunk_node_id_,embedding=Graphhandler.add_sentence_to_parent(parent_id=categories_ids['ALL'],parent_name=f"root!-!{device}!-!ALL"
                                                          ,sentence=text,ordre=str(chunk_id),title=titles,file_name=doc_name,type_data="text")
            try:
                if categories_received:

                    if is_has_other_part :
                        if previous_cat_id :
                            # print("use previous",chunk_id,previous_cat_id)
                            category_id=previous_cat_id
                            category_name=previous_cat_name
                            reason=previous_reason
                            previous_cat_id=None
                            previous_cat_name=None
                            previous_reason=None
                        else:
                            result_json=classify_text_with_bedrock(text,str(categories_ids))
                            category_id=result_json["category_id"]
                            category_name=result_json["category_name"]
                            reason=result_json["reason"]

                            if categories_ids.get(category_name,None):
                                previous_cat_id=categories_ids[category_name]
                                previous_cat_name=category_name
                                previous_reason=reason
                                category_id=categories_ids[category_name]
                            else:
                                print("Error chunk",chunk_id)
                                continue
                    else:
                        if previous_cat_id:
                            # print("use previous",chunk_id,previous_cat_id)
                            category_id=previous_cat_id
                            category_name=previous_cat_name
                            reason=previous_reason
                            previous_cat_id=None
                            previous_cat_name=None
                            previous_reason=None
                        else:
                            result_json=classify_text_with_bedrock(text,str(categories_ids))
                            category_id=result_json["category_id"]
                            category_name=result_json["category_name"]
                            reason=result_json["reason"]
                            if categories_ids.get(category_name,None):
                                category_id=categories_ids[category_name]
                            else:
                                print("Error chunk",chunk_id)
                                continue

                    chunk_node_id,_=Graphhandler.add_sentence_to_parent(parent_id=category_id,parent_name=f"root!-!{device}!-!{category_name}"
                                                    ,sentence=text,ordre=str(chunk_id),title=titles,file_name=doc_name,description=str(reason),embedding=embedding,type_data="text")
            except:
                continue
            cpt+=1
        print("treated",cpt,"viewed",cpt1)
        #so use categories
        # print(chunks)
        if len(chunks)==0:
            message= "Empty File or error durring processing"
        else:
            message= "Success"
        return Response(message,status=200, content_type='text/plain')
    except Exception as e:
        message=f"Error when uploading {filename},{e}"
        print(message)
        return Response(message,status=500, content_type='text/plain')


@appp.route('/add_file_QA', methods=['POST'])
def add_file_QA():
    if 'file' not in request.files:
        message="No file "
        return Response(message, content_type='text/plain')
    file = request.files['file']

    if os.path.exists(JSON_UIDS_PATH):
        with open(JSON_UIDS_PATH, "r", encoding="utf-8") as f:
            nodes_uids = json.load(f)
    else:
        nodes_uids = {"root": {"nodes_uids":{}}}
    #node root "ROOT"
    root_id="ROOT-001-124"

    device=request.form.get('device',None)
    delimiter=request.form.get('delimiter',None)

    filename=file.filename
    file_path=os.path.join(DOCUMENT_PATH, filename)
    try :
        #check if root exist else create one
        is_exist=Graphhandler.is_parent_exist(root_id)
        if not is_exist:
            Graphhandler.create_parent_node(root_id,"ROOT")

        if device not in nodes_uids["root"]["nodes_uids"]:
            # Now create file node :
            Device_id,_=Graphhandler.add_sentence_to_parent(parent_id=root_id,parent_name="root",description=device)
            nodes_uids["root"]["nodes_uids"][device]={"id":Device_id,"categories":{}}
        else:
            Device_id=nodes_uids["root"]["nodes_uids"][device]['id']
        try:
            
            filename = secure_filename(file.filename)
            if os.path.exists(file_path):
                return Response('File exist already',status=500, content_type='text/plain') 
            file.save(file_path)

        except Exception as e:
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            print("error" , str(e))
            pass
        categories=["Q&A"]
        for cat in categories:
            if cat not in nodes_uids["root"]["nodes_uids"][device]['categories']:
                # Now create file node :
                Cat_id,_=Graphhandler.add_sentence_to_parent(parent_id=Device_id,parent_name="root!-!"+device,description=cat)

                nodes_uids["root"]["nodes_uids"][device]["categories"][cat]=Cat_id

        categories_ids=nodes_uids["root"]["nodes_uids"][device]["categories"]
        category_id=categories_ids['Q&A']

        with open(JSON_UIDS_PATH, "w", encoding="utf-8") as f:
            json.dump(nodes_uids, f, indent=4)
        # --------------read csv file --------------

        df = pd.read_csv(file_path,delimiter=delimiter)

        # Loop through each row (question = text, answer = metadata)
        for idx, row in df.iterrows():
            question = str(row.get("question", "")).strip()
            answer = str(row.get("answer", "")).strip()

            chunk_id=idx
            doc_name=filename
            titles=""
            text=question

            chunk_node_id,_=Graphhandler.add_sentence_to_parent(parent_id=category_id,parent_name=f"root!-!{device}!-!Q&A"
                                            ,sentence=text,ordre=str(chunk_id),type_data="Q&A",title=titles,file_name=doc_name,description=str(answer),embedding=None)
        message= "Success"
        return Response(message,status=200, content_type='text/plain')
    except Exception as e:

        message=f"Error when uploading {filename},{e}"
        return Response(message,status=500, content_type='text/plain')


@appp.route('/get_context', methods=['POST'])
def get_context_():
    # question = request.args.get('question')
    question = request.form.get('question')
    type_search=request.form.get('type_search')  #smart,similarity
    device=request.form.get('device',None)
    k=request.form.get('k',10)
    n=request.form.get('n',2)
    use_categories=request.form.get('use_categories',None)
    context=""
    context_QA=""
    print("--serch type: ",type_search)

    #--------------Similarity search--------------
    if type_search=="similarity":
        try:
            if device:
                #get context from Q&A
                filters={"parent_name":f"root!-!{device}!-!Q&A"}
                context_QA=Graphhandler.search_similarity(question,"vector",k,device,filters=filters)
                # print("ALL Questions device",device)
                # print(context_QA)
                if os.path.exists(JSON_UIDS_PATH):
                    with open(JSON_UIDS_PATH, "r", encoding="utf-8") as f:
                        nodes_uids = json.load(f)
                    categories_ids=nodes_uids["root"]["nodes_uids"][device]["categories"]
                    categories_ids={i:categories_ids[i] for i in categories_ids if i not in ["Q&A","ALL"]}
                    # print("wraped categories",categories_ids)
                else:
                    nodes_uids = {"root": {"nodes_uids":{}}}
                    categories_ids=None
                
                if categories_ids and use_categories:

                    #get context from docs if device defined:
                    result_json=classify_text_with_bedrock(question,str(categories_ids))
                    category_id=result_json["category_id"]
                    category_name=result_json["category_name"]
                    # print("Detected category",category_name)

                    reason=result_json["reason"]
                    if categories_ids.get(category_name,None):  
                        filters={"parent_name":f"root!-!{device}!-!{category_name}"}
                        context=Graphhandler.search_similarity(question,"vector",k,device,filters=filters)
                        # print("data from",device,"category",category_name)
                        # print(context)
                    else:
                        # print("ALL data device",device)
                        filters={"parent_name":f"root!-!{device}!-!ALL"}
                        context=Graphhandler.search_similarity(question,"vector",k,device,filters=filters)
                        # print(context)
                else:
                    # print("ALL data device",device)
                    filters={"parent_name":f"root!-!{device}!-!ALL"}
                    context=Graphhandler.search_similarity(question,"vector",k,device,filters=filters)
                    # print(context)

            else:
                context_QA=Graphhandler.search_similarity(question,"vector",k,device,filters={"type":f"Q&A"})
                # print("ALL Questions")
                # print(context_QA)
                context=Graphhandler.search_similarity(question,"vector",k,device,filters={"type":f"text"})
                # print("ALL data device")
                # print(context)

        except Exception as e:
            print("error get_context",str(e))
            context="No context"
            context_QA="No context"

    message={"Q&A":context_QA,"text":context}

    return jsonify(message), 200



@appp.route('/download_image', methods=['POST'])
def download_image():
    data = request.get_json()
    if not data or 'image_name' not in data:
        return jsonify({"error": "Missing 'image_name' in request body"}), 400

    image_name = data['image_name']
    image_path = os.path.join(IMAGES_PATH, image_name)

    # Check if image exists on the server
    if not os.path.exists(image_path):
        return jsonify({"error": f"Image '{image_name}' not found on server"}), 404

    # Return image file
    return send_file(image_path, as_attachment=True)




@appp.route('/set_settings', methods=['POST'])
def set_settings():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Save JSON directly to file
        # os.makedirs(BASE_DIR, exist_ok=True)
        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f, indent=4)
            
        return jsonify({
            "message": "Settings saved successfully",
            "file_path": SETTINGS_FILE
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



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
    appp.run(host="0.0.0.0", port=5009, debug=True, use_reloader=False)
    # define features
    print("started API SERVER")


