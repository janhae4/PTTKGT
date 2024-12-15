import requests
from bs4 import BeautifulSoup

# URL of the dataset or page hosting the dataset
page_url = "https://www.philippe-fournier-viger.com/spmf/index.php?link=datasets.php"

# Name of the file you want to download
target_file = "accidents_negative.txt"

try:
    # Fetch the HTML of the page
    response = requests.get(page_url)
    response.raise_for_status()  # Raise an error for bad HTTP response codes
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the link to the target file
    links = soup.find_all('a', href=True)
    file_link = None
    for link in links:
        if target_file in link['href']:
            file_link = link['href']
            break
    
    if file_link:
        # Construct the full URL if needed
        if not file_link.startswith("http"):
            file_link = "https://www.philippe-fournier-viger.com/spmf/" + file_link
        
        # Download the file
        file_response = requests.get(file_link)
        file_response.raise_for_status()
        
        # Save the file locally
        with open(target_file, "w") as f:
            f.write(file_response.text)
        print(f"File '{target_file}' downloaded successfully.")
    else:
        print(f"Could not find the file link for '{target_file}' on the page.")
except Exception as e:
    print(f"An error occurred: {e}")
