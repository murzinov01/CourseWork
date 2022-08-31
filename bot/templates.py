from jinja2 import Environment, PackageLoader, select_autoescape
ENV = Environment(
    loader=PackageLoader('bot', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def construct_article_from_template(article: dict) -> str:
    template = ENV.get_template('article.html')
    return template.render(article)
