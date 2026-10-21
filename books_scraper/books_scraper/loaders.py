import re

from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose

def clean_text(value):
  return value.strip()

def clean_price(value):
  return float(value)

def clean_availability(value):
  return value.rstrip("/").split("/")[-1]

def clean_number(value):
  return int(re.search(r"\d+", value).group())

class BookLoader(ItemLoader):
  default_output_processor = TakeFirst()

  title_in = MapCompose(clean_text)
  price_in = MapCompose(clean_price)
  category_in = MapCompose(clean_text)
  availability_in = MapCompose(clean_availability)
  downloads_in = MapCompose(clean_number)
  book_id_in = MapCompose(clean_number)
