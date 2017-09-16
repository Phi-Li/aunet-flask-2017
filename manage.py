# -*- coding:utf-8 -*-

""" management script of AUN
"""

import traceback

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from aun import aun_db
from aun.home.models import Article, Category, Tag, article_category, article_tag, SlideShow
from aun.association.models import Club, club_article
from aun.admin.models import User, Node, Role, user_role, role_node, user_club ,\
    LoginLog
from aun.data_station.models import DataStation
from aun.sign_up.models import Applicant
from aun import create_app
from config import DevelopmentConfig, ProductionConfig

aun_app = create_app(DevelopmentConfig)
manager = Manager(aun_app)
migrate = Migrate(aun_app, aun_db)

manager.add_command("db", MigrateCommand)  # 数据库我迁移命令


def add_and_commit(*items):
    for item in items:
        aun_db.session.add(item)
    aun_db.session.commit()


@manager.option('-n', '--name', dest="name", help='Your name', default="admin")
@manager.option('-p', '--password', dest='password', help="Your password", default="123456")
@manager.option('-e', '--email', dest="email", help="your email", default=None)
@manager.option('--phone', dest="phone", help="your phone", default=None)
def create_super_user(name, password, email, phone):
    """
    create super user
    """
    try:
        user = User(name, password, email, phone)
        user.add_role("超管")
        add_and_commit(user)
        print("successfully create a super user name:%s,password:%s,email:%s,phone:%s" % (
            name, password, email, phone))
    except:
        print("something wrong.please ensure you have created a super role and your name is unique")


@manager.command
def create_super_role():
    """
    create super role
    """
    try:
        role = Role("超管")
        node1 = Node("查看用户", 1)
        node2 = Node("添加用户", 1)
        node3 = Node("修改用户", 1)
        node4 = Node("删除用户", 1)

        node5 = Node("查看角色", 1)
        node6 = Node("添加角色", 1)
        node7 = Node("修改角色", 1)
        node8 = Node("删除角色", 1)

        node9 = Node("修改节点", 1)
        node10 = Node("查看权限节点", 1)

        node11 = Node("添加文章", 1)
        node12 = Node("修改文章", 1)
        node13 = Node("删除文章", 1)

        node14 = Node("添加文章栏目", 1)
        node15 = Node("修改文章栏目", 1)
        node16 = Node("删除文章栏目", 1)

        node17 = Node("添加文章标签", 1)
        node18 = Node("修改文章标签", 1)
        node19 = Node("删除文章标签", 1)

        node20 = Node("materialAdmin", 1)
        node21 = Node("materialAction", 1)

        node22 = Node("添加社团", 1)
        node23 = Node("编辑社团空间", 1)
        node24 = Node("删除社团", 1)

        node25 = Node("删除报名人员", 1)

        node26 = Node("上传文件", 1)
        node27 = Node("修改文件属性", 1)  # 包括审核文件，设置红头文件
        node28 = Node("删除文件", 1)

        node29 = Node("编辑社团介绍", 1)  # 用于社联页面，各社团介绍

        add_and_commit(node1, node2, node3, node4, node5, node6, node7, node8,
                       node9, node10, node11, node12, node13, node14, node15, node16,
                       node17, node18, node19, node20, node21, node22, node23, node24,
                       node25, node26, node27, node28, node29, role)

        role = Role.query.filter(Role.role_name == "超管").first()
        role.add_node("添加用户")
        role.add_node("删除用户")
        role.add_node("修改用户")
        role.add_node("查看用户")

        role.add_node("查看角色")
        role.add_node("添加角色")
        role.add_node("修改角色")
        role.add_node("删除角色")

        role.add_node("添加文章")
        role.add_node("修改文章")
        role.add_node("删除文章")

        role.add_node("添加文章栏目")
        role.add_node("修改文章栏目")
        role.add_node("删除文章栏目")

        role.add_node("添加文章标签")
        role.add_node("修改文章标签")
        role.add_node("删除文章标签")

        role.add_node("修改节点")
        role.add_node("查看权限节点")

        role.add_node("materialAction")
        role.add_node("materialAdmin")

        role.add_node("添加社团")
        role.add_node("编辑社团空间")
        role.add_node("删除社团")

        role.add_node("删除报名人员")

        role.add_node("上传文件")
        role.add_node("修改文件属性")
        role.add_node("删除文件")

        role.add_node("编辑社团介绍")

        add_and_commit(role)

        print("successfully create a super role name:超管")
    except:
        print("you can only run it once or something wrong")


@manager.command
def create_test_items():
    """
    create necessary items before web well worked
    """
    try:
    # news and club article
        cate = Category("news")
        tag = Tag("news")
        add_and_commit(cate, tag)
        # index news
        newses = list()
        for i in range(8):
            news = Article("<p>\n 测试\n <br/>\n</p>", "测试", "测试",
                        "static/images/sample_img_as.jpg")
            news.add_category("news")
            news.add_tag("news")
            newses.append(news)
            add_and_commit(news)
            
        articles = list() #club article
        for i in range(8):
            article = Article("<p>\n 测试\n <br/>\n</p>", "测试", "测试",
                            "static/images/sample_img_as.jpg")
            article.add_category("news")
            article.add_tag("news")
            articles.append(article)
            add_and_commit(article)

        # slideshow
        slideshow = SlideShow(
            "", "/static/images/sample_img_cro.png", "", "http://www.google.com")
        add_and_commit(slideshow)

        # club
        club = Club("566", "566", "566", "/static/images/sample_img_as.jpg")
        club.articles = articles
        club1 = Club("566轮滑", "566轮滑", "566轮滑", "/static/images/sample_img_as.jpg")
        club1.articles = articles
        club2 = Club("566轮滑社", "566轮滑社", "566轮滑社", "/static/images/sample_img_as.jpg")
        club2.articles = articles
        add_and_commit(club, club1, club2)

        # add club for user
        user = User.query.filter(User.user_name == "admin").first()
        user.add_club("566")
        user.add_club("566轮滑")
        user.add_club("566轮滑社")
        add_and_commit(user)

        file = DataStation("线上报名导出表.docx", "admin", "test")
        add_and_commit(file)

        print("you have done a good job")
    except:
        traceback.print_exc()
        print("something wrong")
if __name__ == '__main__':
    manager.run()
