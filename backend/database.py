from dotenv import load_dotenv
import os
import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Property, DataType, Configure
import weaviate.classes as wvc
from weaviate.classes.tenants import Tenant
import hashlib
from typing import List
import streamlit as st
from streamlit import session_state

if 'user_id' not in session_state:
    userid = ""
else:
    userid = session_state.user_id


# Load environment variables from a .env file
load_dotenv()

# Get the API token from the environment variables
weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
cohere_api_key = os.environ["COHERE_API_KEY"]

headers = {
    "X-Cohere-Api-Key": cohere_api_key,
}

# Connect to Weaviate Cloud
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_key),
    headers=headers
)

collection = client.collections.get("Users")

def sign_up(username, password):

    # Hash the username and password to create a unique ID
    hash_input = username + password
    hash_id = hashlib.sha256(hash_input.encode()).hexdigest()

    # Check if the username and password combination already exists
    tenants = collection.tenants.get()

    if hash_id in tenants:
        print("This combination of username and password already exists. Please use a different username or password.")
    else:
        # Create a new tenant with the hashed ID
        collection.tenants.create(
    tenants=[
        Tenant(name=hash_id),
        ]
    )
        return hash_id
    

def log_in(username, password):

    # Hash the username and password to recreate the unique ID
    hash_input = username + password
    hash_id = hashlib.sha256(hash_input.encode()).hexdigest()

    tenants = collection.tenants.get()

    if hash_id in tenants:
        print("You have successfully logged in.")
        return hash_id
    else:
        print("User not found. Please sign up first.")




def chunk(text: str, chunk_size: int, overlap_size: int) -> List[str]:
    import re

    source_text = re.sub(r"\s+", " ", text)  # Remove multiple whitespaces
    text_words = re.split(r"\s", source_text)  # Split text by single whitespace

    chunks = []
    for i in range(0, len(text_words), chunk_size):  # Iterate through & chunk data
        chunk = " ".join(text_words[max(i - overlap_size, 0): i + chunk_size])  # Join a set of words into a string
        chunks.append(chunk)
    return chunks


def get_chunks_list(chunked_text: List[str], source, description):

    chunks_list = list()
    for i, chunk in enumerate(chunked_text):
        data_properties = {
            "startup_description": description,
            "source": source,
            "content": chunk
        }
        data_object = wvc.data.DataObject(properties=data_properties)
        chunks_list.append(data_object)
    return chunks_list

def add_data(chunks_list, userid):

    # get the tenant
    user = collection.with_tenant(userid)

    # Insert the data
    object_id = user.data.insert_many(chunks_list)

    return object_id

def get_startup_info(userid):
    user_data = collection.with_tenant(userid)

    result = user_data.query.fetch_objects(
        limit=1,
        return_properties=["startup_description"]
    )

    return result.objects[0].properties["startup_description"]


def query_db(query):
    user_data = collection.with_tenant(userid)

    # Perform vector search on tenantA's version
    response = user_data.query.near_text(
        query=query,
        limit=5
    )

    res = response.objects

    context = ""

    for o in res:
        context += o.properties['content']
    print(context)
    
    return context