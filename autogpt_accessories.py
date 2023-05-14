from langchain.agents import AgentType, initialize_agent
from langchain.experimental import AutoGPT
from langchain.agents import Tool
from langchain.tools import DuckDuckGoSearchRun
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate 
import faiss


def autogpt_process(input_file, output_file):
    GOAL_PROMPT = PromptTemplate(input_variables=['input_file', 'output_file'],
                             template="""
                            Read {input_file} file which have two columns "Keywords" and "URL", 
                            get the "Keywords" columns values and search that in "google" using search tool don't use python for searching and get the first URL,
                            paste all the relevant URLs in the "URL" column for each keyword, do it for all keywords and then finally save the updated dataframe as {output_file} file.
                            """)

    search = DuckDuckGoSearchRun()
    tools = [
        Tool(
            name = "search",
            func=search.run,
            description="useful for when you need to answer questions about current events or you need to search something in google. Always use this tool for searching."
        ),  
        WriteFileTool(),
        ReadFileTool(),
    ]
    llm = ChatOpenAI(temperature=0)

    # Define your embedding model
    embeddings_model = OpenAIEmbeddings()
    embedding_size = 1536
    index = faiss.IndexFlatL2(embedding_size)
    vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

    agent = AutoGPT.from_llm_and_tools( ai_name = "Asst",
                                    ai_role = "Personal assistant",
                                    llm = llm,
                                    tools = tools,
                                    memory = vectorstore.as_retriever()
                                    )
    # agent.chain.verbose = False

    agent.run([GOAL_PROMPT.format(input_file = input_file, output_file=output_file)])

    return "Files processed suffessfully and saved to {output_file}"