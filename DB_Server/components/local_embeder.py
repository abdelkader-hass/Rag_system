
from .static_var import EMB_MODEL_PATH,FEMB_MODEL_PATH,EMB_DEVICE
import os
import numpy as np



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
        model = self.model
        
        if model is not None:
            try:
                # print("Generating model embeddings...")
                return model.encode(texts, show_progress_bar=False)
            except Exception as e:
                print(f"Error generating embeddings with model: {e}")
                print("Using fallback embedding method...")
        
        # Fallback to simple embeddings
        # print("Generating simple embeddings...")
        embeddings = []
        for text in texts:
            embeddings.append(self.simple_embedding(text))
        
        return np.array(embeddings)

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
        """Required method for neo4j-graphrag compatibility"""
        return self.model.encode(text).tolist()
    
    def embed_documents(self, texts):
        """Optional method for batch processing"""
        return [self.model.encode(text).tolist() for text in texts]



class LocalEmbModelSearch:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    
    def embed_query(self, text):
        """Required method for neo4j-graphrag compatibility"""
        return self.model.encode(text).tolist()
    
    def embed_documents(self, texts):
        """Optional method for batch processing"""
        return [self.model.encode(text).tolist() for text in texts]
