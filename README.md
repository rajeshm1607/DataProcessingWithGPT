# Data Scraper and Analyzer

This project is a web application built with Flask that scrapes data from specified websites using Apify, expands keywords using OpenAI, and analyzes the scraped data to provide insights.

## Project Structure

- `app.py`: The main Flask application file that handles HTTP requests, expands keywords, scrapes data, and analyzes the data.
- `scrap.py`: Contains the function to scrape data from the specified websites using Apify.
- `templates/index.html`: The HTML template for the web application's front end.

## Requirements

- Python 3.6 or higher
- Flask
- OpenAI API Key
- Apify API Key
- Requests

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. Replace the OpenAI API key and Apify API key in `app.py` and `scrap.py` with your own API keys:
    ```python
    openai.api_key = 'your_openai_api_key'
    apify_client = ApifyClient('your_apify_api_key')
    ```

## Running the Application

1. Start the Flask application:
    ```sh
    python app.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage

1. Enter the enterprise name, keywords, insight request, and websites in the provided form.
2. Click the "Submit" button.
3. The application will expand the keywords, scrape data from the specified websites, analyze the data, and display the insights.

## Example

1. Input:
    - Enterprise: `Target`
    - Keywords: `baby products`
    - Insight Request: `Customer satisfaction with baby products`
    - Websites: `https://www.target.com`

2. Output:
    ```json
    {
        "insights": "Based on the provided data and additional knowledge, customers generally have a positive experience with Target's baby products. They appreciate the quality and variety offered. However, there are occasional complaints about the price and availability of certain items."
    }
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the API used for keyword expansion and data analysis.
- Apify for providing the API used for web scraping.
