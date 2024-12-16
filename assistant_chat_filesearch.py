import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("OPEN_AI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")
#vector_id = os.getenv("VECTOR_ID")
client = OpenAI(api_key=key)

# Create Vector Store
#vector_store = client.beta.vector_stores.create(name="Vigilia Runbooks Knowledge Base")
#print(f"Vector Store Id - {vector_store.id}")
 
# Upload AWS runbooks
#file_paths = ["files/S3 HRO Runbook.docx"]
#file_streams = [open(path, "rb") for path in file_paths]
 
 # Add Files To Vector Store
#file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
 # vector_store_id = vector_store.id, 
 # files = file_streams
#)
  
# Check The Status Of Files
#print(f"File Status {file_batch.status}")

# Update The Assistant With A Vector Store
#assistant = client.beta.assistants.update(
# assistant_id=assistant_id,
#  tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
#)
#print("Assistant Updated with vector store!")

# Create A Thread
thread = client.beta.threads.create()
print(f"Your thread id is - {thread.id}\n\n")

# Run a loop where user can ask questions
while True:
    text = input("What's your question?\n")

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text,
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant_id
    )

    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    message_content = messages[0].content[0].text
    print("Response: \n")
    print(f"{message_content.value}\n")
