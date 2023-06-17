import csv
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the form inputs
        url = request.form['url']
        element = request.form['element']
        
        # Call the function to scrape the website and export data to CSV
        scrape_website(url, element)
        
        # Read the scraped data from the CSV file
        df = pd.read_csv('scraped_data.csv')
        
        # Render the template with the scraped data
        return render_template('index.html', data=df.to_html(index=True))
    
    return render_template('index.html')

def scrape_website(url, element):
    # Send a GET request to the website
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all the HTML elements based on user input
        elements = soup.find_all(element)
        
        # Create a CSV file and write the scraped data
        with open('scraped_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write headers to the CSV file
            writer.writerow(['Scraped Data'])
            
            # Write the scraped data to the CSV file
            for elem in elements:
                writer.writerow([elem.get_text()])
    else:
        print("Failed to scrape website. Status code:", response.status_code)

if __name__ == '__main__':
    app.run()
