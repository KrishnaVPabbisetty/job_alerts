import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv
import time

# Loading the environment variables from .env file
load_dotenv()

# Email details
sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("EMAIL_PASSWORD")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT"))
receiver_emails = os.getenv("RECEIVER_EMAILS").split(",")


# Function to parse the posting date and return a datetime object
def parse_posting_date(posting_date):
    try:
        return datetime.strptime(posting_date.replace("Posted ", ""), "%B %d, %Y")
    except ValueError:
        return None


# Function to send email notifications
def send_email(subject, message):
    try:
        print("Sending email...")
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = "Undisclosed Recipients"
        msg["Subject"] = subject
        msg["Bcc"] = ", ".join(receiver_emails)
        msg.attach(MIMEText(message, "html"))

        # To connect to the Gmail SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_emails, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


# Function to scrape multiple URLs and check the time-elapsed condition
def scrape_amazon_jobs_selenium():
    urls = [
        "https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=recent&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=USA&base_query=software&city=&country=USA&region=&county=&query_options=&",
        "https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=relevant&category%5B%5D=software-development&job_type%5B%5D=Full-Time&country%5B%5D=USA&category_type=studentprograms&distanceType=Mi&radius=24km&latitude=38.89037&longitude=-77.03196&loc_group_id=&loc_query=USA&base_query=software%20development%20engineer&city=&country=USA&region=&county=&query_options=&",
        "https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=recent&category%5B%5D=software-development&country%5B%5D=USA&distanceType=Mi&radius=24km&latitude=38.89037&longitude=-77.03196&loc_group_id=&loc_query=USA&base_query=software%20engineer&city=&country=USA&region=&county=&query_options=&",
        "https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=relevant&job_type%5B%5D=Full-Time&country%5B%5D=USA&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=&base_query=software%20engineer%20entry%20level&city=&country=&region=&county=&query_options=&",
        "https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=relevant&job_type%5B%5D=Full-Time&country%5B%5D=USA&distanceType=Mi&radius=24km&industry_experience=less_than_1_year&latitude=&longitude=&loc_group_id=&loc_query=&base_query=software%20engineer%20entry%20level&city=&country=&region=&county=&query_options=&",
        "https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=relevant&job_type%5B%5D=Full-Time&country%5B%5D=USA&distanceType=Mi&radius=24km&industry_experience=one_to_three_years&latitude=&longitude=&loc_group_id=&loc_query=&base_query=software%20engineer%20entry%20level&city=&country=&region=&county=&query_options=&",
        "https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=relevant&category%5B%5D=software-development&job_type%5B%5D=Full-Time&country%5B%5D=USA&distanceType=Mi&radius=24km&industry_experience=one_to_three_years&latitude=&longitude=&loc_group_id=&loc_query=&base_query=software%20engineer%20entry%20level&city=&country=&region=&county=&query_options=&",
        "https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=relevant&category%5B%5D=software-development&job_type%5B%5D=Full-Time&country%5B%5D=USA&distanceType=Mi&radius=24km&industry_experience=less_than_1_year&latitude=&longitude=&loc_group_id=&loc_query=&base_query=software%20engineer%20entry%20level&city=&country=&region=&county=&query_options=&",
    ]
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    jobs = []

    for url in urls:
        try:
            print(f"Opening URL: {url}")
            driver.get(url)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "job-tile"))
            )

            job_cards = driver.find_elements(By.CLASS_NAME, "job-tile")
            print(f"Found {len(job_cards)} job cards on {url}.")

            for job_card in job_cards:
                try:
                    title_element = job_card.find_element(By.CLASS_NAME, "job-title")
                    title = title_element.text
                    link = title_element.find_element(By.TAG_NAME, "a").get_attribute(
                        "href"
                    )

                    location_element = job_card.find_element(
                        By.CLASS_NAME, "location-and-id"
                    )
                    location = location_element.find_elements(By.TAG_NAME, "li")[0].text

                    # Extract job ID
                    job_id = link.split("/")[-2]

                    # Extract job posting date
                    posting_date_element = job_card.find_element(
                        By.CLASS_NAME, "posting-date"
                    )
                    posting_date = (
                        posting_date_element.text if posting_date_element else "N/A"
                    )

                    # Check if the job was updated within the last hour
                    time_elapsed_element = job_card.find_element(
                        By.CLASS_NAME, "meta.time-elapsed"
                    )
                    time_elapsed = (
                        time_elapsed_element.text.lower()
                    )  # Example: "updated about 1 hour ago"
                    if " 1 hour" in time_elapsed or "minutes ago" in time_elapsed:
                        jobs.append(
                            {
                                "title": title,
                                "location": location,
                                "job_id": job_id,
                                "url": link,
                                "posting_date": posting_date,
                                "time_elapsed": time_elapsed,
                            }
                        )
                except Exception as e:
                    print(f"Error parsing job card: {e}")
        except Exception as e:
            print(f"Error loading URL {url}: {e}")

    driver.quit()
    return jobs


# Notification function to handle filtered jobs
def notify_jobs_by_email():
    jobs = scrape_amazon_jobs_selenium()
    if jobs:
        message = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; }
                h2 { color: #333; font-size: 24px; }
                .job-title { font-size: 18px; font-weight: bold; color: #4CAF50; }
                .job-details { font-size: 14px; color: #555; }
                .job-link { display: inline-block; background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
                .job-link:hover { background-color: #45a049; }
                .job-list { list-style-type: none; padding: 0; }
                .job-list li { margin-bottom: 15px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            </style>
        </head>
        <body>
        <h2>Amazon Latest Job's</h2>
        <ul class="job-list">
        """

        for job in jobs:
            job_message = f"""
            <li>
                <div class="job-title">{job['title']}</div>
                <div class="job-details"><i>{job['location']} | Job ID: {job['job_id']}</i><br>
                <i>Posted: {job['posting_date']}</i><br>
                <i>{job['time_elapsed']}</i></div>
                <a class="job-link" href="{job['url']}">Apply Here</a>
            </li>
            """
            message += job_message

        message += """
        </ul>
        </body>
        </html>
        """

        send_email("Amazon Latest Job's", message)
    else:
        print("No jobs updated within the last hour.")


if __name__ == "__main__":
    notify_jobs_by_email()
