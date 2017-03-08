#!/usr/bin/env python
# coding: utf-8


from flask import Flask, request, abort

from .article import Article
from .blog import Blog

app = Flask(__name__)
blog = Blog()


@app.route("/")
def index():
    return "<ul>" + "".join('<li><a href="{}">{}</a></li>'.format(article.slug, article.slug)
                            for article in blog.load_all_articles()) + "</ul>"


@app.route("/<slug>", methods=["GET"])
def get_article(slug):
    article = blog.load_article(slug) or abort(404)
    return article.to_html()


@app.route("/<slug>", methods=["PUT"])
def put_article(slug):
    blog.save_article(Article(slug, request.get_data()))
    return "", 204  # No Content

@app.route("/<slug>", methods=["DELETE"])
def delete_article(slug):
    blog.delete_article(slug) or abort(404)
    return "", 204


def run():
    app.run()
