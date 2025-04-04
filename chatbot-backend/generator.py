import dotenv
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema.runnable import RunnablePassthrough

BOOKS_CHROMA_PATH = "chroma_data/"

dotenv.load_dotenv()

review_template_str = """You are a helpful assistant that provides clear and well-formatted responses. Follow these guidelines:

1. For simple, direct answers:
   - Provide a concise, clear response
   - Use basic formatting only when needed (bold for emphasis)
   - No need for complex structure

2. For complex or detailed information:
   - Use Markdown formatting for better readability
   - Break down information into logical sections
   - Use headers (##) for main sections
   - Use bullet points for lists
   - Use bold (**) for important information

3. Always:
   - Be direct and clear
   - Use appropriate formatting based on content complexity
   - Maintain readability
   - Say "I don't know" if the context doesn't contain the answer

Context:
{context}

Remember: Adapt your formatting to the complexity of the information. Simple answers should be simple, while complex information can use more structured formatting."""


review_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["context"],
        template=review_template_str,
    )
)

review_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["question"],
        template="{question}",
    )
)
messages = [review_system_prompt, review_human_prompt]

review_prompt_template = ChatPromptTemplate(
    input_variables=["context", "question"],
    messages=messages,
)

chat_model = ChatOpenAI(model="gpt-3.5-turbo-0125", model_name="gpt-3.5-turbo-0125", temperature=0)


reviews_vector_db = Chroma(
    persist_directory=BOOKS_CHROMA_PATH,
    embedding_function=OpenAIEmbeddings()
)
print("Number of stored documents:", reviews_vector_db._collection.count())

# reviews_retriever = reviews_vector_db.as_retriever(k=10)
reviews_retriever = reviews_vector_db.as_retriever(search_type="similarity", search_kwargs={"k": 5})

def format_retrieved_documents(docs):
    """Extracts and formats the retrieved document content into a single string."""
    return "\n\n".join([doc.page_content for doc in docs]) if docs else "No relevant information found."

output_parser = StrOutputParser()


review_chain = (
    {
        "context": reviews_retriever|format_retrieved_documents,
        "question": RunnablePassthrough(),
    }
    | review_prompt_template
    | chat_model
    | output_parser
)



# # context = "I had a great stay!"
# question = "Who are the cardiology specialists?"
# question = "Who are the cardiology specialists?"
# print(review_chain.invoke(question))