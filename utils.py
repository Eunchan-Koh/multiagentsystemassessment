from langchain_openai import ChatOpenAI, OpenAIEmbeddings

NANO_MODEL = 'gpt-4.1-nano'
MINI_MODEL = 'gpt-4.1-mini'
MODEL = 'gpt-4.1'

# llm model set up
o_model = ChatOpenAI(model=MODEL, temperature=0)
mini_model = ChatOpenAI(model=MINI_MODEL, temperature=0)
nano_model = ChatOpenAI(model=NANO_MODEL, temperature=0)

# embedding model set up
embeddings_model = OpenAIEmbeddings()

# langchain agent needs specific format as an input. Use this function to create a message in the correct format easily.
def message_creator(content: str):
    """used to create a message to invoke an agent"""
    return {"messages": [{"role": "user", "content": content}]}

# langchain agent does not output the last comment. Use this function to extract the final output from the agent's response.
def output_extractor(output: dict):
    """used to extract the output from the ai response"""
    try:
        result = output['messages'][-1].content
    except Exception as e:
        print(f"Error extracting output from output_extractor. Check langchain/openai output format: {e}")
        result = 'Error extracting output from output_extractor.'
    return result