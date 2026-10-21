import scrapy

from books_scraper.items import BookItem
from books_scraper.loaders import BookLoader


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["www.gutenberg.org"]
    start_urls = ["https://www.gutenberg.org/ebooks/bookshelf/645"]

    def parse(self, response):
        for href in response.css("li.booklink a.link::attr(href)").getall():
            yield response.follow(href, callback=self.parse_book)

        next_page = response.css('a[title*="next page"]::attr(href)').get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def parse_book(self, response):
        loader = BookLoader(item=BookItem(), response=response)
        loader.add_css("title", 'td[itemprop="headline"]::text')
        loader.add_css("price", 'meta[itemprop="price"]::attr(content)')
        loader.add_css("availability", 'link[itemprop="availability"]::attr(href)')
        loader.add_css("category", 'a.similar-books-tag[href*="bookshelf"]::text')
        loader.add_css("downloads", 'td[itemprop="interactionCount"]::text')
        loader.add_xpath("book_id", '//th[text()="eBook-No."]/following-sibling::td/text()')
        loader.add_value("url", response.url)
        yield loader.load_item()
