## project setup
1. run installation.py once in the beginning.
2. installation.py does not include automated library installations. That should be done separately - I'll include requirements.txt later if possible.
3. modify the config.py file.
4. install postgreSQL, including vector extension. pgvector is used.
5. create your .env file and include OPENAI_API_KEY. It is needed to use ChatOpenAI and other APIs from OpenAI.
6. When all installation steps are done, run app.py.

## Architecture
1. app.py's llm model decides which pipeline will be needed to fulfill user's question.
2. data retrieval from sql db - find relevant table. Then using schema of the table, create sql query. Check for the sql query safety and runs it. Returned tuples will be used by the agent ai to create proper answer for user's question.
3. data retrieval from vector db - find relevant chunks using vector similarity search. Up to 10 chunks will be retrieved, and that chunks will be provided to the llm model as a prompt so it can find proper information from it to answer user's question.
4. data upload from pdf - write a pdf pathway. It will create chunks of specific token sizes provided after reading the pdf. If not given, 200 will be the default token size. Embedding of each chunk will be generated, and will be inserted into the vector db for further usages.

## How to use
- if properly installed, using it is simple. Simply run the app.py file, and type in the user request in the terminal you ran the file. If it seems to not working, using specific terminologies can enhance the performance, such as 'policy', 'upload' or 'user information'.

## possible enhancements
1. The system does not call multiple pipelines simultaneously. For example, if you ask for a question that requires both information from vector db and sql db, it will only check for one information. That enhancement can be made in the future by making an agent set its own plan.
2. Cost optimization. All agents are currently using gpt-4.1 model, which is much more expensive than mini and nano models.
3. No test scripts are made yet. Creating automated test that uses a json file will be helpful, where the json file will be including both sample question and expected answers. To check for consistency, running the same test script for multiple times will be a necessary step.
