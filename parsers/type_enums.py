from dataclasses import dataclass, fields
from typing import Optional


class Attrs:
    HREF = "href"
    SRC = "src"
    DATETIME = "datetime"


class Tags:
    TIME = "time"
    P = "p"


@dataclass
class ArticleStats:
    votes: str
    views: str
    bookmarks: str
    comments: str


@dataclass
class Article:
    author: str
    author_link: str
    publish_date: str
    publish_date_text: str
    title: str
    title_link: str
    description: str
    tags: list[dict[str, str]]
    stats: ArticleStats
    theme: Optional[str]


ARTICLE_FIELD_NAMES = [field.name for field in fields(Article)]


class ArticleClasses:
    # Common fields
    ARTICLE = "tm-articles-list__item"
    AUTHOR = "tm-user-info__username"
    PUBLISH_DATE = "tm-article-snippet__datetime-published"
    TITLE = "tm-article-snippet__title-link"
    TAG = "tm-article-snippet__hubs-item-link"
    IMAGE = "tm-article-snippet__lead-image"
    DESCRIPTION = "article-formatted-body"
    STATS = "tm-data-icons"

    # For stats
    VOTES_COUNTER = "tm-votes-meter"
    VIEWS_COUNTER = "tm-icon-counter__value"
    BOOKMARKS_COUNTER = "bookmarks-button__counter"
    COMMENTS_COUNTER = "tm-article-comments-counter-link__value"
