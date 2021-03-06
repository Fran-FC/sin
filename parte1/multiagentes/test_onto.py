from hashlib import new
from agent2 import Onto, NewsScrapper
import sys

onto_url = str(sys.argv[1])
news_url = str(sys.argv[2])

news_scrapper = NewsScrapper(news_url)

# news_scrapper.list_keys()

# news_scrapper.list_titles()

keyword = "valencia"
feed = news_scrapper.search_from_titles(keyword)
# news_scrapper.search_from_titles("Ucrania")

onto = Onto(onto_url)
onto.add_instance(keyword, feed)

# print("\nInstances:")
# onto.list_instances()
