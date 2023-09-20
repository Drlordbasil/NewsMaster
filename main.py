import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import telegram
import time


# Define WebScraper class to scrape articles from a website
class WebScraper:
    def __init__(self):
        self.base_url = 'https://newswebsite.com'
        self.articles = []

    def scrape_articles(self):
        html = requests.get(self.base_url)
        soup = BeautifulSoup(html.content, 'html.parser')
        news_items = soup.find_all('div', class_='news-item')
        for item in news_items:
            title = item.find('h2').text
            content = item.find('p').text
            link = item.find('a')['href']
            article = Article(title, content, link)
            self.articles.append(article)


# Define Article class to represent a news article
class Article:
    def __init__(self, title, content, link):
        self.title = title
        self.content = content
        self.link = link


# Define TextProcessor class to preprocess text
class TextProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def preprocess_text(self, text):
        tokens = word_tokenize(text.lower())
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token.isalpha()]
        tokens = [token for token in tokens if token not in self.stop_words]
        return " ".join(tokens)


# Define ContentAnalyzer class to analyze article content
class ContentAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def analyze_content(self, articles):
        content = [article.content for article in articles]
        features = self.vectorizer.fit_transform(content)
        return features 


# Define NewsCategorizer class to categorize news articles
class NewsCategorizer:
    def __init__(self):
        self.svm = SVC()

    def categorize_news(self, features):
        X_train = features[:-1]
        y_train = [article.category for article in features[:-1]]

        self.svm.fit(X_train, y_train)

    def predict_category(self, features):
        X_test = features[-1]
        prediction = self.svm.predict(X_test)
        return prediction


# Define User class to represent a user with preferences
class User:
    def __init__(self, name):
        self.name = name
        self.preferences = []

    def set_preferences(self, preferences):
        self.preferences = preferences

    def get_preferences(self):
        return self.preferences


# Define NewsAggregator class to aggregate news for users
class NewsAggregator:
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def recommend_news(self, user, articles):
        preferences = user.get_preferences()
        relevant_articles = [article for article in articles if any(pref in article.categories for pref in preferences)]
        return relevant_articles


# Define TelegramBot class to interact with the Telegram bot
class TelegramBot:
    def __init__(self, token):
        self.bot = telegram.Bot(token)

    def start(self):
        self.bot.send_message(chat_id='user_id', text='Welcome to the News Aggregator bot!')

    def send_news(self, user, articles):
        user_id = user.id
        for article in articles:
            message = f'{article.title}\n\n{article.content}\n\nRead more: {article.link}'
            self.bot.send_message(chat_id=user_id, text=message)
            time.sleep(1)


def main():
    web_scraper = WebScraper()
    web_scraper.scrape_articles()

    text_processor = TextProcessor()
    for article in web_scraper.articles:
        article.content = text_processor.preprocess_text(article.content)

    content_analyzer = ContentAnalyzer()
    features = content_analyzer.analyze_content(web_scraper.articles)

    news_categorizer = NewsCategorizer()
    news_categorizer.categorize_news(features)

    news_aggregator = NewsAggregator()

    user1 = User('Alice')
    user1.set_preferences(['technology', 'business'])
    news_aggregator.add_user(user1)

    user2 = User('Bob')
    user2.set_preferences(['sports', 'politics'])
    news_aggregator.add_user(user2)

    relevant_articles = news_aggregator.recommend_news(user1, web_scraper.articles)

    telegram_bot = TelegramBot('YOUR_TELEGRAM_BOT_TOKEN')
    telegram_bot.start()
    telegram_bot.send_news(user1, relevant_articles)


if __name__ == '__main__':
    main()