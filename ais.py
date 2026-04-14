from utils import nano_model, mini_model, o_model, message_creator, output_extractor

from langchain.agents import create_agent
from langchain.tools import tool

from db_rel import select_from_table, get_table_info

from dotenv import load_dotenv
#for testing purpose
try:
    # just to call the llm api key. I have used OpenAI API, and key is included in .env file. To test it on your own, please set your own .env file
    load_dotenv()
except:
    print('error, .env file not found')
    exit(0)


@tool
def find_table() -> str:
    """Returns the name of the table in the database."""
    # currently only returns 'users' for testing purposes. In actual implementation, it should search for a relevant table
    # using vector search, after creating a vector db with table name and table summary in it. table summary will have the embedding vector,
    # which will be used for similarity check. For this assessment, due to limited time I have, I will leave it as to return only users.
    return "users"

@tool
def extract_table_schema(table_name: str) -> dict:
    """Returns the schema of the table with table_name. Not a tool! but can be added as a tool if needed."""
    return get_table_info(table_name)

@tool
def postgresql_query_creating_internal(postgresql_query: str):
    """
Create postgresql postgresql_query based on the input given.
Allowed clauses are select, from, join, where, group by, having, order by.
You MUST strictly use only the table names and column names exactly as they appear in the provided table schema.
"""
    return postgresql_query

@tool
def create_sql(user_input: str) -> str:
    """
    __parameter__: 
        user_input: a natural language query from the user
    __output__:
        sql query: a SQL query that can be executed in the database to retrieve the desired information based on the user_input
    __summary__: 
        Returns a SQL query to retrieve all data from the users table."""
    
    # using agent for sql query creation for better performance. However, it can be replaced by other methods later if necessary.
    sql_agent = create_agent(o_model, tools=[postgresql_query_creating_internal])
    resp = sql_agent.invoke(message_creator(user_input))
    return output_extractor(resp)

@tool
def sql_query_runner(sql_query: str) -> bool:
    """Executes the given SQL query in the database and returns the result. Only SELECT queries are allowed."""
    # go through a safety check first to make sure only SELECT queries are executed. This is a very basic check and can be improved later if necessary.
    if sql_query.split(" ")[0].lower() != "select":
        return "Only SELECT queries are allowed."
    return select_from_table(sql_query)


data_retrieval_tools = [
    find_table,
    extract_table_schema,
    create_sql,
    sql_query_runner,
]

data_retrieval_agent = create_agent(
    o_model, data_retrieval_tools
)

sql_retrieval_rule_prompt = """
Always use the tools in a following steps. 1. find_table to find the table name. 
2. extract_table_schema to find the schema of the table. 
3. create_sql to create a SQL query based on the user input and the table schema. 
4. sql_query_runner to execute the SQL query and get the result. 
Always follow this order and do not skip any steps. Always use all tools in order."""

def data_retrieval_agent_call(user_input: str):
    """This agent retrieves data from the sql database based on the user_input."""
    resp = data_retrieval_agent.invoke(message_creator(sql_retrieval_rule_prompt + user_input))
    return output_extractor(resp)
# resp = data_retrieval_agent.invoke(message_creator(retrieval_rule_prompt + "What is the email address of John Doe?"))
# print(output_extractor(resp))

import rag

def policy_retrieval_task(user_input: str):
    """This agent retrieves policy information based on the user_input."""
    # specifically used to retrieve policy information, which was uploaded as an unstructured document.
    output = rag.retrieve_similar_content(user_input)
    policy_retrieval_prompt = f"""Use following information to answer the user's question.
---Information found---\n
{output}
---End of information---\n
user's query:\n
{user_input}"""
    return policy_retrieval_prompt
    
policy_answering_agent = create_agent(o_model, tools=[policy_retrieval_task])

def policy_retrieval_agent_call(user_input: str):
    """This agent retrieves policy information based on the user_input."""
    resp = policy_answering_agent.invoke(message_creator(user_input))
    return output_extractor(resp)

@tool
def policy_upload_agent(pdf_path: str):
    """This agent uploads the policy document to the vector database after chunking and embedding."""
    # specifically used to upload policy document, which is an unstructured document. It will chunk the document into smaller pieces, then embed each piece and upload it to the vector database.
    rag.insert_pdf(pdf_path=pdf_path)
    pass

policy_uploading_agent = create_agent(o_model, tools=[policy_upload_agent])

def policy_upload_agent_call(pdf_path: str):
    """This agent uploads the policy document to the vector database after chunking and embedding."""
    resp = policy_uploading_agent.invoke(message_creator(pdf_path))
    return output_extractor(resp)

agent_calls = [data_retrieval_agent_call, policy_retrieval_agent_call, policy_upload_agent_call]
