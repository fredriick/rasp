import csv
import datetime
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import time
import seaborn as sns

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
        
        # Generate the data visualization and get the chart filename
        chart_filename = generate_chart(df)
        
        # Read the chart image file and encode it as a base64 string
        with open(chart_filename, 'rb') as f:
            chart_data = base64.b64encode(f.read()).decode()
        
        # Render the template with the scraped data and chart
        return render_template('index.html', data=df.to_html(index=False), chart=chart_data)
    
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

                # Delay between requests
                time.sleep(1)  # Sleep for 5 second
    else:
        print("Failed to scrape website. Status code:", response.status_code)

def generate_chart(df):
    # Count the occurrences of each scraped data value
    value_counts = df['Scraped Data'].value_counts()

    # Set the style of the chart using seaborn
    sns.set(style="whitegrid")

    # Create a figure and axes for the chart
    fig, ax = plt.subplots(figsize=(10, 6))

    
    # Create a bar chart
    plt.figure(figsize=(10, 6))
    value_counts.plot(kind='bar')
    plt.xlabel('Scraped Data')
    plt.ylabel('Count')
    plt.title('Scraped Data Visualization')

    # Save the chart to a file
    chart_filename = 'chart.png'
    plt.savefig(chart_filename)
    plt.close()

    return chart_filename

# def generate_chart(df):
#     # Count the occurrences of each scraped data value
#     value_counts = df['Scraped Data'].value_counts()
    
#     # Set the style of the chart using seaborn
#     sns.set(style="whitegrid")
    
#     # Create a figure and axes for the chart
#     fig, ax = plt.subplots(figsize=(10, 6))
    
#     # Customize the chart appearance
#     ax = sns.barplot(x=value_counts.index, y=value_counts.values, palette="Set2")
#     ax.set_xlabel('Scraped Data')
#     ax.set_ylabel('Count')
#     ax.set_title('Scraped Data Distribution')
    
#     # Rotate the x-axis labels if needed
#     plt.xticks(rotation=45, ha='right')
    
#     # Generate a unique file name for the chart image using the current timestamp
#     current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#     chart_filename = f'chart_{current_time}.png'
    
#     # Save the chart to a file
#     plt.savefig(chart_filename)
#     plt.close()
    
#     return chart_filename

if __name__ == '__main__':
    app.run()
