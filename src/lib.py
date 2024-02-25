import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
import pinecone
import os 


load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL_NAME = 'text-embedding-ada-002'
PINECONE_INDEX = os.getenv("PINECONE_INDEX")


def tiktoken_len(text):
    # encoding = tiktoken.encoding_for_model(GPT_MODEL_NAME)
    tokenizer = tiktoken.get_encoding('cl100k_base')
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)

def chunkifier():
    chunkifier = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=20,
        length_function=tiktoken_len,
        separators=["\n\n", "\n", " ", ""]
    )
    return chunkifier


def init_pinecone():
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENV
    )
    if PINECONE_INDEX not in pinecone.list_indexes():
        # we create a new index
        pinecone.create_index(
            name=PINECONE_INDEX,
            metric='cosine',
            dimension=1536
        )
def embedder():
    embed = OpenAIEmbeddings(
        model=EMBEDDING_MODEL_NAME ,
        openai_api_key=OPENAI_API_KEY
    )
    return embed




init_pinecone()
embed = embedder()
chunker = chunkifier()