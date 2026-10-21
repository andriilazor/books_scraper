from scrapy.exceptions import DropItem


class ValidationPipeline:
    required_fields = ["title", "price", "category", "availability", "book_id"]

    def process_item(self, item):
        for field in self.required_fields:
            if item.get(field) in (None, ""):
                raise DropItem(f"Missing field '{field}': {item.get('url')}")

        if not isinstance(item["price"], (int, float)) or item["price"] < 0:
            raise DropItem(f"Invalid price {item['price']!r}: {item.get('url')}")

        return item


class DuplicatePipeline:
    def __init__(self):
        self.seen_ids = set()

    def process_item(self, item):
        if item["book_id"] in self.seen_ids:
            raise DropItem(f"Duplicate book {item['book_id']}")
        self.seen_ids.add(item["book_id"])
        return item


class TransformationPipeline:
    def process_item(self, item):
        item["title"] = " ".join(item["title"].split())
        item["category"] = item["category"].replace("(Bookshelf)", "").strip()
        item["availability"] = "In Stock" if item["availability"] == "InStock" else item["availability"]

        downloads = item.get("downloads") or 0
        if downloads >= 10000:
            item["rating"] = 5
        elif downloads >= 5000:
            item["rating"] = 4
        elif downloads >= 1000:
            item["rating"] = 3
        elif downloads >= 100:
            item["rating"] = 2
        else:
            item["rating"] = 1

        return item
