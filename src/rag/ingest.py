from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Caminhos para os arquivos e pastas
PDF_PATH = "data/base_conhecimento.pdf"
VECTOR_STORE_PATH = "vector_store"

def main():
    print("Iniciando o processo de ingestão do documento PDF...")

    # 1. Carregar o documento
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"PDF carregado. {len(documents)} página(s) encontradas.")

    # 2. Dividir o texto em chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    print(f"Documento dividido em {len(chunks)} chunks.")

    # 3. Gerar embeddings e criar o Vector Store com ChromaDB
    # Usamos um modelo do Hugging Face que roda localmente.
    print("Gerando embeddings e criando o Vector Store... (isso pode levar alguns minutos)")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # O ChromaDB criará o banco de dados na pasta especificada e salvará no disco.
    db = Chroma.from_documents(
        chunks, 
        embeddings, 
        persist_directory=VECTOR_STORE_PATH
    )
    print("Vector Store criado com sucesso!")
    print(f"Total de vetores no banco: {db._collection.count()}")

if __name__ == "__main__":
    main()