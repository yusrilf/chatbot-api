import os
import sys
from langchain.document_loaders import TextLoader

#pip install langchain openai chromadb tiktoken unstructured pypdf
import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.callbacks import get_openai_callback

from langchain.memory import ConversationSummaryMemory, ChatMessageHistory
from langchain.chains.conversational_retrieval.prompts import QA_PROMPT

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler



PERSIST = False

query = None
if len(sys.argv) > 1:
  query = sys.argv[1]

if PERSIST and os.path.exists("persist"):
  print("Reusing index...\n")
  vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
  index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
  #loader = TextLoader("/Users/yusril/Desktop/TugasAkhir/Code/Django/restapi/tutorial/serverapi/testing.txt")
  #pdfFileObj = open('/Users/yusril/Desktop/TugasAkhir/Code/Django/restapi/tutorial/serverapi/qna.pdf', 'rb')
  #loader = PyPDFLoader("/Users/yusril/Desktop/TugasAkhir/Code/Django/restapi/tutorial/serverapi/qna.pdf") # Use this line if you only need data.txt
  #loader = CSVLoader(file_path='/Users/yusril/Desktop/TugasAkhir/Code/Django/restapi/native/data_mentah_komcad_v2.csv')
  loader = CSVLoader(file_path='data_sebagian_komcad.csv', csv_args={
    'delimiter': ';',
    'quotechar': '"',
    'fieldnames': ['Pertanyaan', 'Jawaban']
  })
  #loader = DirectoryLoader("/content/data")

  if PERSIST:
    index = VectorstoreIndexCreator(
    vectorstore_kwargs={"persist_directory":"persist"},
    embedding=OpenAIEmbeddings(),
    text_splitter=CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)#ngareuh
    ).from_loaders([loader])
  else:
    index = VectorstoreIndexCreator().from_loaders([loader])


memory = ConversationSummaryMemory(
    llm = OpenAI(model_name='gpt-4'),
    memory_key='chat_history',
    return_messages=True,
    output_key='answer'
)

chain = ConversationalRetrievalChain.from_llm(
  llm=ChatOpenAI(streaming=True, model="gpt-4",verbose=True),
  retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
  memory = memory,
  chain_type="refine",
  verbose=False,
  max_tokens_limit = 2000,
)