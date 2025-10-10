
import sys
from flask import Flask, request,Response,send_file
import threading
import json
from flask_cors import CORS
import json
import os
import jsonify
import pandas as pd
# sys.path.append("./db_server")
from chroma.VectorSystem import PDFVectorSystem


appp = Flask(__name__)
documents_folder="./vol/documents"
feedback_file="./vol/feedbackall.csv"


if not os.path.exists(documents_folder):
# Create the directory
    os.makedirs(documents_folder,exist_ok=True) 



class FlaskdbServercls(threading.Thread):
    
    def read_cfg(self):
        with open("./api_cnf.json", 'r') as file:
            data = json.load(file)

        flask_threaded=data['model']["flask_threaded"]
        # Creating a dictionary with the extracted parameters
        params = {
            "flask_threaded":flask_threaded
        }
        return params
    
    def __init__(self,path_setting):
        super().__init__()
        # self.params_model=self.read_cfg(path_setting)
        self.pdf_system = PDFVectorSystem(
        aws_region='us-east-1',  # Change to your AWS region
        embedding_model='amazon.titan-embed-text-v1',  # Change to your preferred model
        chunk_size=1200,
        chunk_overlap=200,collection_name="KB_Text"
        )
        self.Qa_system = PDFVectorSystem(
        aws_region='us-east-1',  # Change to your AWS region
        embedding_model='amazon.titan-embed-text-v1',  # Change to your preferred model
        chunk_size=1200,
        chunk_overlap=200,collection_name="KB_QA"
        )
        
    def run(self):
        @appp.route("/", methods=["GET"])
        def index():
            return "REST Service for Vector Store"

        @appp.route('/add_file', methods=['POST'])
        def add_file():
            try:
                if 'file' not in request.files:
                    return jsonify({"error": "No file part"}), 400
                
                file = request.files['file']
                file_ext=str.split(file.filename,"/")[-1].split(".")[-1].lower()
            
                if file_ext=="pdf":
                    print("add pdf proccess")

                    self.pdf_system.add_document(file,documents_folder)
                elif file_ext=='csv':
                    print("add csv proccess")
                    self.Qa_system.add_document(file,documents_folder)

                message= "File uploaded successfully"
            except:
                message= "Error while uploading file"
            return Response(message, content_type='text/plain')

        @appp.route('/add_QA', methods=['POST'])
        def add_QA():
            try:
                question=request.form.get('question')
                answer=request.form.get('answer')

                self.Qa_system.add_QA(question,answer)
                message= "Question uploaded successfully"
            except:
                message= "Error while uploading file"
            return Response(message, content_type='text/plain')


        @appp.route('/get_context', methods=['POST'])
        def get_context():
            question = request.form.get('question')

            try:
                type_kb=request.form.get('type_kb')
                k=request.form.get('k',10)
                n=request.form.get('n',2)
            except:
                k=10
                n=2
                type_kb="KB_QA"

            try:
                print(type_kb)
                print(question)
                question=str(question)
                if type_kb=="kB_text":
                    context,context_json_=self.pdf_system.get_context_text(question,int(k),int(n))
                elif type_kb=="KB_QA":
                    context,context_json=self.Qa_system.get_context_text(question,int(k),int(n))
                    results=context_json['results']
                    tickets=""
                    for idx,item in  enumerate(results):
                        question=item['text']
                        answer=item["metadata"]['answer']
                        tickets+=f"\n ----- Ticket ---- \n disscussion and information : \n {answer}"
                message= tickets
                
            except Exception as e:
                print("error when finding context",str(e))
                message= "No context"
            return Response(message, content_type='text/plain')

        @appp.route('/get_chunks_inpage', methods=['POST'])
        def get_chunks_inpage():
            pdf_name = request.form.get('pdf_name')
            page_id = request.form.get('page_id')

            pages_info = self.pdf_system.list_pages_in_file(pdf_name)            
            if pages_info['exists'] and pages_info['pages']:
                first_page = pages_info['pages'][int(page_id)]['page_id']
                # print("id",first_page,pdf_name)
                print(f"\nChunks on page {first_page}:")
                page_chunks = self.pdf_system.find_chunks_by_file_and_page(pdf_name, first_page)
                # print(page_chunks)
                page_text=f"Page {first_page}"+ str.join("\n",page_chunks)
                
                for chunk in page_chunks['chunks']:
                    print(f"  - Chunk : {chunk}")

            return page_text


        @appp.route('/get_feedback_file', methods=['POST'])
        def get_feedback_file():
            # question = request.args.get('question')
            row_data = request.get_json()
            key=row_data["key"]
            if key=="ai4savfeedback":
                try:
                    # Path to the CSV file to send
                    csv_file_path = feedback_file

                    # Check if the file exists
                    file_exists_feedback = os.path.isfile(feedback_file)
                    
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
                file_exists_feedback = os.path.isfile(feedback_file)
                if not file_exists_feedback:
                    # column_names = ["id_data", "rate", "email", "reply", "reason", "correct_reply"]
                    column_names=list(row_data.keys())

                    df = pd.DataFrame(columns=column_names)
                    row_data_df = pd.DataFrame([row_data])
                    df = pd.concat([df, row_data_df], ignore_index=True)
                    df.to_csv(feedback_file, index=False)
                else:
                    df = pd.DataFrame([row_data])  # Convert row_data to a DataFrame
                    df.to_csv(feedback_file, mode='a', index=False, header=False)  # Append without writing the header
                response ='Success'
            except:
                response ='Failed'
            return Response(response, content_type='text/plain')
        
        @appp.route('/exit_delete', methods=["GET"])
        def exit():
            sys.exit()

        # appp.run(host="0.0.0.0", port=5009, debug=False, use_reloader=False,threaded=self.params_model["flask_threaded"])
        appp.run(host="0.0.0.0", port=5009, debug=False, use_reloader=False)
        # define features
        print("started API SERVER")






