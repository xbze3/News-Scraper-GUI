from flask import Flask
from flask_restful import Api, Resource
import requests
import re
from bs4 import BeautifulSoup

app = Flask(__name__)
api = Api(app)

class getRequest(Resource):

    def get(self, searchTerm):
        processedData = self.getNews(searchTerm)
        return {
            "searchTerm": searchTerm,
            "processedData": processedData
        }
    
    def getNews(self, searchTerm):

        bloomberg = self.getBloomberg(searchTerm)
        investing = self.getInvesting(searchTerm)
        news = bloomberg + investing

        return news
    
    def getBloomberg(self, searchTerm):

        newsArray = []

        userInput = searchTerm.replace(" ", "%20")
        headers = {'User-Agent': 'Mozilla/5.0'}

        URL = f"https://www.bloomberg.com/search?query={userInput}"
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")

        img = [img['src'] for img in soup.find_all('img', class_=lambda x: x and re.search(r'thumbnail', x), src=True)]
        headlineData = [x.get_text() for x in soup.find_all('a', attrs={'class': lambda x: x and re.compile(r'^headline').match(x)})]
        link = [a['href'] for a in soup.find_all('a', class_= lambda x: x and re.compile(r'^headline').match(x), href=True) if a.text]

        for i in range(0, len(link)):
            case = {"Image": img[i], "Headline": headlineData[i], "Link": link[i]}
            newsArray.append(case)



        return newsArray
    
    def getInvesting(self, searchTerm):

            newsArray = []

            userInput = searchTerm.replace(" ", "%20")
            headers = {'User-Agent': 'Mozilla/5.0'}

            URL = f"https://www.investing.com/search/?q={userInput}&tab=news"
            page = requests.get(URL, headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")

            img = "https://th.bing.com/th/id/OIP.48FWT7d2HaEMDm06-PrJTAHaE2?rs=1&pid=ImgDetMain"
            headlineData = [x.get_text() for x in soup.find_all('a', attrs={'class': 'title'})]
            link = [a['href'] for a in soup.find_all('a', class_= 'title', href=True) if a.text]

            for i in range(0, (len(headlineData) - 3)):
                case = {"Image": img, "Headline": headlineData[i], "Link": "https://www.investing.com"+link[i]}
                newsArray.append(case)

            return newsArray

api.add_resource(getRequest, "/getNews/<string:searchTerm>")

if __name__ == "__main__":
    app.run(debug=True)