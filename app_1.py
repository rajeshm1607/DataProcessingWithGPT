from flask import Flask, render_template, request, jsonify
import openai
from apify_client import ApifyClient
from langchain_community.llms import OpenAI as LangChainOpenAI
from langchain.prompts import PromptTemplate
from openai.error import RateLimitError
import requests
from scrap import scrape_data_from_target

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI API
openai.api_key = 'openaiAPIkey'
# Initialize Apify client
apify_client = ApifyClient('apify_API_token')

# Function to get expanded keywords using OpenAI
def get_expanded_keywords(keywords):
    prompt = f"Generate variations for the following keywords: {keywords}"
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=50
        )
    expanded_keywords = response['choices'][0]['message']['content'].strip().split(',')
    print(f"Expanded Keywords: {expanded_keywords}")  # Print the output to console
    return expanded_keywords

# Function to analyze data using LangChain and OpenAI
def analyze_data(data, insight_request):
    # If the data is too large, summarize it
    # if len(str(data)) > 15000:  # Adjust the length limit as necessary
    #     summary = summarize_data(data)
    #     data = summary
    data = data[:1]
    
    prompt_template = PromptTemplate.from_template(
        "Given the following data: {data}, if the data is irrelevant or insufficient, use your own knowledge to provide the requested insights: {insight_request}"
    )
    formatted_prompt = prompt_template.format(data=data, insight_request=insight_request)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": formatted_prompt}],
        max_tokens=100
    )
    insights = response['choices'][0]['message']['content'].strip()
    print(f"Insights: {insights}")  # Print the output to console
    return insights

# Function to summarize data if it's too large
def summarize_data(data):
    prompt = f"Summarize the following data: {data[:4000]}"  # Taking the first 4000 characters as an example
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    summary = response['choices'][0]['message']['content'].strip()
    return summary

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    enterprise = request.form['enterprise']
    keywords = request.form['keywords']
    insight_request = request.form['insight_request']
    websites_input = request.form['websites']
    websites = [w.strip() for w in websites_input.split(',')] if websites_input else []

    # Expand keywords
    expanded_keywords = get_expanded_keywords(keywords)
    
    # Check if the expanded keywords contain an error message
    if "Error" in expanded_keywords[0]:
        return jsonify({'insights': expanded_keywords[0]})

    # Scrape data using the new method
    scraped_data = scrape_data_from_target(expanded_keywords, websites)
    
    # Analyze data
    insights = analyze_data(scraped_data, insight_request)
    
    return jsonify({'insights': insights})

if __name__ == "__main__":
    app.run(debug=True)
