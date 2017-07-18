# -*-coding:utf-8 -*-

""" module docstring
"""

from datetime import datetime, timedelta

from flask import render_template, request
from flask import jsonify

from aun import aun_app
from aun.home import home
from aun.home.models import News, Category, SlideShow, news_category


@aun_app.template_filter('time')
def time_filter(time):
    """ used in template to format time
        usage : '|time'
    """
    if isinstance(time, datetime) is True:
        now = datetime.now()
        utc_now = datetime.utcnow()
        return (time - (utc_now - now)).strftime('%Y %b %d %H:%M')
    elif isinstance(time, str):
        now = datetime.now()
        utc_now = datetime.utcnow()
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        time = time - (utc_now - now)
        return time.strftime("%Y %b %d %H:%M")


@home.route('/', methods=["POST", "GET"])
@home.route('/index', methods=["POST", "GET"])
def index():
    """ function docstring
    """
    slideshow = SlideShow.query.order_by(
        SlideShow.post_time.desc()).limit(5).all()
    associations = get_news(1, "魅力社团")  # charm_association
    notifications = get_news(1, "通知")
    advance_notice = get_news(1, "预告")
    news_featured = get_news(1, "品牌活动")
    news_hust = get_news(1, "魅力华科")
    news_preview = get_news(2, "新闻")
    return render_template(
        "Home/index/index.html", SliderShow=slideshow, CharmAssociation=associations, LatestNotice=notifications, LatestAdvanceNotice=advance_notice, NewsPinPai=news_featured,
        NewsCharmHust=news_hust, NewsYuLan=news_preview)


@home.route('/news/<int:id>', methods=["POST", "GET"])
def show_news(news_id):
    """ function docstring
    """
    news = News.query.filter(News.news_id == news_id).first()
    return render_template("Home/news/detail.html", news=news)


@home.route('/news', methods=["POST", "GET"])
def index_news():
    """ function docstring
    """
    return render_template("Home/news/index.html")


@home.route('/au_card', methods=['GET'])
def au_card():
    """ function docstring
    """
    return render_template('Home/PartnerInfo/PartnerInfo.html')


def get_news(number, category):
    """ function docstring
    """
    news = News.query.join(news_category).join(Category).filter(
        Category.name == category).order_by(News.post_time).limit(number).all()
    return news


# change news objects into json
def news_to_json(news, length, page, news_number):
    """ function docstring
    """
    news_json = dict()
    news_json['title'] = list()
    news_json['outline'] = list()
    news_json['img_url'] = list()
    news_json['post_time'] = list()
    news_json['length'] = length
    news_json['news_number'] = news_number
    news_json['current_page'] = str(page)
    news_json['id'] = list()
    i = 0
    for new in news:
        now = datetime.now()
        utc_now = datetime.utcnow()
        news_json['title'].append(dict({i: new.title}))
        news_json['outline'].append(dict({i: new.outline}))
        news_json['img_url'].append(dict({i: new.img_url}))
        news_json['post_time'].append(
            dict({i: (new.post_time - (utc_now - now)).strftime('%Y %b %d %H:%M')}))
        news_json['id'].append(dict({i: new.news_id}))
        i = i + 1
    return news_json


#/news page to load news by ajax
@home.route('/news/news2Json', methods=["POST", "GET"])
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
            news = News.query.filter(News.post_time > time).order_by(
                News.post_time.desc()).all()
            news_number = len(news)
            news = news[(goto_page - 1) * 10:goto_page * 10]
        elif category == "all" and sort == "oldest":
            news = News.query.filter(
                News.post_time > time).order_by(News.post_time).all()
            news_number = len(news)
            news = news[(goto_page - 1) * 10:goto_page * 10]
        elif category != "all" and (sort == "all" or sort == "hot" or sort == "latest"):
            news = News.query.join(news_category).join(Category).filter(News.post_time > time).filter(
                Category.name == category).order_by(News.post_time.desc()).all()
            news_number = len(news)
            news = news[(goto_page - 1) * 10:goto_page * 10]
        elif category != "all" and sort == "oldest":
            news = News.query.join(news_category).join(Category).filter(
                News.post_time > time, Category.name == category).order_by(News.post_time).all()
            news_number = len(news)
            news = news[(goto_page - 1) * 10:goto_page * 10]
        else:
            news = None
        if news != None:
            news_json = news_to_json(news, len(news), goto_page, news_number)
            return jsonify(news_json)
        else:
            return "<html><body>bad</body></html>"
    return "bad method"
