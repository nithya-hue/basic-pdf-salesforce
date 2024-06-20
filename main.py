
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
from typing import List
allowed_origins = [ "*" ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  
    allow_credentials=True,         
    allow_methods=["*"],            
    allow_headers=["*"])

apikey = None


def extract_text_from_pdf(pdf_file) -> List[str]:
    text_chunks = []
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in doc:
        text = page.get_text()
        text_chunks.append(text)
    return text_chunks

@app.post("/upload/")
async def upload_pdf_and_extract_text(pdf_file: UploadFile = File(...)):
    if not pdf_file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Uploaded file is not a PDF.")
    
    try:
        text_chunks = extract_text_from_pdf(pdf_file.file)
        return {"text_chunks": text_chunks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
