from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

VECTOR_STORE_PATH = "vector_store"

def get_retriever():
    """
    Carrega o Vector Store do disco e o retorna como um objeto retriever.
    """
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Carrega o banco de dados do disco
    vector_store = Chroma(
        persist_directory=VECTOR_STORE_PATH, 
        embedding_function=embeddings
    )
    
    # Converte o Vector Store em um retriever, que é a interface de busca
    return vector_store.as_retriever(search_kwargs={"k": 3})

# Inicializa o retriever uma vez quando o módulo é carregado
print("[Retriever] Carregando o Vector Store do disco...")
retriever = get_retriever()
print("[Retriever] Vector Store carregado e pronto.")