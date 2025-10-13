
from neo4j import GraphDatabase
import uuid
from neo4j_graphrag.retrievers import VectorRetriever, VectorCypherRetriever
from neo4j_graphrag.indexes import create_vector_index
from .local_embeder import LocalEmbModel
from litellm import completion
from concurrent.futures import ThreadPoolExecutor, as_completed
import ast,re,json
import boto3

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


    def add_sentence_to_parent(self, parent_id=None,parent_name=None,type_data="", sentence=" no",ordre="",title="",description="",file_name="",embedding=None):
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
        CREATE (c:Sentence {name:$title,description:$description,parent_id:$parent_id,parent_name:$parent_name,type:$type,id: $child_id,ordre:$ordre, text: $sentence,embedding:$embedding,len_embedding:$len_embedding,file_name:$file_name})
        CREATE (p)-[:CONTAINS]->(c)
        RETURN c
        """
        
        query_convert_and_create_child = """
            MATCH (n {id: $parent_id})
            REMOVE n:Sentence
            SET n :Parent
            REMOVE n.embedding
            CREATE (c:Sentence {name:$title,description:$description,parent_id:$parent_id,parent_name:$parent_name,type:$type, id: $child_id,ordre:$ordre, text: $sentence, embedding: $embedding,len_embedding:$len_embedding,file_name:$file_name})
            CREATE (n)-[:CONTAINS]->(c)
            RETURN c
        """

        try:

            if embedding:
                title_embedding=embedding
            else:
                title_embedding=self.emb_model.generate_embeddings([sentence])
        except Exception as e:
            print('error embedding chunk', str(e))
        parameters = {"parent_id": parent_id,"parent_name":parent_name, "child_id": child_id,"type":type_data, "sentence": sentence,"embedding":title_embedding,"len_embedding":len(title_embedding),"ordre":ordre,"title":title,"description":description,"file_name":file_name}

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
            return child_id,title_embedding
        except Exception as e:
            print(f"Error adding child node: {e}")

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
    def search_similarity(self,query="",retriever_type='vector',top_k=5,device=None,filters=None):
        try:
            # Initialize the wrapped embedder
            embedder = self.emb_model
            # Get embedding dimensions
            sample_embedding = embedder.embed_query("test")
            embedding_dim = len(sample_embedding)
            # Create vector index with correct dimensions
            try:
                create_vector_index(
                    self.driver, 
                    name="sav1_embeddings", 
                    label="Sentence",
                    embedding_property="embedding", 
                    dimensions=embedding_dim,  # Use actual embedding dimensions
                    similarity_fn="cosine"
                )
            except Exception as e:
                print("Exception create vector index",str(e))
            try:
                # Basic Vector Retriever (works with your current structure)
                vector_retriever = VectorRetriever(
                    self.driver,
                    index_name="sav1_embeddings",
                    embedder=embedder,
                    return_properties=["text", "id","parent_id","parent_name","type","description"]
                )
            except Exception as e:
                print("Exception crete VectorRetriever",str(e))
            # Modified GraphRAG Vector Cypher Retriever for your structure
            # Alternative retrieval query that uses your category structure
            # Usage example
            if retriever_type == "vector":
                try:    
                    results = vector_retriever.search(query_text=query, top_k=top_k,filters=filters)
                except Exception as e:
                    print("error vector_retreiver",str(e))


            context=""""""
            if results:
                for item in results.items:
                    data_dict = ast.literal_eval(item.content)
                    if data_dict["type"]=="Q&A":
                        text="question: "+data_dict['text'] +"-- answer"+data_dict['description']
                    else:
                        text=data_dict['text']
                    # print(data_dict['parent_name'])
                    context+=f"""
                    {text}"""
            return context
        except Exception as e :
            print("error search_similarity",str(e))
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
