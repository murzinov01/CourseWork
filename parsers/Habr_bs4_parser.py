import json
from dataclasses import asdict
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
import requests as req
from http import HTTPStatus

from parsers.type_enums import Article, ArticleClasses, ArticleStats


class HabrBS4Parser:
    def init(self):
        pass

    @staticmethod
    def parse_article_stats(article) -> ArticleStats:
        article_stats = article.find("div", class_=ArticleClasses.STATS)
        votes = article_stats.find("span", class_=ArticleClasses.VOTES_COUNTER)
        views = article_stats.find("span", class_=ArticleClasses.VIEWS_COUNTER)
        bookmarks = article_stats.find("span", class_=ArticleClasses.BOOKMARKS_COUNTER)
        comments = article_stats.find("span", class_=ArticleClasses.COMMENTS_COUNTER)
        return ArticleStats(
            votes=votes.text.strip(),
            views=views.text.strip(),
            bookmarks=bookmarks.text.strip(),
            comments=comments.text.strip(),
        )

    def parse_article(self, article, theme: str = None) -> Article:
        author = article.find("a", class_=ArticleClasses.AUTHOR)
        publish_date = article.find("span", class_=ArticleClasses.PUBLISH_DATE)
        title = article.find("a", class_=ArticleClasses.TITLE)

        resp = req.get(f"https://habr.com{title['href']}")
        if resp.status_code == HTTPStatus.OK:
            article_html = resp.text
        else:
            article_html = None

        soup = BeautifulSoup(article_html, "html.parser")
        tags = soup.findAll("a", class_=ArticleClasses.TAG)
        description = soup.find("div", class_=ArticleClasses.DESCRIPTION).find("p")
        return Article(
            author=author.text.strip(),
            author_link=f"https://habr.com{author['href']}",
            publish_date=publish_date.find("time")["datetime"],
            publish_date_text=publish_date.text.strip(),
            title=title.text.strip(),
            title_link=f"https://habr.com{title['href']}",
            description=description,
            tags=[
                {
                    "tag": tag.text.strip(" \n\t,.*"),
                    "link": tag['href'],
                }
                for tag in tags
            ],
            stats=self.parse_article_stats(article),
            theme=theme,
        )

    def parse_page(self, html_data: str, for_minutes: int = None, theme: str = None) -> list[Article]:
        # print(html_data)
        soup = BeautifulSoup(html_data, "html.parser")
        articles_on_page = soup.findAll("article", class_=ArticleClasses.ARTICLE)

        articles_data = []
        # parse page
        for article in articles_on_page:
            #try:
            article_info = self.parse_article(article, theme)
            print(json.dumps(asdict(article_info), indent=4))
            if for_minutes is not None:
                published_date = article_info.publish_date
                if datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%S.000Z") < datetime.utcnow() - timedelta(
                    minutes=for_minutes
                ):
                    break
            articles_data.append(article_info)
            # except Exception:
            #     continue
        return articles_data

    def find_newest_articles(self, for_minutes: int = None) -> list[Article]:
        newest_articles = []
        seen_titles = set()
        for theme in ("develop", "admin", "design", "management", "marketing", "popsci"):
            response = req.get(f"https://habr.com/ru/flows/{theme}")
            if response.status_code == HTTPStatus.OK:
                resp_html = response.text
                articles_data = self.parse_page(resp_html, for_minutes=for_minutes, theme=theme)
                for article in articles_data:
                    if article.title in seen_titles:
                        continue
                    seen_titles.add(article.title)
                    newest_articles.append(article)
        return newest_articles


def main():
    habr_parser = HabrBS4Parser()
    articles = habr_parser.find_newest_articles()
    for article in articles:
        print(json.dumps(asdict(article), indent=4))


if __name__ == "__main__":
    main()
