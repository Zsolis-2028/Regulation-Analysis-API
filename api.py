from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, AgentType

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI()

# -----------------------------
# Request Model
# -----------------------------
class Question(BaseModel):
    question: str

# -----------------------------
# Embeddings + Vector DB
# -----------------------------
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load or create vector store
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# Retriever
retriever = db.as_retriever(search_kwargs={"k": 5})

# -----------------------------
# Load PDF + Chunk + Persist
# -----------------------------
loader = PyPDFLoader("epa_docs.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)

db = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
db.persist()

# -----------------------------
# LLM + Agent
# -----------------------------
llm = Ollama(model="llama3.2")

agent = initialize_agent(
    tools=[],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# -----------------------------
# RAG Endpoint
# -----------------------------
@app.post("/rag")
def rag_endpoint(payload: Question):
    question = payload.question
    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
    You are a regulatory assistant. Answer ONLY using the context below.
    If the answer is not in the context, say:
    "I don't have enough information in the provided documents to answer this question."

    Context:
    {context}

    Question: {question}
    """

    response = llm.invoke(prompt)
    return {"answer": response, "sources": docs}

# -----------------------------
# Agent Endpoint
# -----------------------------
@app.post("/agent")
def agent_endpoint(payload: Question):
    question = payload.question
    result = agent.invoke({"input": question})
    return {"answer": result["output"], "steps": result["intermediate_steps"]}