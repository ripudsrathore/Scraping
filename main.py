import requests
from bs4 import BeautifulSoup
import pandas as pd
import time  # To introduce delay if needed

# Define the base URL and the template URL for pagination
base_url = 'https://www.reed.co.uk'
template_url = 'https://www.reed.co.uk/jobs/it-jobs?pageno={}'

# List to hold job titles and their corresponding links
job_data = []

# Loop through the first 300 pages
for page in range(1, 10):  # Adjust the range if you want more or fewer pages
    print(f"Scraping page {page}...")

    # Format the URL for the current page
    url = template_url.format(page)

    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content of the page with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <a> tags that have the 'data-element' attribute set to 'job_title'
        job_links = soup.find_all('a', attrs={'data-element': 'job_title'})

        # Loop through the job links and extract job title and link
        for job in job_links:
            job_title = job.get_text(strip=True)  # Extract job title text
            job_link = job.get('href')  # Extract the relative link from the href attribute

            # If the job_link is relative (starts with /), prepend the base URL
            if job_link.startswith('/'):
                full_job_link = base_url + job_link
            else:
                full_job_link = job_link

            # Append the job title and full link to the job_data list
            job_data.append({'Job Title': job_title, 'Job Link': full_job_link})

    else:
        print(f"Failed to retrieve page {page}. Status code: {response.status_code}")
    
    # OPTIONAL: Introduce a short delay to avoid overwhelming the server
    time.sleep(1)

# If job data is found, save it to an Excel file
if job_data:
    df = pd.DataFrame(job_data)
    df.to_excel('job_listings.xlsx', index=False)
    print('Job data exported successfully to job_listings_all_pages.xlsx')
else:
    print("No job data found to export!")
