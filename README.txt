# What is it?

Here is a script I used to scrape new reviews from trip-hop.net and post
them to Twitter or post them by email. This version is a subset of a
larger scraper operating on other sites than trip-hop.net, which
explains the apparent useless complexity. BeautifulSoup and tweepy
dependencies are vendored with the script for simplicity.

# Scraping

First create a webupdates.cfg configuration file next to fetch.py. You
only need to fill the [twitter] section for tweeter updates. See
webupdates.cfg.templ for a sample file.

Then execute it like:

```sh
python fetch.py seen.txt
```

The `seen.txt` file must be read/writable. It is a line-based list of
the individual reviews already processed by the script. These entries
are ignored by the script. Missing entries will be processed and
appended to the file.

Put the call above in a cron task and you are done.


