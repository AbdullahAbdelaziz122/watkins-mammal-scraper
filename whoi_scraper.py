import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin

# Configuration 
BASE_URL = "https://whoicf2.whoi.edu/science/B/whalesounds/"
INDEX_URL = urljoin(BASE_URL, "index.cfm")
DOWNLOAD_DIR = "whoi_whale_sounds"


def get_page_content(url):
    """Fetches the content of a given URL."""
    print(f"Fetching: {url}")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()  
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def get_category_links(html_content):
    """Parses the main page HTML to extract species names and their category URLs."""
    print("Parsing category links...")
    soup = BeautifulSoup(html_content, 'html.parser')
    category_links = {}
    
    # The links are in the 'Common name' dropdown select element
    select_tag = soup.find('select', {'id': 'getSpeciesCommon'})
    
    if select_tag:
        for option in select_tag.find_all('option'):
            url = option.get('value')
            name = option.text.strip()
            
            # Filter out the default 'Select' option and any other non-link options
            if url and 'bestOf.cfm?code=' in url:
                category_links[name] = url
    
    print(f"Found {len(category_links)} species categories.")
    return category_links

def get_download_links(html_content, species_name):
    """Parses a category page HTML to extract direct sound file download links."""
    print(f"  Parsing download links for {species_name}...")
    soup = BeautifulSoup(html_content, 'html.parser')
    download_links = []
    

    
    
    for a_tag in soup.find_all('a', string='Download'):
       
        relative_link = a_tag.get('href')
        
        if relative_link and relative_link.endswith('.wav'):
            
            full_download_url = urljoin(BASE_URL, relative_link)
            download_links.append(full_download_url)
            
    print(f"  Found {len(download_links)} sound files for {species_name}.")
    return download_links

def download_file(url, species_name, file_index):
    """Downloads a single file and saves it to the appropriate directory."""
    
    # Extract the file name from the URL path
    filename = os.path.basename(url)
    
    if not filename or not filename.endswith('.wav'):
        print(f"  Could not determine filename for URL: {url}")
        return
    
    # Create a clean directory name for the species
    clean_species_name = re.sub(r'[^\w\-_\. ]', '_', species_name).strip()
    species_dir = os.path.join(DOWNLOAD_DIR, clean_species_name)
    
    # Create directory if it doesn't exist
    os.makedirs(species_dir, exist_ok=True)
    
    file_path = os.path.join(species_dir, filename)
    
    if os.path.exists(file_path):
        print(f"  File already exists, skipping: {file_path}")
        return

    print(f"  Downloading file {file_index}: {filename} to {species_dir}")
    
    try:
        # The URL is the direct link to the .wav file.
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
    
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"  Successfully downloaded: {filename}")
        
    except requests.exceptions.RequestException as e:
        print(f"  Error downloading {filename} from {url}: {e}")

def main():
    """Main function to orchestrate the scraping and downloading process."""
    print("Starting WHOI Marine Mammal Sound Database Scraper...")
    
    # 1. Get the main page content
    main_page_html = get_page_content(INDEX_URL)
    if not main_page_html:
        print("Failed to fetch main page. Exiting.")
        return

    # 2. Extract all category links
    category_links = get_category_links(main_page_html)
    if not category_links:
        print("No category links found. Exiting.")
        return

    # 3. Iterate through each category
    total_files_downloaded = 0
    
    for species_name, category_url in category_links.items():
        print(f"\n--- Processing Species: {species_name} ---")
        
        # 4. Get the category page content
        category_page_html = get_page_content(category_url)
        if not category_page_html:
            print(f"Failed to fetch category page for {species_name}. Skipping.")
            continue
            
        # 5. Extract all download links for this species
        download_urls = get_download_links(category_page_html, species_name)
        
        # 6. Download each file
        for i, url in enumerate(download_urls, 1):
            download_file(url, species_name, i)
            total_files_downloaded += 1
            
    print("\n--- Scraping Complete ---")
    print(f"Total files processed (attempted to download): {total_files_downloaded}")
    print(f"Files are saved in the '{DOWNLOAD_DIR}' directory.")

if __name__ == "__main__":
    main()
