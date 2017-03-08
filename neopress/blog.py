#!/usr/bin/env python
# coding: utf-8


from neo4j.v1 import GraphDatabase

from .article import Article


class Blog(object):

    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

    def close(self):
        self.driver.close()

    def save_article(self, article):
        with self.driver.session() as session:
            return session.write_transaction(article.save)

    def load_article(self, slug):
        with self.driver.session() as session:
            return session.read_transaction(lambda tx: Article.load(tx, slug))

    def load_all_articles(self):
        with self.driver.session() as session:
            return session.read_transaction(lambda tx: Article.load_all(tx))
