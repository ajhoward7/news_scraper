# News Scraping

Within this repo we provide two key methods for scraping current news data from online sources:

1. Twitter - user can enter a number of twitter handles (along with their Twitter API authentication)
2. RSS feeds - the URLs for RSS feeds can be provided and key details about the constituent articles is scraped.

Note: Twitter imposes rate limits on individuals that reset every 15 minutes - specific information available [here](https://developer.twitter.com/en/docs/basics/rate-limiting).

## Setup:
- This code is designed to be run with Python 2 from the Command Line
- To run the Twitter API scrape you require to pass credentials as a command line argument, the twitter credentials should be stored in a CSV as described [here](https://github.com/parrt/msan692/blob/master/hw/sentiment.md) under *Discussion* section.
- Custom configurations should be set within the appropriate `confs.yaml` file (a list of RSS URLs in `conf/confs.rss.yaml`, a list of Twitter user handles in `conf/confs.twitter.yaml` and a number `n` of most recent tweets to fetch for each user).

## Running Code:

**Twitter:**

`! python twitter_scrape.py <twitter credentials csv path>`

**RSS:**

`! python rss_scraper.py`

## Output:
- The output from both scripts is very similar in structure - a dictionary of the inputs (tweets / rss urls) mapped to a list of the outputs. In each case this output is itself formatted a list of dictionaries, each dictionary contains the information on one tweet/article for a particular user.
- Output is automatically written to `output.json`, this can optionally be changed with an additional command line argument
- `sample_output_digest.py` provides sample code for reading this `.json` file back into Python and a template for printing a human-readable format.

-----

Credit to [Terence Parr](https://github.com/parrt) for his existing Twitter API functionality.
