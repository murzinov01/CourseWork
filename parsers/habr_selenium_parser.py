import os
from csv import DictWriter
from dataclasses import asdict
from datetime import datetime, timedelta
from typing import Union

from pymongo import MongoClient, UpdateOne
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

import config
from parsers.type_enums import Article, ARTICLE_FIELD_NAMES, ArticleStats, Attrs, Tags, ArticleClasses


class HabrSeleniumParser:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    @staticmethod
    def get_attribute(elem, attr_name):
        try:
            return elem.get_attribute(attr_name)
        except NoSuchElementException:
            return None

    @staticmethod
    def save_data(data: Union[Article, list[Article]], file_name="article.csv") -> None:
        with open(file_name, "a+", encoding="utf-8") as articles_file:
            writer = DictWriter(articles_file, fieldnames=ARTICLE_FIELD_NAMES)
            if os.stat(file_name).st_size == 0:
                writer.writeheader()
            if isinstance(data, Article):
                writer.writerow(asdict(data))
            elif isinstance(data, list):
                writer.writerows((asdict(entry) for entry in data))
            else:
                raise TypeError

    @staticmethod
    def update_data(
        data: Union[Article, list[Article]],
        url=config.MONGO_URL,
        database=config.DATABASE,
        collection=config.HABR_ARTICLES_COLL,
    ):
        client = MongoClient(url)
        articles_db = client[database]
        habr_collection = articles_db[collection]
        if isinstance(data, Article):
            entry = asdict(data)
            habr_collection.update_one(
                {"author": entry["author"], "title": entry["title"]},
                {"$set": entry},
                upsert=True,
            )
        elif isinstance(data, list):
            ops = []
            for entry in data:
                entry = asdict(entry)
                ops.append(
                    UpdateOne(
                        {"author": entry["author"], "title": entry["title"]},
                        {"$set": entry},
                        upsert=True,
                    )
                )
            habr_collection.bulk_write(ops)
        else:
            raise TypeError

    @staticmethod
    def parse_article_stats(article) -> ArticleStats:
        article_stats = article.find_element(By.CLASS_NAME, ArticleClasses.STATS)
        votes = article_stats.find_element(By.CLASS_NAME, ArticleClasses.VOTES_COUNTER)
        views = article_stats.find_element(By.CLASS_NAME, ArticleClasses.VIEWS_COUNTER)
        bookmarks = article_stats.find_element(By.CLASS_NAME, ArticleClasses.BOOKMARKS_COUNTER)
        comments = article_stats.find_element(By.CLASS_NAME, ArticleClasses.COMMENTS_COUNTER)
        return ArticleStats(
            votes=votes.text,
            views=views.text,
            bookmarks=bookmarks.text,
            comments=comments.text,
        )

    def parse_article(self, article, theme: str = None) -> Article:
        author = article.find_element(By.CLASS_NAME, ArticleClasses.AUTHOR)
        publish_date = article.find_element(By.CLASS_NAME, ArticleClasses.PUBLISH_DATE)
        title = article.find_element(By.CLASS_NAME, ArticleClasses.TITLE)
        tags = article.find_elements(By.CLASS_NAME, ArticleClasses.TAG)
        description = article.find_element(By.CLASS_NAME, ArticleClasses.DESCRIPTION)

        return Article(
            author=author.text,
            author_link=author.get_attribute(Attrs.HREF),
            publish_date=publish_date.find_element(By.TAG_NAME, Tags.TIME).get_attribute(Attrs.DATETIME),
            publish_date_text=publish_date.text,
            title=title.text,
            title_link=title.get_attribute(Attrs.HREF),
            description="\n\n".join((paragraph.text for paragraph in description.find_elements(By.TAG_NAME, Tags.P))),
            tags=[
                {
                    "tag": tag.text.strip(" \n\t,.*"),
                    "link": tag.get_attribute(Attrs.HREF),
                }
                for tag in tags
            ],
            stats=self.parse_article_stats(article),
            theme=theme,
        )

    def save(self, articles_data: Union[Article, list[Article]], save_method="db"):
        if not articles_data:
            return
        if save_method == "db":
            self.update_data(articles_data)
        elif save_method == "file":
            self.save_data(articles_data)
        else:
            raise ValueError

    def search(self, search_query: str, page=1) -> list[Article]:
        search_query = search_query.replace(" ", "%20")
        self.driver.get(f"https://habr.com/ru/search/page{page}/?q={search_query}&target_type=posts&order=relevance")
        articles_data = self.parse_page()
        return articles_data

    def parse_page(self, for_minutes: int = None, theme: str = None) -> list[Article]:
        articles_on_page = self.driver.find_elements(By.CLASS_NAME, ArticleClasses.ARTICLE)
        articles_data = []

        # parse page
        for article in articles_on_page:
            try:
                article_info = self.parse_article(article, theme)
                if for_minutes is not None:
                    published_date = article_info.publish_date
                    if datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%S.000Z") < datetime.utcnow() - timedelta(
                        minutes=for_minutes
                    ):
                        break
                articles_data.append(article_info)
            except NoSuchElementException:
                continue
        return articles_data

    def parse(self, page_num=50, url=None):
        if url is not None:
            self.driver.get(f"{url}")
            articles_data = self.parse_page()
            self.save(articles_data)
        else:
            for page in tqdm(range(1, page_num + 1)):
                self.driver.get(f"{config.HABR_URL}/page{page}")
                articles_data = self.parse_page()
                self.save(articles_data)

    def find_newest_articles(self, for_minutes: int) -> list[Article]:
        newest_articles = []
        seen_titles = set()
        for theme in ("develop", "admin", "design", "management", "marketing", "popsci"):
            self.driver.get(f"https://habr.com/ru/flows/{theme}")
            articles_data = self.parse_page(for_minutes=for_minutes, theme=theme)
            for article in articles_data:
                if article.title in seen_titles:
                    continue
                seen_titles.add(article.title)
                newest_articles.append(article)
        return newest_articles

    def update(self, page_num=50, days_n=1):
        for page in tqdm(range(1, page_num + 1)):
            # open page
            self.driver.get(f"{config.HABR_URL}/page{page}")

            articles_on_page = self.driver.find_elements(By.CLASS_NAME, ArticleClasses.ARTICLE)
            articles_data = []

            # parse page
            for article in articles_on_page:
                try:
                    article_info = self.parse_article(article)
                    publish_date = article_info.publish_date
                    publish_date = publish_date.replace(".000Z", "")
                    time_now = datetime.now()

                    if time_now - timedelta(days=days_n) < datetime.fromisoformat(publish_date):
                        articles_data.append(article_info)
                    else:
                        print("There is no new articles. Finish...")
                        self.save(articles_data)
                        return
                except NoSuchElementException:
                    continue
            self.save(articles_data)


def main():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    habr_parser = HabrSeleniumParser(driver)
    habr_parser.parse(page_num=474)


if __name__ == "__main__":
    main()
