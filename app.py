temp = input("Enter your request: ")

from ais import agent_calls
# pre-processing
from utils import o_model
preprocessing_prompt = f"""
Check the user's request and decide what methods can be called. Methods allowed are:
1. data retrieval from the sql database, for any user information retrieval.
2. policy retrieval, for any policy information retrieval.
3. policy upload, for uploading any policy document.
4. None. Not calling any methods.
You must answer in a number between 1 to 4.
"""
response = o_model.invoke(preprocessing_prompt + temp)
# print(response.content)
if "1" in response.content:
    print(agent_calls[0](temp))
elif "2" in response.content:
    print(agent_calls[1](temp))
elif "3" in response.content:
    pdf_path = input("Enter the PDF file path to upload: ")
    print(agent_calls[2](pdf_path))
elif "4" in response.content:
    print("No methods are called. Here is the response to the user's query:")
    print(response.content)