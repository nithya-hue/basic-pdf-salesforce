
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import os
import fitz
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

allowed_origins = [ "*" ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  
    allow_credentials=True,         
    allow_methods=["*"],            
    allow_headers=["*"])



class PDF(BaseModel):
    filename: str

def extract_text_pymupdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            extracted = page.get_text()
            text += extracted
        doc.close()
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""




@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        
        with open(file.filename, "wb") as buffer:
            buffer.write(await file.read())       
        extracted_text = extract_text_pymupdf(file.filename)
        response =  extracted_text 
        os.remove(file.filename)
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
