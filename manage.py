# -*- coding:utf-8 -*-

""" management script of AUN
"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from aun import aun_app, aun_db
from aun.home.models import News, news_category, news_tag, Category, Tag, SlideShow
from aun.admin.models import User, Node, Role, user_role, role_node


manager = Manager(aun_app)
migrate = Migrate(aun_app, aun_db)

manager.add_command("db", MigrateCommand)  # 数据库我迁移命令


@manager.option('-n', '--name', dest="name", help='Your name', default="admin")
@manager.option('-p', '--password', dest='password', help="Your password", default="123456")
@manager.option('-e', '--email', dest="email", help="your email", default=None)
@manager.option('--phone', dest="phone", help="your phone", default=None)
def create_super_user(name, password, email, phone):
    """ function docstring
    """
    try:
        user = User(name, password, email, phone)
        user.addRole("超管")
        aun_db.session.add(user)
        aun_db.session.commit()
        print("successfully create a super user name:%s,password:%s,email:%s,phone:%s" % (
            name, password, email, phone))
    except:
        print("something wrong.please ensure you have created a super role and your name is unique")


@manager.command
def create_super_role():
    """ function docstring
    """
    try:
        role = Role("超管")
        node1 = Node("添加用户", 1)
        node2 = Node("修改用户", 1)
        node3 = Node("删除用户", 1)
        node4 = Node("添加角色", 1)
        node5 = Node("修改角色", 1)
        node6 = Node("删除角色", 1)
        node7 = Node("添加新闻", 1)
        node8 = Node("修改新闻", 1)
        node9 = Node("删除新闻", 1)
        node10 = Node("添加新闻属性", 1)
        node11 = Node("修改新闻属性", 1)
        node12 = Node("删除新闻属性", 1)
        node13 = Node("添加新闻标签", 1)
        node14 = Node("修改新闻标签", 1)
        node15 = Node("删除新闻标签", 1)
        node16 = Node("修改节点", 1)
        node17 = Node("materialAdmin", 1)
        node18 = Node("materialAction", 1)
        node19 = Node("查看新闻", 1)
        node20 = Node("查看新闻栏目", 1)
        node21 = Node("查看新闻标签", 1)
        node22 = Node("查看用户", 1)
        node23 = Node("查看角色", 1)
        node24 = Node("查看权限节点", 1)
        aun_db.session.add(node1)
        aun_db.session.add(node2)
        aun_db.session.add(node3)
        aun_db.session.add(node4)
        aun_db.session.add(node5)
        aun_db.session.add(node6)
        aun_db.session.add(node7)
        aun_db.session.add(node8)
        aun_db.session.add(node9)
        aun_db.session.add(node10)
        aun_db.session.add(node11)
        aun_db.session.add(node12)
        aun_db.session.add(node13)
        aun_db.session.add(node14)
        aun_db.session.add(node15)
        aun_db.session.add(node16)
        aun_db.session.add(node17)
        aun_db.session.add(node18)
        aun_db.session.add(node19)
        aun_db.session.add(node20)
        aun_db.session.add(node21)
        aun_db.session.add(node22)
        aun_db.session.add(node23)
        aun_db.session.add(node24)
        aun_db.session.add(role)
        aun_db.session.commit()
        role = Role.query.filter(Role.roleName == "超管").first()
        role.addNode("添加用户")
        role.addNode("删除用户")
        role.addNode("修改用户")
        role.addNode("添加角色")
        role.addNode("修改角色")
        role.addNode("删除角色")
        role.addNode("添加新闻")
        role.addNode("修改新闻")
        role.addNode("删除新闻")
        role.addNode("添加新闻属性")
        role.addNode("修改新闻属性")
        role.addNode("删除新闻属性")
        role.addNode("添加新闻标签")
        role.addNode("修改新闻标签")
        role.addNode("删除新闻标签")
        role.addNode("修改节点")
        role.addNode("materialAdmin")
        role.addNode("materialAction")
        role.addNode("查看新闻")
        role.addNode("查看新闻栏目")
        role.addNode("查看新闻标签")
        role.addNode("查看用户")
        role.addNode("查看角色")
        role.addNode("查看权限节点")

        aun_db.session.add(role)
        aun_db.session.commit()
        print("successfully create a super role name:超管")
    except:
        print("you can only run it once")


@manager.command
def create_necessary_items():
    """ function docstring
    """
    try:
        c1 = Category("通知")
        c2 = Category('预告')
        c3 = Category('魅力社团')
        c4 = Category('品牌活动')
        c5 = Category('魅力华科')
        c6 = Category("新闻")
        t1 = Tag("news")

        aun_db.session.add(c1)
        aun_db.session.add(c2)
        aun_db.session.add(c3)
        aun_db.session.add(c4)
        aun_db.session.add(c5)
        aun_db.session.add(c6)
        aun_db.session.add(t1)

        aun_db.session.commit()
    except:
        print("something wrong")


if __name__ == '__main__':
    manager.run()
