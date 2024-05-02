# Sarah.ai
This LangChain-based agent has access to the following tools : 

- SERP API — Google Search results for a given query and get URLs and context from different websites.
- Wintr — Scrape the provided URL from the SERP API to get more information from any webpage.
- Arxiv — Access recent publications data via Arxiv API and even get a summary of research papers.
- GPT3 summarizer — Summarize data from any of the above using GPT3.

## Instructions
1. Setup a venv
`python3 -m venv venv`
2. Activate venv
`source venv/bin/activate`
3. Install dependencies
`pip3 install -r requirements.txt`
 4. Start server
`streamlit run app.py`  


## Demo
https://youtu.be/Ni_PbXr6keM

## Explanation
https://youtu.be/-z-UKC5KYeY

