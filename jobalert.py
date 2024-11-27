from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_amazon_jobs_selenium():
    # Set up Selenium with ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run headlessly
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    service = Service('C:/Users/pc/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    URL = "https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=recent&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=USA&base_query=software&city=&country=USA&region=&county=&query_options="
    
    print("Opening URL...")
    driver.get(URL)
    print("Page Loaded!")
    
    # Wait for jobs to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'job-tile'))
    )

    # Extract job postings
    jobs = []
    job_cards = driver.find_elements(By.CLASS_NAME, 'job-tile')
    print(f"Found {len(job_cards)} job cards.")
    
    for job_card in job_cards:
        try:
            title_element = job_card.find_element(By.CLASS_NAME, 'job-title')
            title = title_element.text
            link = title_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            
            location_element = job_card.find_element(By.CLASS_NAME, 'location-and-id')
            location = location_element.find_elements(By.TAG_NAME, 'li')[0].text  # Location is the first <li> element
            
            # Extract job ID from the URL
            job_id = link.split('/')[-2]  # Job ID is in the URL before the job title

            # Extract job posting date
            posting_date_element = job_card.find_element(By.CLASS_NAME, 'posting-date')
            posting_date = posting_date_element.text if posting_date_element else "N/A"

            jobs.append({'title': title, 'location': location, 'job_id': job_id, 'url': link, 'posting_date': posting_date})
        except Exception as e:
            print(f"Error parsing job card: {e}")
    
    driver.quit()
    
    # Print formatted output
    print("\nJob Listings:")
    for i, job in enumerate(jobs, 1):
        print(f"\n{str(i)}. {job['title']}")
        print(f"   {job['location']} | {job['job_id']}")
        print(f"   Posted: {job['posting_date']}")
        print(f"   URL: {job['url']}")
    
    return jobs

# Call the function to test
scrape_amazon_jobs_selenium()