from langchain import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
from langchain.chains.question_answering import load_qa_chain
from urllib.parse  import quote
# from serpapi import GoogleSearch


from bs4 import BeautifulSoup
import pinecone

import requests
import json
import os
import src.lib as lib

import streamlit as st 

brwoserless_api_key = os.getenv("BROWSERLESS_API_KEY")
wintr_api_key = os.getenv("WINTR_API_KEY")
serper_api_key = os.getenv("SERP_API_KEY")
pinecone_index = os.getenv("PINECONE_INDEX")

index = pinecone.Index(pinecone_index)

def search(query):
    url = f"https://serpapi.com/search.json?api_key={serper_api_key}&engine=google&q=" + quote(query)

    response = requests.request("GET", url)
    print(response.text)
    
    return summary(query, response.text)
  


def scrape_website(objective: str, url: str):

    print("Scraping website...")
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
    }

    data = {
        "url": url, 
        "apikey": wintr_api_key
    }

    data_json = json.dumps(data)

    # Send the POST request
    post_url = f"https://api.wintr.com/fetch"
    response = requests.post(post_url, headers=headers, data=data_json)

    st.write( f"Scraping {url} for {objective}"  ) 

    # Check the response status code
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text() 
        print("CONTENTTTTTT:", text)

        if len(text) > 10000:
            output = summary(objective, text)
            return output
        else:
            return text
    else:
        print(f"HTTP request failed with status code {response.status_code}")


def summary(objective:str, content:str):
    st.write( f"Summarizing { content[:min(100, len(content))] }for {objective} "  ) 

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125")

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=8000, chunk_overlap=500)
    docs = text_splitter.create_documents([content])
    map_prompt = """
    ### INSTRUCTION:
    Write a summary of the following text for {objective} without losing any major details:
    "{text}"
    ### SUMMARY:
    """
    map_prompt_template = PromptTemplate(
        template=map_prompt, input_variables=["text", "objective"])

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type='map_reduce',
        map_prompt=map_prompt_template,
        combine_prompt=map_prompt_template,
        verbose=True
    )

    output = summary_chain.run(input_documents=docs, objective=objective)

    return output

def search_pinecone(query:str)  :
    st.write( f"Searching Database for {query}"  ) 

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125")
    chain = load_qa_chain(llm, chain_type="stuff")
    vectorstore = Pinecone.from_existing_index(pinecone_index, lib.embed)
    docs = vectorstore.similarity_search(query, k = 5)
    ans = chain.run(input_documents=docs, question=query)
    return ans 






