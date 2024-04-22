# LSlackBot
The script has been tested and developed to run on a raspberry pi model 4B, but should run on any device capable of handling the chromium web browser. It scrapes a website for listings that meet defined criteria and forwards them to a slack channel, when configured as a slack app with the incoming-webhook scope enabled.

If you cloned the repo you can install all required dependencies with `pip install -r requirements.txt` (except for chrome webdriver and python, you can use any corresponding packages that are the most convenient for those) Chrome webdriver can be installed from https://sites.google.com/chromium.org/driver/.

Remember to scrape responsibly and to check /robots.txt of any site you intend to scrape before initiating a scraping script.

![image](https://github.com/osemo-hb/LSlackBot/assets/77531741/d26406f3-fb2c-48d1-9fb7-a08fa88b2585)
