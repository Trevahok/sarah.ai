from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Any, Type
from src.tool_funcs import scrape_website, search, summary, search_pinecone



class ScrapeWebsiteInput(BaseModel):
    """Inputs for scrape_website"""
    objective: str = Field(
        description="The objective & task that users give to the agent")
    url: str = Field(description="The url of the website to be scraped")

class SummarizerInput(BaseModel):
    """Inputs for summarizer"""
    objective: str = Field(
        description="The key objective that you need to summarize the content for."
    )
    content: str = Field(
        description="The cotent that is to be summarized."
    )

class DBToolInput(BaseModel):
    """Inputs for UIUCDatabaseTool"""
    query: str = Field( description=
        "The query you need to ask UIUC Webpage Database."
    )

class ScrapeWebsiteTool(BaseTool):
    name = "scrape_website"
    description = "useful when you need to get data from a website url, passing both url and objective to the function; DO NOT make up any url, the url should only be from the search results. Be precise with the objective."
    args_schema: Type[BaseModel] = ScrapeWebsiteInput

    def _run(self, objective: str, url: str):
        return scrape_website(objective, url)

    def _arun(self, url: str):
        raise NotImplementedError("error here")

class SearchSERPTool(BaseTool):
    name = "Search"
    description="useful for when you need to answer questions about current events, data or specifics that isn't available in other tools. You should ask targeted questions"

    def _run(self, query: str ):
        return search(query)

    def _arun(self, query: str):
        raise NotImplementedError("error here")

class SummarizerTool(BaseTool):
    name = "Summarizer"
    description = "used to summarize paragraphs and pages. You should pass both objective and content. You should use this sparingly."
    args_schema: Type[BaseModel] = SummarizerInput

    def _run(self,objective:str, content: str ):
        return summary(objective, content)

    def _arun(self, query: str):
        raise NotImplementedError("error here")

class DatabaseTool(BaseTool):
    name = "Database"
    description = "used to get expert data about files or UIUC. Contains personal documents and files uploaded by user. You should consider this as the MOST IMPORTANT but not only source of information about anything related to UIUC or documents."
    args_schema: Type[BaseModel] = DBToolInput

    def _run(self, query:str) -> Any:
        return search_pinecone(query)

    def _arun(self, query: str):
        raise NotImplementedError("error here")