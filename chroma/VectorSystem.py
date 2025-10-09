import pymupdf4llm
import boto3
import chromadb
import json
import pandas as pd
from typing import List, Dict, Any, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
import hashlib
import os
from pathlib import Path
from datetime import datetime
from werkzeug.utils import secure_filename
import csv
from datetime import datetime
import uuid

class PDFVectorSystem:

    """
    A comprehensive system for PDF processing, embedding generation, and vector search.
    """

    def __init__(self, 
                 aws_region: str = 'us-east-1',
                 embedding_model: str = 'amazon.titan-embed-text-v1',
                 chroma_path: str = './vol/chroma_db',
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200,collection_name=None):
        """
        Initialize the PDF Vector System.
        Args:
            aws_region: AWS region for Bedrock
            embedding_model: Bedrock embedding model ID
            chroma_path: Path to ChromaDB storage
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.aws_region = aws_region
        self.embedding_model = embedding_model
        self.chroma_path = chroma_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize AWS Bedrock client
        self.bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            region_name=self.aws_region
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=self.chroma_path)
        if collection_name:
            self.collection_name = collection_name
        else:
            collection_name=str(datetime.now().strftime("%Y%m%d%H%M%S"))
        # Create or get collection
        try:
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            print("exception create collection",str(e))
            try:
                self.collection = self.chroma_client.get_collection(name=self.collection_name)
            except Exception as e:
                print("exception get collection",str(e))

    def read_pdf_with_chunks(self, pdf_path: str) -> Tuple[List[str], List[Dict[str, Any]]]:
        """
        Read PDF using pymupdf4llm and return text chunks with metadata.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Tuple of (text_chunks, metadata_list)
        """
        try:
            # Get PDF name without extension
            pdf_name = Path(pdf_path).stem
            
            # Read PDF using pymupdf4llm
            md_text = pymupdf4llm.to_markdown(pdf_path, page_chunks=True)
            
            text_chunks = []
            metadata_list = []
            
            # Process each page
            for page_num, page_data in enumerate(md_text):
                page_text = page_data.get('text', '')
                page_id = page_data.get('page', page_num)
                
                if page_text.strip():  # Only process non-empty pages
                    # Split page text into chunks
                    page_chunks = self.text_splitter.split_text(page_text)
                    
                    for chunk_idx, chunk in enumerate(page_chunks):
                        if chunk.strip():  # Only add non-empty chunks
                            # Generate unique chunk ID
                            chunk_id = self._generate_chunk_id(pdf_name, page_id, chunk_idx)
                            
                            text_chunks.append(chunk)
                            metadata_list.append({
                                'pdf_name': pdf_name,
                                'pdf_path':pdf_path,
                                'page_id': page_id,
                                'chunk_id': chunk_id,
                                'chunk_index': chunk_idx,
                                'text': chunk
                            })
            
            print(f"Successfully processed {pdf_path}: {len(text_chunks)} chunks from {page_num + 1} pages")
            return text_chunks, metadata_list
            
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {str(e)}")
            return [], []

    def read_csv_with_chunks(self, csv_path: str) -> Tuple[List[str], List[Dict[str, Any]]]:
        """
        Read CSV file (with question/answer columns) and return text chunks with metadata.

        Args:
            csv_path: Path to the CSV file

        Returns:
            Tuple of (text_chunks, metadata_list)
        """
        try:
            # Get CSV name without extension
            csv_name = Path(csv_path).stem
            with open(csv_path, "r", encoding="utf-8") as f:
                sample = f.read(2048)  # read a small portion for detection
                dialect = csv.Sniffer().sniff(sample)
                delimiter = dialect.delimiter
            # Read CSV file
            df = pd.read_csv(csv_path,delimiter=delimiter)

            text_chunks = []
            metadata_list = []

            # Loop through each row (question = text, answer = metadata)
            for idx, row in df.iterrows():
                question = str(row.get("question", "")).strip()
                answer = str(row.get("answer", "")).strip()

                if question:  # Only process non-empty questions
                    # Treat the full question as one chunk
                    chunk_id = f"{csv_name}_{idx}"

                    text_chunks.append(question)
                    metadata_list.append({
                        "pdf_name": csv_name,
                        'pdf_path':csv_path,
                        "page_id": idx,
                        "chunk_id": chunk_id,
                        "chunk_index": idx,
                        "text": question,
                        "answer": answer  # Store answer in metadata
                    })

            print(f"Successfully processed {csv_path}: {len(text_chunks)} rows as chunks")
            return text_chunks, metadata_list

        except Exception as e:
            print(f"Error processing {csv_path}: {e}")
            return [], []

    def _generate_chunk_id(self, pdf_name: str, page_id: int, chunk_idx: int) -> str:
        """Generate a unique chunk ID."""
        base_string = f"{pdf_name}_{page_id}_{chunk_idx}"
        return hashlib.md5(base_string.encode()).hexdigest()[:12]

    def convert_to_embeddings(self, text_chunks: List[str],pdf_name="") -> List[List[float]]:
        """
        Convert text chunks to embeddings using AWS Bedrock.
        
        Args:
            text_chunks: List of text chunks
            
        Returns:
            List of embedding vectors
        """
        embeddings = []
        
        for i, chunk in enumerate(text_chunks):
            try:
                # Prepare the request body based on the embedding model
                if 'titan-embed' in self.embedding_model:
                    body = {
                        "inputText": chunk
                    }
                elif 'cohere' in self.embedding_model:
                    body = {
                        "texts": [chunk],
                        "input_type": "search_document"
                    }
                else:
                    body = {"inputText": chunk}  # Default format
                
                # Make the API call
                response = self.bedrock_client.invoke_model(
                    modelId=self.embedding_model,
                    body=json.dumps(body),
                    contentType='application/json',
                    accept='application/json'
                )
                
                # Parse response
                response_body = json.loads(response['body'].read())
                
                # Extract embedding based on model
                if 'titan-embed' in self.embedding_model:
                    embedding = response_body.get('embedding', [])
                elif 'cohere' in self.embedding_model:
                    embedding = response_body.get('embeddings', [[]])[0]
                else:
                    embedding = response_body.get('embedding', [])
                
                if embedding:
                    embeddings.append(embedding)
                else:
                    print(f"Warning: Empty embedding for chunk {i}")
                    
            except Exception as e:
                print(f"{pdf_name} ,Error generating embedding for chunk {i}: {str(e)}")
                # Add a zero vector as placeholder
                embeddings.append([0.0] * 1536)  # Adjust dimension as needed

        print(f"Generated {len(embeddings)} embeddings")
        return embeddings

    def add_vectors_to_chromadb(self, 
                               embeddings: List[List[float]], 
                               metadata_list: List[Dict[str, Any]],
                               update_mode: str = 'skip') -> bool:
        
        """
        Add vectors with metadata to ChromaDB.
        
        Args:
            embeddings: List of embedding vectors
            metadata_list: List of metadata dictionaries
            update_mode: 'skip', 'update', or 'error'
                - 'skip': Skip existing IDs, add only new ones
                - 'update': Update existing IDs with new data
                - 'error': Raise error if ID exists (default ChromaDB behavior)
            
        Returns:
            Success status
        """
        try:
            if len(embeddings) != len(metadata_list):
                print("Error: Embeddings and metadata lists must have the same length")
                return False
            
            # Prepare data for ChromaDB
            ids = [metadata['chunk_id'] for metadata in metadata_list]
            documents = [metadata['text'] for metadata in metadata_list]
            
            # Prepare metadata (remove 'text' as it's stored separately as document)
            chroma_metadata = []
            for metadata in metadata_list:
                chroma_meta = {
                    'pdf_name': metadata['pdf_name'],
                    'pdf_path':metadata["pdf_path"],
                    'page_id': str(metadata['page_id']),  # ChromaDB requires string values
                    'chunk_id': metadata['chunk_id'],
                    'chunk_index': str(metadata['chunk_index']),
                    'answer':metadata.get("answer","")
                }
                chroma_metadata.append(chroma_meta)
            
            if update_mode == 'skip':
                # Check for existing IDs and filter out duplicates
                new_embeddings, new_documents, new_metadata, new_ids = self._filter_existing_ids(
                    embeddings, documents, chroma_metadata, ids
                )
                
                if new_ids:
                    self.collection.add(
                        embeddings=new_embeddings,
                        documents=new_documents,
                        metadatas=new_metadata,
                        ids=new_ids
                    )
                    print(f"Added {len(new_ids)} new vectors to ChromaDB (skipped {len(ids) - len(new_ids)} existing)")
                else:
                    print("No new vectors to add - all IDs already exist")
                
            elif update_mode == 'update':
                # Use upsert functionality - add new or update existing
                self.collection.upsert(
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=chroma_metadata,
                    ids=ids
                )
                print(f"Upserted {len(embeddings)} vectors to ChromaDB")
                
            else:  # update_mode == 'error'
                # Default ChromaDB behavior - will raise error if ID exists
                self.collection.add(
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=chroma_metadata,
                    ids=ids
                )
                print(f"Added {len(embeddings)} vectors to ChromaDB")
            
            return True
            
        except Exception as e:
            print(f"Error adding vectors to ChromaDB: {str(e)}")
            return False

    def _filter_existing_ids(self, embeddings: List[List[float]], 
                           documents: List[str], 
                           metadata: List[Dict], 
                           ids: List[str]) -> Tuple[List[List[float]], List[str], List[Dict], List[str]]:
        """Filter out existing IDs to avoid duplicates."""
        try:
            # Try to get existing documents with these IDs
            existing_ids = set()
            try:
                result = self.collection.get(ids=ids, include=[])
                existing_ids = set(result['ids'])
            except Exception:
                # If get fails, assume no existing IDs
                pass
            
            # Filter out existing IDs
            new_embeddings = []
            new_documents = []
            new_metadata = []
            new_ids = []
            
            for i, id_val in enumerate(ids):
                if id_val not in existing_ids:
                    new_embeddings.append(embeddings[i])
                    new_documents.append(documents[i])
                    new_metadata.append(metadata[i])
                    new_ids.append(id_val)
            
            return new_embeddings, new_documents, new_metadata, new_ids
            
        except Exception as e:
            print(f"Error filtering existing IDs: {str(e)}")
            # Return all data if filtering fails
            return embeddings, documents, metadata, ids

    def retrieve_similar_text(self, 
                             query: str, 
                             n_results: int = 5,
                             pdf_filter: str = None) -> Dict[str, Any]:
        """
        Retrieve similar text chunks based on query.
        
        Args:
            query: Query text
            n_results: Number of results to return
            pdf_filter: Optional PDF name to filter results
            
        Returns:
            Dictionary with similar chunks and their metadata
        """
        try:
            # Generate embedding for the query
            query_embedding = self.convert_to_embeddings([query])[0]
            print("embedding length",len(query_embedding))
            # Prepare where clause if PDF filter is specified
            where_clause = None
            if pdf_filter:
                where_clause = {"pdf_name": pdf_filter}
            
            # Query the collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_clause,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Format results
            formatted_results = {
                'query': query,
                'n_results': len(results['documents'][0]) if results['documents'] else 0,
                'results': []
            }
            
            if results['documents']:
                for i in range(len(results['documents'][0])):
                    result = {
                        'text': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'similarity_score': 1 - results['distances'][0][i],  # Convert distance to similarity
                        'distance': results['distances'][0][i]
                    }
                    formatted_results['results'].append(result)
            
            print(f"Found {formatted_results['n_results']} similar chunks")
            return formatted_results
            
        except Exception as e:
            print(f"Error retrieving similar text: {str(e)}")
            return {'query': query, 'n_results': 0, 'results': []}

    def check_pdf_exists(self, pdf_name: str) -> Dict[str, Any]:
        """
        Check if a PDF has already been processed.
        
        Args:
            pdf_name: Name of the PDF (without extension)
            
        Returns:
            Dictionary with existence info and chunk count
        """
        try:
            result = self.collection.get(
                where={"pdf_name": pdf_name},
                include=['metadatas']
            )
            
            return {
                'exists': len(result['ids']) > 0,
                'chunk_count': len(result['ids']),
                'chunk_ids': result['ids']
            }
        except Exception as e:
            print(f"Error checking PDF existence: {str(e)}")
            return {'exists': False, 'chunk_count': 0, 'chunk_ids': []}

    def remove_pdf_from_db(self, pdf_name: str) -> bool:
        """
        Remove all chunks of a specific PDF from the database.
        
        Args:
            pdf_name: Name of the PDF to remove
            
        Returns:
            Success status
        """
        try:
            # Get all IDs for this PDF
            result = self.collection.get(
                where={"pdf_name": pdf_name},
                include=[]
            )
            
            if result['ids']:
                self.collection.delete(ids=result['ids'])
                print(f"Removed {len(result['ids'])} chunks for PDF: {pdf_name}")
                return True
            else:
                print(f"No chunks found for PDF: {pdf_name}")
                return True
                
        except Exception as e:
            print(f"Error removing PDF from database: {str(e)}")
            return False

    def process_pdf_pipeline(self, pdf_path: str, update_mode: str = 'skip',ext="") -> bool:
        """
        Complete pipeline to process a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            update_mode: 'skip', 'update', or 'error'
                - 'skip': Skip if PDF already exists, add only new chunks
                - 'update': Update/replace existing PDF data
                - 'error': Raise error if chunks exist
        Returns:
            Success status
        """
        print(f"Starting PDF processing pipeline for: {pdf_path}")
        
        # Get PDF name
        pdf_name = Path(pdf_path).stem
        # Check if PDF already exists
        pdf_status = self.check_pdf_exists(pdf_name)
        if pdf_status['exists']:
            if update_mode == 'skip':
                print(f"PDF '{pdf_name}' already exists with {pdf_status['chunk_count']} chunks. Skipping.")
                return True
            elif update_mode == 'update':
                print(f"PDF '{pdf_name}' exists. Removing existing chunks for update.")
                self.remove_pdf_from_db(pdf_name)
        
        #---------------PDF------------------

        if ext=="pdf":
        # Step 1: Read PDF and create chunks
            text_chunks, metadata_list = self.read_pdf_with_chunks(pdf_path)
            if not text_chunks:
                print("Failed to extract text chunks from PDF")
                return False
        elif ext=="csv":
            text_chunks, metadata_list = self.read_csv_with_chunks(pdf_path)
            if not text_chunks:
                print("Failed to extract text chunks from csv")
                return False
        # Step 2: Generate embeddings
        embeddings = self.convert_to_embeddings(text_chunks,pdf_name)
        if len(embeddings) != len(text_chunks):
            print("Failed to generate embeddings for all chunks")
            return False
        
        # Step 3: Add to ChromaDB
        success = self.add_vectors_to_chromadb(embeddings, metadata_list, update_mode)
        if success:
            print("PDF processing pipeline completed successfully!")
        
        return success

    def generate_unique_id(self):
        # Date + Time with milliseconds
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # trim to milliseconds
        # Short random UUID
        random_part = uuid.uuid4().hex  
        # Combine them
        return f"{timestamp}_{random_part}"

    def add_QA(self,question,answer) -> bool:        
        text_chunks=[]
        metadata_list=[]
        #---------------PDF------------------
        text_chunks.append(question)
        unique_id = self.generate_unique_id()

        metadata_list.append({
            "pdf_name": "added with api",
            'pdf_path':"",
            "page_id": "",
            "chunk_id": unique_id,
            "chunk_index": unique_id,
            "text": question,
            "answer": answer  # Store answer in metadata
        })

        # Step 2: Generate embeddings
        embeddings = self.convert_to_embeddings(text_chunks,"QA--"+question)
        if len(embeddings) != len(text_chunks):
            print("Failed to generate embeddings for all chunks")
            return False
        
        # Step 3: Add to ChromaDB
        success = self.add_vectors_to_chromadb(embeddings, metadata_list, "skip")
        if success:
            print("PDF processing pipeline completed successfully!")
        
        return success

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the ChromaDB collection."""
        try:
            count = self.collection.count()
            
            # Get unique PDF names
            all_metadata = self.collection.get(include=['metadatas'])
            pdf_names = set()
            if all_metadata['metadatas']:
                pdf_names = {meta.get('pdf_name') for meta in all_metadata['metadatas']}
            
            return {
                'total_chunks': count,
                'unique_pdfs': len(pdf_names),
                'pdf_names': list(pdf_names),
                'collection_name': self.collection_name,
                'chroma_path': self.chroma_path
            }
        except Exception as e:
            print(f"Error getting collection stats: {str(e)}")
            return {}

    def list_pages_in_file(self, file_name: str) -> Dict[str, Any]:
        """
        List all pages available in a specific file.
        
        Args:
            file_name: Name of the PDF file
            
        Returns:
            Dictionary with page information
        """
        try:
            clean_file_name = file_name.replace('.pdf', '').replace('.PDF', '')
            
            # Get all chunks for this file
            results = self.collection.get(
                where={"pdf_name": clean_file_name},
                include=['metadatas']
            )
            
            if not results['metadatas']:
                return {
                    'file_name': clean_file_name,
                    'exists': False,
                    'total_pages': 0,
                    'pages': [],
                    'total_chunks': 0
                }
            
            # Extract page information
            page_info = {}
            for metadata in results['metadatas']:
                page_id = int(metadata.get('page_id', 0))
                if page_id not in page_info:
                    page_info[page_id] = 0
                page_info[page_id] += 1
            
            # Sort pages and create summary
            sorted_pages = sorted(page_info.keys())
            page_details = []
            for page_id in sorted_pages:
                page_details.append({
                    'page_id': page_id,
                    'chunk_count': page_info[page_id]
                })
            
            return {
                'file_name': clean_file_name,
                'exists': True,
                'total_pages': len(sorted_pages),
                'pages': page_details,
                'total_chunks': len(results['metadatas']),
                'page_range': f"{min(sorted_pages)}-{max(sorted_pages)}" if sorted_pages else "0-0"
            }
            
        except Exception as e:
            print(f"Error listing pages in file: {str(e)}")
            return {
                'file_name': file_name,
                'exists': False,
                'total_pages': 0,
                'pages': [],
                'total_chunks': 0
            }

    def find_chunks_by_file_and_page(self, 
                                    file_name: str, 
                                    page_id: int = None,
                                    include_text: bool = True) -> Dict[str, Any]:
        """
        Find chunks by file name and optionally by page number.
        
        Args:
            file_name: Name of the PDF file (with or without .pdf extension)
            page_id: Specific page number (optional, if None returns all pages)
            include_text: Whether to include full text content in results
            
        Returns:
            Dictionary with matching chunks and their metadata
        """
        try:
            # Clean file name (remove .pdf extension if present)
            clean_file_name = file_name.replace('.pdf', '').replace('.PDF', '')
            # Determine what to include in results
            include_fields = ['metadatas']
            if include_text:
                include_fields.append('documents')
            
            # Step 1: Query by filename
            results = self.collection.get(
                where={"pdf_name": {"$eq": clean_file_name}},
                include=include_fields
            )
            # Step 2: If page_id is requested, filter locally
            if page_id is not None:
                filtered = {
                    "ids": [],
                    "metadatas": [],
                    "documents": [],
                }
                for i, metadata in enumerate(results["metadatas"]):
                    if str(metadata.get("page_id")) == str(page_id):
                        filtered["ids"].append(results["ids"][i])
                        filtered["metadatas"].append(metadata)
                        if "documents" in results:
                            filtered["documents"].append(results["documents"][i])
                results = filtered

            

            
            # Format results
            formatted_results = {
                'file_name': clean_file_name,
                'page_id': page_id,
                'total_chunks': len(results['ids']) if results['ids'] else 0,
                'chunks': results["documents"]
            }
            
            return formatted_results
            
        except Exception as e:
            print(f"Error finding chunks by file and page: {str(e)}")
            return {
                'file_name': file_name,
                'page_id': page_id,
                'total_chunks': 0,
                'chunks': []
            }

    def show_all_chunks(self, 
                        pdf_filter: str = None,
                        page_filter: int = None,
                        limit: int = None,
                        include_text: bool = True,
                        text_preview_length: int = 200,
                        sort_by: str = 'pdf_page_chunk') -> Dict[str, Any]:
            """
            Show all chunks in the database with optional filtering.
            
            Args:
                pdf_filter: Filter by specific PDF name (optional)
                page_filter: Filter by specific page (requires pdf_filter)
                limit: Maximum number of chunks to return (optional)
                include_text: Whether to include full text content
                text_preview_length: Length of text preview (if include_text=True)
                sort_by: Sorting method - 'pdf_page_chunk', 'pdf_only', 'chunk_id', or 'none'
                
            Returns:
                Dictionary with all matching chunks and summary statistics
            """
            try:
                # Build where clause for filtering
                where_clause = None
                if pdf_filter:
                    clean_pdf_name = pdf_filter.replace('.pdf', '').replace('.PDF', '')
                    where_clause = {"pdf_name": clean_pdf_name}
                    
                    if page_filter is not None:
                        where_clause["page_id"] = str(page_filter)
                elif page_filter is not None:
                    print("Warning: page_filter ignored because pdf_filter is not specified")
                
                # Determine what to include in results
                include_fields = ['metadatas']
                if include_text:
                    include_fields.append('documents')
                
                # Get all matching chunks
                results = self.collection.get(
                    where=where_clause,
                    include=include_fields,
                    limit=limit
                )
                
                # Format results
                chunks_data = []
                if results['ids']:
                    for i in range(len(results['ids'])):
                        chunk_info = {
                            'chunk_id': results['ids'][i],
                            'pdf_name': results['metadatas'][i].get('pdf_name', 'unknown'),
                            'page_id': int(results['metadatas'][i].get('page_id', 0)),
                            'chunk_index': int(results['metadatas'][i].get('chunk_index', 0)),
                            'metadata': results['metadatas'][i]
                        }
                        
                        if include_text and 'documents' in results:
                            full_text = results['documents'][i]
                            chunk_info['text'] = full_text
                            chunk_info['text_preview'] = full_text[:text_preview_length] + ('...' if len(full_text) > text_preview_length else '')
                            chunk_info['word_count'] = len(full_text.split())
                            chunk_info['char_count'] = len(full_text)
                        
                        chunks_data.append(chunk_info)
                
                # Sort chunks based on sort_by parameter
                if sort_by == 'pdf_page_chunk':
                    chunks_data.sort(key=lambda x: (x['pdf_name'], x['page_id'], x['chunk_index']))
                elif sort_by == 'pdf_only':
                    chunks_data.sort(key=lambda x: x['pdf_name'])
                elif sort_by == 'chunk_id':
                    chunks_data.sort(key=lambda x: x['chunk_id'])
                # 'none' - no sorting
                
                # Generate summary statistics
                pdf_stats = {}
                page_stats = {}
                total_words = 0
                total_chars = 0
                
                for chunk in chunks_data:
                    pdf_name = chunk['pdf_name']
                    page_id = chunk['page_id']
                    
                    # PDF statistics
                    if pdf_name not in pdf_stats:
                        pdf_stats[pdf_name] = {'chunk_count': 0, 'pages': set()}
                    pdf_stats[pdf_name]['chunk_count'] += 1
                    pdf_stats[pdf_name]['pages'].add(page_id)
                    
                    # Page statistics
                    page_key = f"{pdf_name}::{page_id}"
                    if page_key not in page_stats:
                        page_stats[page_key] = 0
                    page_stats[page_key] += 1
                    
                    # Text statistics
                    if include_text:
                        total_words += chunk.get('word_count', 0)
                        total_chars += chunk.get('char_count', 0)
                
                # Convert PDF stats to serializable format
                pdf_summary = {}
                for pdf_name, stats in pdf_stats.items():
                    pdf_summary[pdf_name] = {
                        'chunk_count': stats['chunk_count'],
                        'page_count': len(stats['pages']),
                        'pages': sorted(list(stats['pages']))
                    }
                
                # Create filter description
                filter_desc = ""
                if pdf_filter:
                    filter_desc += f"PDF: '{pdf_filter}'"
                    if page_filter is not None:
                        filter_desc += f", Page: {page_filter}"
                else:
                    filter_desc = "All chunks"
                
                result = {
                    'filter_description': filter_desc,
                    'total_chunks': len(chunks_data),
                    'chunks': chunks_data,
                    'summary': {
                        'unique_pdfs': len(pdf_stats),
                        'unique_pages': len(page_stats),
                        'pdf_breakdown': pdf_summary,
                        'sorting': sort_by,
                        'limited_results': limit is not None and len(chunks_data) == limit
                    }
                }
                
                if include_text:
                    result['summary']['total_words'] = total_words
                    result['summary']['total_characters'] = total_chars
                    result['summary']['avg_words_per_chunk'] = total_words / len(chunks_data) if chunks_data else 0
                
                print(f"Retrieved {len(chunks_data)} chunks ({filter_desc})")
                if limit and len(chunks_data) == limit:
                    print(f"Note: Results limited to {limit} chunks")
                
                return result
                
            except Exception as e:
                print(f"Error showing all chunks: {str(e)}")
                return {
                    'filter_description': 'Error',
                    'total_chunks': 0,
                    'chunks': [],
                    'summary': {}
                }

    #-------------------- function to add document to kb , add QA , get_context
    
    def add_document(self,uploaded_file,documents_folder):

        uploaded_file_name=uploaded_file.filename
        print("file name",uploaded_file_name)
        if uploaded_file is not None:
            file_name=str.split(uploaded_file_name,"/")[-1]

            file_ext=str.split(file_name,".")[-1].lower()
            print(" recieved file name",file_name,file_ext)
            document_path=os.path.join(documents_folder, file_name)

            try:
                filename = secure_filename(uploaded_file_name)
                uploaded_file.save(document_path)

            except Exception as e:
                with open(document_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                print("error method 2 save file" , str(e))
                
            try:
                if file_ext=="pdf":
                    success = self.process_pdf_pipeline(document_path, update_mode='skip',ext="pdf")
                elif file_ext=='csv':
                    success = self.process_pdf_pipeline(document_path, update_mode='skip',ext="csv")
                return "success"
            except:
                return "Error add to database"

    def get_context_text(self,query_text,k=10,n=2):
        results = self.retrieve_similar_text(query_text, n_results=k)
        try:
            return str(results),results
        except Exception as e:
            print("Exception query function",str(e))
            return "Error to find context"
        
    def get_context_QA(self,query_text,k=10,n=2):
        results = self.retrieve_similar_text(query_text, n_results=k)
        try:
            return results
        except Exception as e:
            print("Exception query function",str(e))
            return "Error to find context"
        





































# # Example usage
# if __name__ == "__main__":
#     # Initialize the system

#     pdf_system = PDFVectorSystem(
#         aws_region='us-east-1',  # Change to your AWS region
#         embedding_model='amazon.titan-embed-text-v1',  # Change to your preferred model
#         chunk_size=1200,
#         chunk_overlap=200
#     )
#     # Process a PDF file with different modes
#     pdf_path = "test_pdf1.pdf"  # Replace with your PDF path
    
#     if os.path.exists(pdf_path):
#         # Mode 1: Skip if exists (default - safe for re-runs)
#         success = pdf_system.process_pdf_pipeline(pdf_path, update_mode='skip')
        
#         # Mode 2: Update/replace existing PDF
#         # success = pdf_system.process_pdf_pipeline(pdf_path, update_mode='update')
        
#         # Mode 3: Error if exists (strict mode)
#         # success = pdf_system.process_pdf_pipeline(pdf_path, update_mode='error')
        
#         if success:
#             # Query for similar text
#             query = "how install the process"
#             # results = pdf_system.retrieve_similar_text(query, n_results=3)
            
#             # print(f"\nQuery: {results['query']}")
#             # print(f"Found {results['n_results']} results:")
            
#             # for i, result in enumerate(results['results'], 1):
#             #     print(f"\n--- Result {i} ---")
#             #     print(f"PDF: {result['metadata']['pdf_name']}")
#             #     print(f"Page: {result['metadata']['page_id']}")
#             #     print(f"Similarity: {result['similarity_score']:.3f}")
#             #     print(f"Text: {result['text'][:200]}...")
            
#             # Get collection statistics

#             # res=pdf_system.show_all_chunks()
#             # print(res)
#             # stats = pdf_system.get_collection_stats()
#             # print(f"\nCollection stats: {stats}")
            
#             pdf_name = Path(pdf_path).stem
#             # pdf_status = pdf_system.check_pdf_exists(pdf_name)
#             # print(f"\nPDF '{pdf_name}' status: {pdf_status}"
#             pages_info = pdf_system.list_pages_in_file(pdf_name)
#             # print(f"Pages info: {pages_info}")
            
#             if pages_info['exists'] and pages_info['pages']:
#                 first_page = pages_info['pages'][25]['page_id']
#                 # print("id",first_page,pdf_name)
#                 print(f"\nChunks on page {first_page}:")

#                 page_chunks = pdf_system.find_chunks_by_file_and_page(pdf_name, first_page)
#                 # print(page_chunks)
#                 for chunk in page_chunks['chunks']:
#                     print(f"  - Chunk : {chunk}")


#     else:
#         print(f"PDF file not found: {pdf_path}")
#         print("Please update the pdf_path variable with a valid PDF file path.")