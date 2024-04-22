# LSlackBot
The script has been tested and developed to run on a raspberry pi model 4B, but should run on any device capable of handling the chromium web browser. It scrapes a website for listings that meet defined criteria and forwards them to a slack channel, when configured as a slack app with the incoming-webhook scope enabled.

If you cloned the repo you can install all required dependencies with 
pip install -r requirements.txt 
(except for chrome webdriver and python, you can use any corresponding packages that is most convenient)

Remember to scrape responsibly and to check /robots.txt of any site you intend to scrape before initiating a scraping script.