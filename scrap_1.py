import os
from apify_client import ApifyClient

# Replace with your Apify API token
APIFY_API_TOKEN = 'apify_API_token'

def scrape_data_from_target(keywords, urls):
    # Initialize the ApifyClient with your API token
    client = ApifyClient(APIFY_API_TOKEN)

    # Validate and prepare start URLs
    start_urls = []
    for url in urls:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url  # Default to HTTP if no scheme is provided
        start_urls.append({"url": url})

    # Prepare the Actor input
    run_input = {
        "startUrls": start_urls,
        "useSitemaps": False,
        "crawlerType": "playwright:adaptive",
        "includeUrlGlobs": [],
        "excludeUrlGlobs": [],
        "ignoreCanonicalUrl": False,
        "maxCrawlDepth": 5,
        "maxCrawlPages": 5,
        "initialConcurrency": 10,
        "maxConcurrency": 200,
        "initialCookies": [],
        "proxyConfiguration": { "useApifyProxy": True },
        "maxSessionRotations": 10,
        "maxRequestRetries": 5,
        "requestTimeoutSecs": 60,
        "minFileDownloadSpeedKBps": 128,
        "dynamicContentWaitSecs": 5,
        "maxScrollHeightPixels": 5000,
        "removeElementsCssSelector": """nav, footer, script, style, noscript, svg,
    [role=\"alert\"],
    [role=\"banner\"],
    [role=\"dialog\"],
    [role=\"alertdialog\"],
    [role=\"region\"][aria-label*=\"skip\" i],
    [aria-modal=\"true\"]""",
        "removeCookieWarnings": True,
        "clickElementsCssSelector": "[aria-expanded=\"false\"]",
        "htmlTransformer": "readableText",
        "readableTextCharThreshold": 100,
        "aggressivePrune": False,
        "debugMode": False,
        "debugLog": False,
        "saveHtml": False,
        "saveMarkdown": True,
        "saveFiles": False,
        "saveScreenshots": False,
        "maxResults": 100,
        "clientSideMinChangePercentage": 15,
        "renderingTypeDetectionPercentage": 10,
        "keywords": keywords,  # Add the keywords to the input
        "customDataFunction": """
    async ({ page, request }) => {
        const keywords = request.userData.keywords;
        // Check if the page contains any of the keywords
        const content = await page.content();
        for (const keyword of keywords) {
            if (content.toLowerCase().includes(keyword.toLowerCase())) {
                return { url: request.url, content };
            }
        }
        return null;
    }
    """
    }

    # Add keywords to the userData field for each start URL
    for startUrl in run_input["startUrls"]:
        startUrl["userData"] = { "keywords": keywords }

    # Run the Actor and wait for it to finish
    run = client.actor("aYG0l9s7dbB7j3gbS").call(run_input=run_input)

    # Fetch and return Actor results from the run's dataset
    results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        results.append(item)

    return results
