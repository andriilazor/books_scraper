# Books Scraper

A simple [Scrapy](https://scrapy.org/) scraper that collects book data from [Project Gutenberg](https://www.gutenberg.org/ebooks/bookshelf/645) (bookshelf #645).

## Scraped fields

| Field          | Description                                         |
|----------------|-----------------------------------------------------|
| `book_id`      | Gutenberg eBook number                              |
| `title`        | book title                                          |
| `category`     | category (bookshelf)                                |
| `price`        | price (always `0.0` on Gutenberg)                   |
| `availability` | availability (`In Stock`)                           |
| `downloads`    | number of downloads                                 |
| `rating`       | 1–5 score derived from the number of downloads      |
| `url`          | link to the book page                               |

`rating` thresholds: ≥10000 downloads → 5, ≥5000 → 4, ≥1000 → 3, ≥100 → 2, otherwise → 1.

## Project structure

```
books_scraper/
├── scrapy.cfg
├── out.json                    # sample output
└── books_scraper/
    ├── spiders/books.py        # spider: crawls the book list and book pages
    ├── items.py                # BookItem field definitions
    ├── loaders.py              # value cleaning (ItemLoader)
    ├── pipelines.py            # validation, deduplication, transformation
    └── settings.py             # Scrapy settings
```

Pipelines run in this order:

1. `ValidationPipeline` drops items with missing required fields or an invalid price.
2. `DuplicatePipeline` drops duplicates by `book_id`.
3. `TransformationPipeline` normalizes title, category and availability, and computes `rating`.

## Usage

```bash
# create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install dependencies
pip install scrapy

# run the spider and save results to JSON
cd books_scraper
scrapy crawl books -O out.json
```

## Settings

Defaults in `settings.py`:

- `CLOSESPIDER_ITEMCOUNT = 120`: stop after 120 books.
- `DOWNLOAD_DELAY = 1` and `CONCURRENT_REQUESTS_PER_DOMAIN = 1`: keep the load on the site low.
- `ROBOTSTXT_OBEY = True`: respect `robots.txt`.
