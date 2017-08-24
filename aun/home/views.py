# -*-coding:utf-8 -*-

""" module docstring
"""

from datetime import datetime, timedelta

from flask import render_template, request, current_app
from flask import jsonify

# from aun import aun_app
from aun.home import home
from aun.home.models import Article, Category, SlideShow, article_category


# @aun_app.template_filter('time')
# def time_filter(time):
#     """ used in template to format time
#         usage : '|time'
#     """
#     with app.app_context():
#         if isinstance(time, datetime) is True:
#             now = datetime.now()
#             utc_now = datetime.utcnow()
#             return (time - (utc_now - now)).strftime('%Y %b %d %H:%M')
#         elif isinstance(time, str):
#             now = datetime.now()
#             utc_now = datetime.utcnow()
#             time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
#             time = time - (utc_now - now)
#             return time.strftime("%Y %b %d %H:%M")


@home.route('/', methods=["POST", "GET"])
@home.route('/index', methods=["POST", "GET"])
def index():
    """ function docstring
    """
    slideshow = SlideShow.query.order_by(
        SlideShow.post_time.desc()).limit(5).all()
    associations = get_article(1, "魅力社团")  # charm_association
    notifications = get_article(1, "通知")
    advance_notice = get_article(1, "预告")
    article_featured = get_article(1, "品牌活动")
    article_hust = get_article(1, "魅力华科")
    article_preview = get_article(2, "新闻")
    return render_template(
        "Home/index/index.html", SliderShow=slideshow, CharmAssociation=associations, LatestNotice=notifications, LatestAdvanceNotice=advance_notice, ArticlePinPai=article_featured,
        ArticleCharmHust=article_hust, ArticleYuLan=article_preview)


@home.route('/article/<int:id>', methods=["POST", "GET"])
def show_article(article_id):
    """ function docstring
    """
    article = Article.query.filter(Article.article_id == article_id).first()
    return render_template("Home/article/detail.html", article=article)


@home.route('/article', methods=["POST", "GET"])
def index_article():
    """ function docstring
    """
    return render_template("Home/article/index.html")


@home.route('/au_card', methods=['GET'])
def au_card():
    """ function docstring
    """
    return render_template('Home/PartnerInfo/PartnerInfo.html')


def get_article(number, category):
    """ function docstring
    """
    article = Article.query.join(article_category).join(Category).filter(
        Category.name == category).order_by(Article.post_time).limit(number).all()
    return article


# change article objects into json
def article_to_json(article, length, page, article_number):
    """ function docstring
    """
    article_json = dict()
    article_json['title'] = list()
    article_json['outline'] = list()
    article_json['img_url'] = list()
    article_json['post_time'] = list()
    article_json['length'] = length
    article_json['article_number'] = article_number
    article_json['current_page'] = str(page)
    article_json['id'] = list()
    i = 0
    for new in article:
        now = datetime.now()
        utc_now = datetime.utcnow()
        article_json['title'].append(dict({i: new.title}))
        article_json['outline'].append(dict({i: new.outline}))
        article_json['img_url'].append(dict({i: new.img_url}))
        article_json['post_time'].append(
            dict({i: (new.post_time - (utc_now - now)).strftime('%Y %b %d %H:%M')}))
        article_json['id'].append(dict({i: new.article_id}))
        i = i + 1
    return article_json


#/article page to load article by ajax
@home.route('/article/article2Json', methods=["POST", "GET"])
def new_json():
    """ function docstring
    """
    if request.method == 'POST':
        get_dict = request.get_json()
        now = datetime.now()
        category = get_dict['Category']
        time = get_dict['Time']
        sort = get_dict['Sort']
        goto_page = get_dict['gotoPage']
        goto_page = int(goto_page)
        if time == "all":
            time = now - timedelta(days=365 * 10)
        elif time == "week":
            time = now - timedelta(days=7)
        elif time == "month":
            time = now - timedelta(days=90)
        elif time == "year":
            time = now - timedelta(days=365)

        if category == "all" and (sort == "all" or sort == "hot" or sort == "latest"):
            article = Article.query.filter(Article.post_time > time).order_by(
                Article.post_time.desc()).all()
            article_number = len(article)
            article = article[(goto_page - 1) * 10:goto_page * 10]
        elif category == "all" and sort == "oldest":
            article = Article.query.filter(
                Article.post_time > time).order_by(Article.post_time).all()
            article_number = len(article)
            article = article[(goto_page - 1) * 10:goto_page * 10]
        elif category != "all" and (sort == "all" or sort == "hot" or sort == "latest"):
            article = Article.query.join(article_category).join(Category).filter(Article.post_time > time).filter(
                Category.name == category).order_by(Article.post_time.desc()).all()
            article_number = len(article)
            article = article[(goto_page - 1) * 10:goto_page * 10]
        elif category != "all" and sort == "oldest":
            article = Article.query.join(article_category).join(Category).filter(
                Article.post_time > time, Category.name == category).order_by(Article.post_time).all()
            article_number = len(article)
            article = article[(goto_page - 1) * 10:goto_page * 10]
        else:
            article = None
        if article != None:
            article_json = article_to_json(
                article, len(article), goto_page, article_number)
            return jsonify(article_json)
        else:
            return "<html><body>bad</body></html>"
    return "bad method"
