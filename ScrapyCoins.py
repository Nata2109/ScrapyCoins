import requests
from bs4 import BeautifulSoup
import sqlite3
from CoinInfo import CoinInfo

# Method to Scrape Coin Data From Search Result Pages
def scrapeData(webpageToScrape):

    coinInfos = []

    # WebPages of coin search results
    webpage_response = requests.get(webpageToScrape)

    webpage = webpage_response.content
    soup = BeautifulSoup(webpage, "html.parser")

    # Go through each coin in the webpage
    for div in soup.select(".divCoinBackground"):
        # Coin Name
        coinName = div.find('a')['title']

        # Coin Img Small
        coinImgUrlSmall = "https://www.changechecker.org" + div.find('img')['src']

        # Coin info page URL
        coinInfoURL = "https://www.changechecker.org/" + div.find('a')['href']

        # Soup the URL
        webpageInfo_response = requests.get(coinInfoURL)

        infoWebpage = webpageInfo_response.content
        infoSoup = BeautifulSoup(infoWebpage, "html.parser")

        # Coin details Page
        # Value
        try:
            fullDescriptor = infoSoup.body.find('span', attrs={'id' : 'ContentPlaceHolderBodyText_ctl00_coin-details_1_lblCoinTitle'}).text
            value = fullDescriptor.split(':')[0]
        except:
            value = "Unknown"

        # Years of Issue
        yearsOfIssue = infoSoup.body.find('span', attrs={'id' : 'ContentPlaceHolderBodyText_ctl00_coin-details_1_lbl_years'}).text

        # Coin Info Para
        coinInfo = infoSoup.body.find('span', attrs={'id' : 'ContentPlaceHolderBodyText_ctl00_coin-details_1_lbl_information'}).text

        # Coin Img Large
        coinImgUrlLarge = "https://www.changechecker.org/" + infoSoup.body.find('img', attrs={'id' : 'ContentPlaceHolderBodyText_ctl00_coin-details_1_CoinImage'})['src']

        coinInfos.append(CoinInfo(coinName, value, yearsOfIssue, coinInfo, coinImgUrlSmall, coinImgUrlLarge))

        # Can be removed but useful to know where the program is at
        print(coinName)

    return coinInfos

# There are no commeriative designs of the new £1 coin so search results go straight to the coins info page
def new1PoundScrape():
    # Own Logic for New £1 Coin
    new1Webpage_response = requests.get('https://www.changechecker.org/coin/187/1pound-UK-Nations-of-the-Crown.aspx')
    new1Webpage = new1Webpage_response.content
    new1Soup = BeautifulSoup(new1Webpage, "html.parser")

    coinTitle = new1Soup.body.find('span', attrs={'id' : 'ContentPlaceHolderBodyText_ctl00_coin-details_1_lblCoinTitle'}).text
    # Coin Name
    coinName = coinTitle.split(":")[1]+ coinTitle.split(":")[2]

    # Coin Value
    coinValue = "1"

    # Coin Years of Issue
    yearsOfIssue = new1Soup.body.find('span', attrs={'id' : 'ContentPlaceHolderBodyText_ctl00_coin-details_1_lbl_years'}).text

    # Coin Info Para
    coinInfo = new1Soup.body.find('span', attrs={'id' : 'ContentPlaceHolderBodyText_ctl00_coin-details_1_lbl_information'}).text

    # Coin Img Large
    coinImgUrlLarge = "https://www.changechecker.org/" + new1Soup.body.find('img', attrs={'id' : 'ContentPlaceHolderBodyText_ctl00_coin-details_1_CoinImage'})['src']

    return CoinInfo(coinName, coinValue, yearsOfIssue, coinInfo, "", coinImgUrlLarge)


# Webpages to be scraped
webpagesToScrape = ['https://www.changechecker.org/search-results.aspx?denominationId=16&subcategory=Definitive&subcategoryId=1020',
                    'https://www.changechecker.org/search-results.aspx?denominationId=1&subcategory=Year&subcategoryId=1000',
                    'https://www.changechecker.org/search-results.aspx?denominationId=3&subcategory=Year&subcategoryId=1000',
                    'https://www.changechecker.org/search-results.aspx?denominationId=4&subcategory=Sport&subcategoryId=1010',
                    'https://www.changechecker.org/search-results.aspx?denominationId=4&subcategory=Sport&subcategoryId=1010',
                    'https://www.changechecker.org/search-results.aspx?denominationId=7&subcategory=Year&subcategoryId=1000',
                    'https://www.changechecker.org/search-results.aspx?denominationId=5&subcategory=Year&subcategoryId=1000',
                    'https://www.changechecker.org/search-results.aspx?denominationId=2&subcategory=Year&subcategoryId=1000',
                    'https://www.changechecker.org/search-results.aspx?denominationId=6&subcategory=Year&subcategoryId=1000',
                    'https://www.changechecker.org/search-results.aspx?denominationId=8&subcategory=Year&subcategoryId=1000'
                    ]

# Connect to DB and store scraped values
# This will only work when populating an empty DB
i = 0
conn = sqlite3.connect('CoinsDB.db')
c = conn.cursor()
coinData = []

# Create Tuple of all data to insert
for webpage in webpagesToScrape:
    # Scrape Data
    allCoins = scrapeData(webpage)

    for coin in allCoins:
        coinData.append((i, coin.Name, coin.Value, coin.YearsOfIssue, coin.Description, coin.SmallImgLoc, coin.LargeImgLoc))
        i = i + 1

new1PoundCoin = new1PoundScrape()
coinData.append((i, new1PoundCoin.Name, new1PoundCoin.Value, new1PoundCoin.YearsOfIssue, new1PoundCoin.Description, new1PoundCoin.SmallImgLoc, new1PoundCoin.LargeImgLoc))

# Execute single SQL Query
sqlStatement = "INSERT INTO Coins(Coin_Id, Name, Value, Years_Of_Issue, Description, Small_Img_Url, Large_Img_Url) VALUES(?,?,?,?,?,?,?);"
c.executemany(sqlStatement, coinData)
print('We have inserted', c.rowcount, 'records to the table.')
conn.commit()

# Close the connection
conn.close()


