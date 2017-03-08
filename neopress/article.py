#!/usr/bin/env python
# coding: utf-8


from markdown import markdown


MATCH_ALL_ARTICLES = """\
MATCH (a:Article)
RETURN a.slug AS slug, a.content AS content
"""
MATCH_ARTICLE = """\
MATCH (a:Article) WHERE a.slug = $slug
RETURN a.slug AS slug, a.content AS content
"""
MERGE_ARTICLE = """\
MERGE (a:Article {slug: $slug})
SET a.content = $content
RETURN id(a)
"""

DELETE_ARTICLE = """\
match (a:article {slug: $slug})
delete a
"""


class Article(object):

    def __init__(self, slug, content):
        self.slug = slug
        self.content = content

    def to_html(self):
        return markdown(self.content)

    def save(self, tx):
        result = tx.run(MERGE_ARTICLE, slug=self.slug, content=self.content)
        record = result.single()
        return record[0]

    def delete(self, tx):
        result = tx.run(DELETE_ARTICLE, slug=self.slug, content=self.content)
        record = result.single()
        return record[0]

    @classmethod
    def load(cls, tx, slug):
        result = tx.run(MATCH_ARTICLE, slug=slug)
        record = result.single()
        if record is None:
            return None
        return Article(**record)

    @classmethod
    def load_all(cls, tx):
        result = tx.run(MATCH_ALL_ARTICLES)
        return [Article(**record) for record in result]
