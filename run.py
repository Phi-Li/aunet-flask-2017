# -*-coding:utf-8 -*-

""" launch script of AUN
"""

from aun import create_app

aun_app = create_app('config.DevelopmentConfig')
try:
    aun_app.config.from_object('secret_config.ProductionConfig')  # 导入secret配置
except:
    pass


if __name__ == "__main__":
    aun_app.run(debug=True)
