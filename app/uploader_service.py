from dotenv import load_dotenv
import os
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.word_document import Docx2txtLoader
from langchain_community.document_loaders.powerpoint import UnstructuredPowerPointLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.image import UnstructuredImageLoader
import qdrant_client

load_dotenv()

class UploaderService:
    def __init__(self,_document_id):
        self.document_id = _document_id
        self.url = os.getenv("QDRANT_HOST_STRING")
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=100
        )
    async def upload_image(self,path) -> bool:
            try:
                loader = UnstructuredImageLoader(path)
                print("-----------------Uploading----------------")
                data = loader.load()
                Qdrant.from_documents(
                        data,
                        OpenAIEmbeddings(),
                        url=self.url,
                        collection_name=self.document_id,
                        force_recreate=True,
                        )
                print("-----------------Completed----------------")
                return True
            except Exception as exception:
                print(exception)
                return False
    async def upload_document(self,path,doc_type) -> bool:
        try:
            pages = None
            if(doc_type == 'pdf'):
                loader = PyPDFLoader(path)
            if(doc_type == 'doc'):
                loader = Docx2txtLoader(path)
            if(doc_type == 'ppt'):
                loader = UnstructuredPowerPointLoader(path)
            if(doc_type == 'exl'):
                loader = UnstructuredExcelLoader(path)
            print("-----------------Generating----------------")
            pages = loader.load_and_split(text_splitter=self.splitter)
            if(len(pages)==0):
                    pages = loader.load()
            Qdrant.from_documents(
                    pages,
                    OpenAIEmbeddings(),
                    url=self.url,
                    collection_name=self.document_id,
                    force_recreate=True,
                    )
            print("-----------------Completed----------------")
            return True
        except Exception as exception:
            print(exception)
            return False
    def get_relevant_documents(self,query) -> str:
        client = qdrant_client.QdrantClient(
            url=self.url,
        )
        qdrant = Qdrant(
            client=client,
            collection_name=self.document_id,
            embeddings=OpenAIEmbeddings(),
            )
        docs = qdrant.similarity_search(query=query,k=5)
        print(f"DOCS RETRIEVED: {len(docs)}")
        input_text = ""
        for doc in docs:
            input_text += str(doc.metadata["page"]) + ":"+doc.page_content+"\n"
        return input_text
    
    def delete_document(self) -> bool:
        try:
            client = qdrant_client.QdrantClient(
                url=self.url,
            )
            client.delete_collection(collection_name=self.document_id)
            return True
        except Exception as exception:
            print(exception)
            return False