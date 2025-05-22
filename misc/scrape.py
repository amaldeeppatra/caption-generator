import requests
from bs4 import BeautifulSoup

def scrape_schemes(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract schemes and descriptions (Adjust the tags and classes based on the actual structure of the website)
        schemes = []
        for scheme_section in soup.find_all('div', class_='scheme-card'):  # Adjust the class name as needed
            title = scheme_section.find('h3').get_text(strip=True) if scheme_section.find('h3') else 'No Title'
            description = scheme_section.find('p').get_text(strip=True) if scheme_section.find('p') else 'No Description'
            schemes.append({
                'title': title,
                'description': description
            })

        # Save the results to a file
        with open('schemes_and_descriptions.txt', 'w', encoding='utf-8') as file:
            for scheme in schemes:
                file.write(f"Title: {scheme['title']}\n")
                file.write(f"Description: {scheme['description']}\n\n")

        print(f"Successfully scraped {len(schemes)} schemes and saved to schemes_and_descriptions.txt")
    except requests.exceptions.RequestException as e:
        print(f"Error while fetching the URL: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# URL of the webpage to scrape
url = "https://www.myscheme.gov.in/search/category/Education%20&%20Learning"

scrape_schemes(url)
