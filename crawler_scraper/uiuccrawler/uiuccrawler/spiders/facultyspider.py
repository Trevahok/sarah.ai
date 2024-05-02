# mycrawler/mycrawler/spiders/myspider.py
import json
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FacultySpider(scrapy.Spider):
    name = 'faculty_spider'
    allowed_domains = ['illinois.edu']  # Replace with the domain you want to crawl
    start_urls = [ i['profileURL'] for i in json.load(open('/Users/itsakilesh/Downloads/gpt_experiments/crawler_scraper/uiuccrawler/uiuccrawler/fixtures/faculty.json', 'r')) ]
    scraped_data = []

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={'depth': 0})

    def parse(self, response):
        depth = response.meta['depth']
        if depth < 2:
            # Call the scrape function to extract content
            content = self.scrape(response.url)
            self.save_to_json({
                "url": response.url,
                "data": content
            })
            
            # Extract links and follow them
            links = response.css('a::attr(href)').getall()
            for link in links:
                yield response.follow(link, self.parse, meta={'depth': depth + 1})

    def scrape(self, url):

        # Create a Chrome webdriver instance
        driver = webdriver.Chrome()

        try:
            # Open the URL
            driver.get(url)

            # Find the container with the id "content_inner"
            content_inner = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "content"))
            )

            # Get all the text from the container
            container_text = content_inner.text

            # Print the scraped content
            self.logger.info(f"Scraped content from {url}:\n{container_text}")

            return container_text

        except Exception as e:
            self.logger.error(f"An error occurred while scraping {url}: {str(e)}")

        finally:
            # Close the browser when done
            driver.quit()
    
    def save_to_json(self, data):
        current_data = []
        file_name = '/Users/itsakilesh/Downloads/gpt_experiments/crawler_scraper/uiuccrawler/uiuccrawler/fixtures/scraped_data.json'
        
        with open(file_name, 'r') as file:
            current_data = json.load(file)
            current_data.append(data)

        with open(file_name, 'w') as file:
            json.dump(current_data, file)



