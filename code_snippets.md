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

@app.post("/agent")
def agent_endpoint(payload: Question):
    question = payload.question
    result = agent.invoke({"input": question})
    return {"answer": result["output"], "steps": result["intermediate_steps"]}

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
retriever = db.as_retriever(search_kwargs={"k": 5})

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
retriever = db.as_retriever(search_kwargs={"k": 5})

loader = PyPDFLoader("epa_docs.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)

db = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
db.persist()