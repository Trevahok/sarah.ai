from dotenv import load_dotenv
import streamlit as st
from src.agent import agent
from src.ingestion import ingest
import PyPDF2 as pdf 
import io 

load_dotenv()


st.set_page_config(page_title="Sarah", page_icon=":brain:")

st.markdown("<h1 style='text-align: center; '>Sarah</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; '>Like Siri but wayy better</h>", unsafe_allow_html=True)

left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image('./bin/sarah.png')

query = st.chat_input("What are we doing today?")
uploaded_file = st.file_uploader("Pop in a file", type=["pdf", "txt"])



if uploaded_file is not None:
    with st.status("Running..."):
        st.write("Reading file...")
        bytes_data = uploaded_file.read()
        reader = pdf.PdfReader(io.BytesIO( bytes_data) )    
        num_pages = len( reader.pages )

        data = []
        metadata = []
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            metadata.append( {
                "page_num": page_num,
                "file_name": uploaded_file.name
            } )
            data.append(text )
        st.write("Ingesting file ...")
        ingest(data, metadata, "faculty-gpt")
        st.write("Done processing file!")


        
        
        

if query:

    with st.chat_message("User"):
        st.write( query)

    with st.status("Running..."):
        result = agent({"input": query})

    with st.chat_message("Sarah"):
        st.write(result['output'])

