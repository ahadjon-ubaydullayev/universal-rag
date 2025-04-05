from langchain_core.documents import Document
import dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

PDF_BOOK_PATH = "../data/harmony.pdf"
BOOK_CHROMA_PATH = "chroma_data"

dotenv.load_dotenv()

loader = PyPDFLoader(PDF_BOOK_PATH)
pdf_documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

split_docs = []
for doc in pdf_documents:
    chunks = text_splitter.split_text(doc.page_content)
    for chunk in chunks:
        split_docs.append(Document(page_content=chunk, metadata={"page": doc.metadata["page"]}))

reviews_vector_db = Chroma.from_documents(
    split_docs, OpenAIEmbeddings(), persist_directory=BOOK_CHROMA_PATH
)

print(f"✅ Indexed {len(split_docs)} chunks into ChromaDB")
