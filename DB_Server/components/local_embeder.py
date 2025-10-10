
from .static_var import EMB_MODEL_PATH,FEMB_MODEL_PATH,EMB_DEVICE
import os
import numpy as np
import boto3
import json

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    print("SentenceTransformers not available, using fallback embedding method")
    SENTENCE_TRANSFORMERS_AVAILABLE = False



class LocalEmbModel:
    
    def __init__(self):
        self.model=None
        self.setup()
        self.get_local_model()

    def download_model_locally(self):
        """Download the SentenceTransformer model to local directory"""
        try:
            from sentence_transformers import SentenceTransformer
            
            # Create models directory
            os.makedirs(EMB_MODEL_PATH,exist_ok=True)
            model_path = EMB_MODEL_PATH+'/all-MiniLM-L6-v2'
            
            if os.path.exists(model_path):
                print(f"Model already exists at: {model_path}")
                return str(model_path)
            
            print("Downloading SentenceTransformer model...")
            print("This may take a few minutes on first run...")
            
            # Download and save model locally
            model = SentenceTransformer('all-MiniLM-L6-v2')
            model.save(str(model_path))
            
            print(f"Model successfully downloaded to: {model_path}")
            return str(model_path)
            
        except ImportError:
            print("SentenceTransformers not installed. Install with:")
            print("pip install sentence-transformers")
            return None
        except Exception as e:
            print(f"Error downloading model: {e}")
            return None

    def setup_offline_environment(self):
        """Setup environment variables for offline use"""
        os.environ['TRANSFORMERS_OFFLINE'] = '1'
        os.environ['HF_DATASETS_OFFLINE'] = '1'
        os.environ['HF_HUB_OFFLINE'] = '1'
        print("Environment configured for offline use")

    def get_local_model(self):
        """Load SentenceTransformer model locally"""
        if self.model is None and SENTENCE_TRANSFORMERS_AVAILABLE:
            # Try different local paths where the model might be stored
            local_paths = [FEMB_MODEL_PATH]
            
            model_loaded = False
            for path in local_paths:
                if os.path.exists(path):
                    try:
                        print(f"Loading model from local path: {path}")
                        self.model = SentenceTransformer(path, device=EMB_DEVICE)
                        model_loaded = True
                        break
                    except Exception as e:
                        print(f"Failed to load from {path}: {e}")
                        continue
                else:
                    self.download_model_locally()
                    self.model = SentenceTransformer(path, device=EMB_DEVICE)
            if not model_loaded:
                # Try to load with offline mode
                try:
                    print("Attempting to load model in offline mode...")
                    os.environ['TRANSFORMERS_OFFLINE'] = '1'
                    os.environ['HF_DATASETS_OFFLINE'] = '1'
                    self.model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
                except Exception as e:
                    print(f"Failed to load model in offline mode: {e}")
                    # Fallback to simple averaging embeddings
                    print("Using fallback embedding method...")
                    self.model = None

    def simple_embedding(self,text, embedding_dim=384):
        """Fallback embedding method using simple text features"""
        import numpy as np
        
        # Simple feature extraction
        features = []
        
        # Length features
        features.append(len(text) / 1000.0)  # Normalized length
        features.append(len(text.split()) / 100.0)  # Normalized word count
        
        # Character frequency features
        char_counts = {}
        for char in text.lower():
            char_counts[char] = char_counts.get(char, 0) + 1
        
        # Top 10 most common characters (normalized)
        sorted_chars = sorted(char_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        for _, count in sorted_chars:
            features.append(count / len(text))
        
        # Pad or truncate to desired dimension
        while len(features) < embedding_dim:
            features.append(0.0)
        
        return np.array(features[:embedding_dim], dtype=np.float32)

    def generate_embeddings(self,texts):
        """Generate embeddings using local model or fallback method"""
        try:
            sentence=texts[0]
            print("aws embedding")
            embedding_model="amazon.titan-embed-text-v1"
            aws_region="us-east-1"
            # Prepare the request body based on the embedding model
            if 'titan-embed' in embedding_model:
                body = {
                    "inputText": sentence
                }
                bedrock_client = boto3.client(
                    service_name='bedrock-runtime',
                    region_name=aws_region
                )
            # Make the API call
            response = bedrock_client.invoke_model(
                modelId=embedding_model,
                body=json.dumps(body),
                contentType='application/json',
                accept='application/json'
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            # Extract embedding based on model
            if 'titan-embed' in embedding_model:
                title_embedding = response_body.get('embedding', [])
            # title_embedding=title_embedding.tolist()
            return title_embedding
        
        except Exception as e:
            print("local embedding" ,str(e))
            # Fallback to simple embeddings
            embeddings = []
            # for text in texts:
            #     embeddings.append(self.simple_embedding(text))

            title_embedding = title_embedding=self.model.encode(sentence)
            target_length = 1536
            title_embedding=title_embedding.tolist()

            # Calculate how many zeros you need to add
            missing = target_length - len(title_embedding)
            if missing > 0:
                title_embedding.extend([0] * missing)

            return title_embedding

    def setup(self):
        """Main setup function"""
        model_path = EMB_MODEL_PATH
        if not os.path.exists(model_path):
            print("Model not found. Run download_model_locally() first.")
            # Download model
            model_path = self.download_model_locally()
            if not model_path:
                print("Failed to download model")
                return
            else:
                # Setup offline environment
                self.setup_offline_environment()
                # self.get_local_model()

    
    def embed_query(self, text):
        try:
            embedding_model="amazon.titan-embed-text-v1"
            aws_region="us-east-1"
            # Prepare the request body based on the embedding model
            if 'titan-embed' in embedding_model:
                body = {
                    "inputText": text
                }
                bedrock_client = boto3.client(
                    service_name='bedrock-runtime',
                    region_name=aws_region
                )
            # Make the API call
            response = bedrock_client.invoke_model(
                modelId=embedding_model,
                body=json.dumps(body),
                contentType='application/json',
                accept='application/json'
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            # Extract embedding based on model
            if 'titan-embed' in embedding_model:
                title_embedding = response_body.get('embedding', [])
                print("query embedding len0 ",len(title_embedding))

                return title_embedding
            
            else:
                raise 
        except Exception as e:
            print("Error embedding query go with local ",str(e) )
            title_embedding=self.model.encode(text).tolist()
            target_length = 1536

            # Calculate how many zeros you need to add
            missing = target_length - len(title_embedding)
            if missing > 0:
                title_embedding.extend([0] * missing)
            print("query embedding len1 ",len(title_embedding))

            return title_embedding

    
    def embed_documents(self, texts):
        """Optional method for batch processing"""
        return [self.model.encode(text).tolist() for text in texts]



# class LocalEmbModelSearch:
#     def __init__(self, model_name='all-MiniLM-L6-v2'):
#         self.model = SentenceTransformer(model_name)
    
#     def embed_query(self, text):
#         try:
#             embedding_model="amazon.titan-embed-text-v1"
#             aws_region="us-east-1"
#             # Prepare the request body based on the embedding model
#             if 'titan-embed' in embedding_model:
#                 body = {
#                     "inputText": text
#                 }
#                 bedrock_client = boto3.client(
#                     service_name='bedrock-runtime',
#                     region_name=aws_region
#                 )
#             # Make the API call
#             response = bedrock_client.invoke_model(
#                 modelId=embedding_model,
#                 body=json.dumps(body),
#                 contentType='application/json',
#                 accept='application/json'
#             )
            
#             # Parse response
#             response_body = json.loads(response['body'].read())
            
#             # Extract embedding based on model
#             if 'titan-embed' in embedding_model:
#                 title_embedding = response_body.get('embedding', [])
#                 return title_embedding
#             else:
#                 raise 
#         except Exception as e:
#             print("Error embedding query")
#             return self.model.encode(text).tolist()
    
#     def embed_documents(self, texts):
#         """Optional method for batch processing"""
#         return [self.model.encode(text).tolist() for text in texts]
