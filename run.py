# -*-coding:utf-8 -*-

""" launch script of AUN
"""

from aun import create_app

aun_app = create_app('config.DevelopmentConfig')

aun_app.run(debug=True)
