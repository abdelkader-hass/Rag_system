
from neo4j import GraphDatabase
import uuid
from neo4j_graphrag.retrievers import VectorRetriever, VectorCypherRetriever
from neo4j_graphrag.indexes import create_vector_index
from .local_embeder import LocalEmbModel
from litellm import completion
from concurrent.futures import ThreadPoolExecutor, as_completed
import ast,re,json

#--------------------
from .static_var import NEO4J_URI ,NEO4J_USER ,NEO4J_PASSWORD ,DB ,RATE_LIMITER,SYSTEM_PROMPT,MODEL_NAME,PROVIDER
from .static_var import AformatSEARCH,AnswerFormat,Aformat,SYSTEM__SEARCH_PROMPT_answer,SYSTEM_SEARCH_PROMPT,MAX_WORKERS


class SimpleGraphHandler:
    
    def __init__(self, uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD,db=DB,driver=None,emb_model=None):
        if driver :
            self.driver=driver
            self.session = self.driver.session() 
        else:
            self.driver = GraphDatabase.driver(uri, auth=(user, password),database=db)
            self.session = self.driver.session() 
        if emb_model :
            self.emb_model=emb_model
        else:
            self.emb_model = LocalEmbModel()
        
        self.QUEUE=[]

    #add to graph

    def create_parent_node(self,node_id=None,name="random"):
        """
        Creates a parent node with a unique ID and name.

        Args:
            name (str): The name of the parent node.

        Returns:
            str: The unique ID of the created node, or None if creation failed.
        """
        if not self.driver:
            print("Not connected to Neo4j. Please connect first.")
            return None
        if not id:
            node_id = str(uuid.uuid4())  # Generate a unique ID
        query = (
            "CREATE (p:Parent {id: $id, name: $name})"
            "RETURN p.id AS id"
        )
        parameters = {"id": node_id, "name": name}

        try:
            result = self.session.run(query, parameters)
            record = result.single() # Get the single record returned
            if record:
                return node_id # Access the 'id' from the record

            else:
                print("Parent node creation failed: No ID returned.")
                return None
            
        except Exception as e:
            print(f"Error creating parent node: {e}")
            return None


    def add_sentence_to_parent(self, parent_id=None, sentence="",ordre="",title="",description="",file_name=""):
        if not parent_id:
            return ''
        if not self.driver:
            print("Not connected to Neo4j. Please connect first.")
            return

        child_id = str(uuid.uuid4())  # Generate a unique ID for the child

        query_find_parent = """
        MATCH (p:Parent {id: $parent_id})
        RETURN p
        """

        query_create_child_under_parent = """
        MATCH (p:Parent {id: $parent_id})
        CREATE (c:Sentence {name:$title,description:$description,parent_id:$parent_id,id: $child_id,ordre:$ordre, text: $sentence,embedding:$embedding,file_name:$file_name})
        CREATE (p)-[:CONTAINS]->(c)
        RETURN c
        """
        
        query_convert_and_create_child = """
            MATCH (n {id: $parent_id})
            REMOVE n:Sentence
            SET n :Parent
            REMOVE n.embedding
            CREATE (c:Sentence {name:$title,description:$description,parent_id:$parent_id, id: $child_id,ordre:$ordre, text: $sentence, embedding: $embedding,file_name:$file_name})
            CREATE (n)-[:CONTAINS]->(c)
            RETURN c
        """

        title_embedding = self.emb_model.generate_embeddings([sentence])[0]
        parameters = {"parent_id": parent_id, "child_id": child_id, "sentence": sentence,"embedding":title_embedding.tolist(),"ordre":ordre,"title":title,"description":description,"file_name":file_name}

        try:
                # First, check if a Parent node exists with the given id
            result = self.session.run(query_find_parent, {"parent_id": parent_id})
            record = result.single()

            if record:
                # Parent found, add the child
                self.session.run(query_create_child_under_parent, parameters)
                # print(f"Sentence added to existing parent with ID: {parent_id}")
            else:
                # No parent found, convert node to Parent and add child
                self.session.run(query_convert_and_create_child, parameters)
                # print(f"Node converted to parent and sentence added with ID: {parent_id}")
            return child_id
        except Exception as e:
            print(f"Error adding child node: {e}")

    
    # ------------------Simple MD add to graph parent-child ------------------

    def add_md_data(self,start_child=None,tree=[],file_name=""):
        try:
            if tree and start_child:
                ordre=0
                for node in tree:
                    id=node.get("id","")
                    title=node.get("title","")
                    
                    text=title+node.get("text","")
                    description=title
                    node_child_id=self.add_sentence_to_parent(start_child, text,str(ordre),title,description,file_name)
                    # child=(node_child_id,part_text,description,title)
                    ordre+=1
                    children=node.get("children",[])
                    if children:
                        self.add_md_data(start_child=node_child_id,tree=children,file_name=file_name)
            else:
                print("Tree is empty")
            return True
        except Exception as e:
            print("error when adding md format",str(e))
            return False
    
    
    # ------------------Recursive split and add------------------
    
    def add_txt_data(self,txt="",file_name="",Cat_id=""):  
        #---------add doc name
        # Cat_id="5300c1b7-f38e-4f49-b945-f5a45e2bb554"
        #if not find cat add parent 
        # NEO4J_CONNECTOR.create_parent_node("CEM500")
        child=(Cat_id,txt)
        
    #--------- start loop 
        self.QUEUE.append(child)
        i=0
        First_text=True
        while len(self.QUEUE)!=0:
            # print("-------------------len self.QUEUE-------------",len(self.QUEUE))
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                # Submit all jobs, track original item with future
                future_to_item = {
                    executor.submit(
                        self.recursive_split,
                        item[0],
                        item[1],
                        None,file_name,First_text
                    ): item for item in self.QUEUE
                }
                for idse,future in enumerate(as_completed(future_to_item)):
                    item = future_to_item[future]
                    try:
                        result = future.result()
                        self.QUEUE.remove(item)
                        
                    except Exception as e:
                        print(f"Error in item {idse}: {e}")

                print(f"Completed successfully: {idse}")
        First_text=False
        
        return True


    #-----------------------------------
    def split(self,text="",previous_nodes=[]):
        try:
            result_json={}

            previous_nodes=f"""
                {previous_nodes}
            """
            if PROVIDER=="Bedrock":
                messages =[{"role": "user","content":SYSTEM_PROMPT},
                        {"role":"assistant","content":"now give me the input text"},
                        {"role":"user","content":f"Text :{text}"},
                    ]
            else:
                messages =[{"role": "system","content":SYSTEM_PROMPT},
                    {"role":"assistant","content":"now give me the input text"},
                    {"role":"user","content":f"Text :{text}"},
                ]
            # titles=[{"role":"assistant","content":"now give me the previous_titles"},
            #     {"role":"user","content":f"previous_nodes :{previous_nodes}"}]
            # messages.extend(titles)
            RATE_LIMITER.acquire()
            resp = completion(
                model=MODEL_NAME,
                messages=messages,
                response_format=Aformat
            )
            result_json=json.loads(resp.choices[0].message.content)
            return result_json
        except Exception as e:
            print("error run search",str(e))
            return False

    def save_parts_bd(self,id_parent="",text="",json_data={},file_name="",First_text=False):
            try:
                # print(json_data)
                text=re.sub(r'\s+', ' ', text).strip()
                if isinstance(json_data, str):
                    parts = json.loads(json_data)
                elif isinstance(json_data, dict):
                    parts = json_data.get("parts",[])
                else:
                    raise ValueError("json_data must be a JSON string or a Python list.")
                if len(parts)!=0:
                    try :
                        for ordre,part in enumerate(parts):
                            title = part["title"]
                            description = part["description"]
                            start_sentence=part["start_sentence"]
                            end_sentence=part["end_sentence"]
                            start_index = text.find(start_sentence)
                            end_index = text.find(end_sentence)

                            if start_index == -1 or end_index == -1:
                                raise ValueError("Start or end sentence not found in the text.")
                            end_index += len(end_sentence)
                            part_text=text[start_index:end_index]

                            node_child_id=self.add_sentence_to_parent(id_parent, part_text,str(ordre),title,description,file_name)
                            # child=(node_child_id,part_text,description,title)
                            child=(node_child_id,part_text)
                            self.QUEUE.append(child)
                        # print(title+" Added to db",node_child_id)
                    except:
                        node_child_id=self.add_sentence_to_parent(id_parent, text,0,title="",description=json_data.get("text_description",""),file_name=file_name)

                elif len(parts)==0 and First_text :
                    print(json_data.get("text_description","No text description found"))
                    node_child_id=self.add_sentence_to_parent(id_parent, text,0,title="",description=json_data.get("text_description",""),file_name=file_name)
                return True
            except Exception as e :
                print("error savedb",str(e))
                return False

    def recursive_split(self,id_parent="",text="",previous_nodes=[],file_name="",First_text=False):
        # previous_nodes =self.create_tree_dict(id_parent)
        previous_nodes=[]
        result=self.split(text=text,previous_nodes=previous_nodes)
        j=0
        while not result and j<3:
            print("loop run_search---")
            result=self.split(text=text,previous_nodes=previous_nodes)
            j+=1
        if result:
            bool=self.save_parts_bd(id_parent=id_parent,text=text,json_data=result,file_name=file_name,First_text=First_text)
            i=0
            while not bool and i<3:
                print("loop db---")
                bool=self.save_parts_bd(id_parent=id_parent,text=text,json_data=result)
                i+=1
            if not bool:
                return False
        else:
            return False
        
        return True


    #------------------Get infos and tree

    def create_tree_dict(self, start_node_id=None):
        if start_node_id is None:
            # Find root node
            query = """
            MATCH (root) 
            WHERE NOT ()-[:CONTAINS]->(root) AND root.id IS NOT NULL
            RETURN root.id as node_id 
            LIMIT 1
            """
            result = self.session.run(query).single()
            if result:
                start_node_id = result["node_id"]
            else:
                print("No root node found!")
                return None
        return self._build_node_tree(self.session, start_node_id)
    
    def _build_node_tree(self, session, node_id,description=""):
        """Build tree recursively"""
        
        # Get children IDs
        query = """
        MATCH (parent)-[:CONTAINS]->(child)
        WHERE parent.id = $node_id AND child.id IS NOT NULL
        RETURN child.id as child_id ,child.description as description
        ORDER BY child.id
        """
        result = session.run(query, node_id=node_id)
        child_ids = [(record["child_id"], record["description"]) for record in result]
        
        # print(f"  Found {len(child_ids)} children for node {node_id}: {child_ids}")
        
        # Build node dict
        node_dict = {
            "id": node_id,
            "description":description,
            "childrens": []
        }
        return child_ids
    
    def get_node_data(self, node_id):
        """
        Get node data by ID
        Returns: {"name": "...", "title": "...", "description": "..."}
        """
        try:
            query = """
            MATCH (n) WHERE n.id = $node_id
            RETURN n.id as id , n.text as text , n.parent_id as parent_id
            """
            result = self.session.run(query, node_id=node_id).single()
            
            if result:
                return {
                    "id": node_id or "",
                    "text": result.get("text",""),
                    "parent_id": result.get("parent_id","")
                }
            return {}
        except:
            print("error get_node_data id ",node_id)
            return {}

    def is_parent_exist(self, node_id):
        try:
            query = """
            MATCH (n) WHERE n.id = $node_id
            RETURN n.id as id
            """
            result = self.session.run(query, node_id=node_id).single()
            
            if result:
                return True
            return False
        except:
            return False


    #Search from grapgh  -------------------
    def search_similarity(self,query="",retriever_type='vector',top_k=5):

        # Initialize the wrapped embedder
        embedder = self.emb_model

        # Get embedding dimensions
        sample_embedding = embedder.embed_query("test")
        embedding_dim = len(sample_embedding)

        # Create vector index with correct dimensions
        create_vector_index(
            self.driver, 
            name="sav_embeddings", 
            label="Sentence",
            embedding_property="embedding", 
            dimensions=embedding_dim,  # Use actual embedding dimensions
            similarity_fn="cosine"
        )

        # Basic Vector Retriever (works with your current structure)
        vector_retriever = VectorRetriever(
            self.driver,
            index_name="sav_embeddings",
            embedder=embedder,
            return_properties=["text", "id","parent_id"],
        )

        # Modified GraphRAG Vector Cypher Retriever for your structure
        graph_retriever = VectorCypherRetriever(
            self.driver,
            index_name="sav_embeddings",
            embedder=embedder,
            retrieval_query="""
                WITH node AS e

                MATCH (s:Sentence)
                WHERE s.parent_id = e.parent_id

                //WITH e, s
                //ORDER BY s.ordre  // Replace 'ordre' with your actual ordering property if you have one

                RETURN
                    collect(s.text) AS sibling_texts

            """
        )

        # Alternative retrieval query that uses your category structure
        # Usage example
        if retriever_type == "vector":
            results = vector_retriever.search(query_text=query, top_k=top_k)
        elif retriever_type == "graph":
            results = graph_retriever.search(query_text=query, top_k=top_k)
        context=""""""

        if results:
            for item in results.items:
                data_dict = ast.literal_eval(item.content)
                text=data_dict['text']
                context+=f"""
                {text}"""
        return context

    # Recursive Search -------

    def llm_select_nodes(self,nodes=[],question=""):
        try:
            print("start llm")
            result_json={}
            re=f"""
                {nodes}
            """
            if PROVIDER=="Bedrock":
                messages =[{"role": "user","content":SYSTEM_SEARCH_PROMPT},
                        {"role":"assistant","content":"now give me list of nodes"},
                        {"role":"user","content":f" Nodes {re}"},
                        {"role":"assistant","content":"now give me your question"},
                        {"role":"user","content":f"Question :{question}"},
                    ]
            else:
                messages =[{"role": "system","content":SYSTEM_SEARCH_PROMPT},
                    {"role":"assistant","content":"now give me list of nodes"},
                    {"role":"user","content":f" Nodes {re}"},
                    {"role":"assistant","content":"now give me your question"},
                    {"role":"user","content":f"Question :{question}"},
                ]
            RATE_LIMITER.acquire()
            resp = completion(
                model=MODEL_NAME,
                messages=messages,
                response_format=AformatSEARCH
            )
            
            result_json=json.loads(resp.choices[0].message.content)

            if result_json:
                ids=[node['id'] for node in result_json["nodes"]]
                print("okay result llm select")
                return ids
            else:
                print("node nodes")
                return []

        except Exception as e:
            print("error run llm_select_nodes",str(e))

            return []

    def search_recursive(self,start_id=None,question="no question"):
        try:
            if not start_id:
                return "no context"
            ITERATION_QUEUE=[]
            SELECTED_NODES_IDS=[]
            ITERATION_QUEUE.append(start_id)
            
            cpt=0
            last_res=[]
            while ITERATION_QUEUE :
                Temp=[]
                # at each level iterte all queue and get all children and them to queue
                for id_q in  ITERATION_QUEUE:
                    tree = self.create_tree_dict(start_node_id=id_q)
                    if len(tree)==0:
                        SELECTED_NODES_IDS.append(id_q)
                    else:
                        Temp.extend(tree)

                selected_ids=self.llm_select_nodes(nodes=Temp,question=question)
                if selected_ids:
                    if last_res==selected_ids:
                        ITERATION_QUEUE=[]
                    else:
                        last_res=selected_ids
                        ITERATION_QUEUE=selected_ids
                else:
                    ITERATION_QUEUE=[]
                    t=SELECTED_NODES_IDS.copy()
                    for i in Temp:
                        t.append(i[0])
                    SELECTED_NODES_IDS=t
                cpt+=1
            context=""" """

            print("Selected NODES IDS",SELECTED_NODES_IDS)
            for last_id in SELECTED_NODES_IDS:
                node_data = self.get_node_data(last_id)
                text=node_data.get("text","No context")
                context+=f"""{text} \n---------------------"""
            
            return context
        except Exception as e:
            print(str(e))
            return "No context "
        
    #---------------------
    def answer_question(question="" , context=""):
        try:
            result_json={}
            if PROVIDER=="Bedrock":
                messages =[{"role": "user","content":SYSTEM__SEARCH_PROMPT_answer},
                {"role":"assistant","content":"now give me the context"},
                {"role":"user","content":f"{context}"},
                {"role":"assistant","content":"now give me your question"},
                {"role":"user","content":f"Question :{question}"},
                ]
            
            else:
                messages =[{"role": "system","content":SYSTEM__SEARCH_PROMPT_answer},
                        {"role":"assistant","content":"now give me the context"},
                        {"role":"user","content":f"{context}"},
                        {"role":"assistant","content":"now give me your question"},
                        {"role":"user","content":f"Question :{question}"},
                    ]
                
            RATE_LIMITER.acquire()
            resp = completion(
                model=MODEL_NAME,
                messages=messages,
                response_format=AnswerFormat
            )
            
            result_json=json.loads(resp.choices[0].message.content)

            return result_json["answer_md_format"],result_json['bool_answer_find_or_not']
        except Exception as e:
            print("error run answer",str(e))
            return "error no asnwer"
