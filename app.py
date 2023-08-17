from flask import Flask,render_template
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import io
import nltk
from PIL import Image
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
nltk.download('punkt')

app=Flask('__name__')


#FUCTION FOR FETCHING THE TRENDING NEWS
def fetch_top_news():
    site = 'https://news.google.com/news/rss'
    op = urlopen(site)
    rd = op.read()
    op.close()
    sp_page = soup(rd, 'xml')
    news_list = sp_page.find_all('item')
    return news_list

#FUNTION FOR FETCHING NEWS FROM URL
def summarize_article_from_url(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        original_title = article.title
        article_content = article.text
        parser = PlaintextParser.from_string(article_content, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary_sentences = summarizer(parser.document, 3)
        summary = " ".join([str(sentence) for sentence in summary_sentences])
        return original_title, summary
    except Exception as e:
        print("Error summarizing the article:", str(e))
        return None, None




#FUCTION FOR RETURN THE NEWS DAT
def fetch_news_data(list_of_news,news_quantity):
   
    news_quantity = 5  # Example value

    news_list = []
    c=0

    for c, news in enumerate(list_of_news, start=1):
        if c > news_quantity:
            break

        news_data = Article(news.link.text)
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception as e:
            print("Error:", e)
            continue

        news_info = {
            'index': c,
            'title': news.title.text,
            'summary': news_data.summary,
            'source': news.source.text,
            'link': news.link.text,
            'published_date': news.pubDate.text,
          
        }
        news_list.append(news_info)

    return news_list



#ROOT FUCTIONS

@app.route('/')
def root():
    return render_template('root.html')

@app.route('/home')
def home1():
    news_list=fetch_top_news()
    news_list=fetch_news_data(news_list,5)
    return render_template('home.html',news_list=news_list)

if __name__=='__main__':
    app.run(debug=True)