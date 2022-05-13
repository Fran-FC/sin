import time
import json
import feedparser
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from owlready2 import *


class Onto:
    def __init__(self, onto_url, onto_dir):
        self.onto_url_ = onto_url
        self.onto_local_dir_ = onto_dir
        self.onto_ = get_ontology(self.onto_url_)
        self.onto_.load()
        # print(self.onto_.base_iri)

    def get_iri(self):
        return self.onto_.base_iri

    def list_classes(self):
        for onto_class in self.onto_.classes():
            print("Class: {}".format(onto_class))
            for subclass in onto_class.subclasses():
                print("\tSubclass: {}".format(subclass))

    def list_instances(self):
        for onto_individual in self.onto_.individuals():
            print(onto_individual)
            for prop in onto_individual.get_properties():
                for val in prop[onto_individual]:
                    print("\t%s := %s" % (prop.python_name, val))

    def instance_to_str(self, individual):
        res = {}
        for prop in individual.get_properties():
            for val in prop[individual]:
                res[prop.python_name] = val
                # res += "%s := %s\n" % (prop.python_name, val)
        return res

    def add_property(self, property, value):
        try:
            property.append(value)
        except:
            return

    def add_instance(self, keyword, feed_dict):
        article = self.onto_.Article(keyword)
        self.add_property(article.url, feed_dict.link)
        self.add_property(article.datePublished, feed_dict.published)
        self.add_property(article.headline, feed_dict.title)
        try:  # some articles haven't got body
            for content in feed_dict.content:
                if content.value != feed_dict.title:
                    self.add_property(
                        article.articleBody, content.value)
        except AttributeError:
            pass
        self.onto_.save(self.onto_local_dir_)

        return article


class NewsScrapper:
    def __init__(self, url):
        self.news_feed_ = feedparser.parse(url)

    # source: https://stackoverflow.com/questions/2460177/edit-distance-in-python
    def __levenshtein_distance(self, s1, s2):
        if len(s1) > len(s2):
            s1, s2 = s2, s1
        distances = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            distances_ = [i2+1]
            for i1, c1 in enumerate(s1):
                if c1 == c2:
                    distances_.append(distances[i1])
                else:
                    distances_.append(
                        1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
            distances = distances_
        return distances[-1]

    def list_keys(self):
        print(self.news_feed_.entries[0].keys())

    def list_titles(self):
        for entry in self.news_feed_.entries:
            print(entry.title)

    def search_from_titles(self, substr_title):
        substr_title = substr_title.lower()
        distance = 9000
        for entry in self.news_feed_.entries:
            title = entry.title.lower()
            if substr_title in title:
                self.entry_ = entry
                break
            # if there's not exact match, keep the entry with minimum manhatan distance
            else:
                aux = 0
                i = 0
                for word in title.split(" "):
                    aux = aux + self.__levenshtein_distance(substr_title, word)
                    i += 1
                aux /= i
                if aux < distance:
                    distance = aux
                    self.entry_ = entry
        print("\nBest entry: %s" % self.entry_.title)
        return self.entry_

    def get_title(self):
        return self.entry_.title


class ReceiverAgent(Agent):
    class RecvBehav(OneShotBehaviour):
        def __init__(self):
            super().__init__()
            # self.ontology_url_ = "ontologies/rnews.owl"
            self.ontology_url_ = "http://dev.iptc.org/files/rNews/rnews_1.0_draft3_rdfxml.owl"
            self.ontology_dir_ = "rnews.owl"
            self.news_url_ = "https://rss.elconfidencial.com/mundo"

        async def run(self):
            msg = await self.receive(timeout=120)
            if msg:
                print("Message received: {}".format(msg.body))

                response_body = self.processNews(msg.body)

                msg = Message(to=str(msg.sender))
                msg.set_metadata("performative", "inform")
                msg.body = response_body

                await self.send(msg)
            else:
                print("No message after 120 seconds")
            await self.agent.stop()

        def processNews(self, news_keyword):
            news_scrapper = NewsScrapper(self.news_url_)
            onto = Onto(self.ontology_url_, self.ontology_dir_)

            feed = news_scrapper.search_from_titles(news_keyword)
            instance = onto.add_instance(news_keyword, feed)
            onto_result = {"irl": onto.get_iri(
            ), "instance": onto.instance_to_str(instance)}

            return json.dumps(onto_result)

    async def setup(self):
        self.b = self.RecvBehav()
        self.add_behaviour(self.b)


if __name__ == "__main__":
    receiveragent = ReceiverAgent("frafolco_r@gtirouter.dsic.upv.es", "4241")
    res = receiveragent.start()
    time.sleep(2)
    res.result()

    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            receiveragent.stop()
            break
