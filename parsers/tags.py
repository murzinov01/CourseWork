from pymongo import MongoClient, InsertOne
from collections import defaultdict

import config


def collect_unique_tags():
    client = MongoClient(config.MONGO_URL)
    db = client[config.DATABASE]
    habr_articles_coll = db[config.HABR_ARTICLES_COLL]
    tags_coll = db[config.TAGS_COLL]

    unique_tags = defaultdict(int)

    for entry in habr_articles_coll.find({}, projection={"tags": 1}):
        tags = entry.get("tags", [])
        for tag in tags:
            tag_name = tag.get("tag")
            if tag_name:
                unique_tags[tag_name] += 1

    unique_tags_sorted = [k for k, v in sorted(unique_tags.items(), key=lambda item: item[1], reverse=True)]
    print("Unique tags num: ", len(unique_tags_sorted))
    tags_coll.bulk_write([InsertOne({"tag": tag}) for tag in unique_tags_sorted], ordered=True)


def main():
    collect_unique_tags()


if __name__ == '__main__':
    main()
