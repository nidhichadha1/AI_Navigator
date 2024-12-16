import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("OPEN_AI_API_KEY")

client = OpenAI(api_key=key)
assistant = os.getenv("ASSISTANT_ID")
# --------------------------------------------------------------
# Create assistant
# --------------------------------------------------------------

#assistant = client.beta.assistants.create(
#        name="Runbook Assistant",
#        instructions="You're a helpful runbook assistant for cloud security . Use your knowledge base to best respond to user queries. If you don't know the answer, say simply that you cannot help with question and advice to contact the host directly. Be verbose.",
#        tools=[{"type": "file_search"}],
#        model="gpt-4o-mini",
#    )



print(assistant)


    # Create Vector Store
vector_store = client.beta.vector_stores.create(name="Vigilia Runbooks Knowledge Base_test")
print(f"Vector Store Id - {vector_store.id}")
 
# Upload AWS runbooks
file_paths = ["files/S3 HRO Runbook.docx"]
file_streams = [open(path, "rb") for path in file_paths]
 
 # Add Files To Vector Store
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id = vector_store.id, 
  files = file_streams
)
  
# Check The Status Of Files
print(f"File Status {file_batch.status}")

# Update The Assistant With A Vector Store
assistant = client.beta.assistants.update(
  assistant_id=assistant,
  tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)


print("Assistant Updated with vector store!")

