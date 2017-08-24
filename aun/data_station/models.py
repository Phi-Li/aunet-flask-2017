# -*- coding: utf-8 -*-

"""
uploaded file table
"""
from datetime import datetime

from aun import aun_db


class DataStation(aun_db.Model):
	"""
	uploaded file table

	"""
	file_id = aun_db.Column(aun_db.Integer, primary_key=True)
	file_name = aun_db.Column(aun_db.String(40), unique=True)
	uploader = aun_db.Column(aun_db.String(20))
	upload_time = aun_db.Column(aun_db.DateTime, default=datetime.now)
	download_times = aun_db.Column(aun_db.Integer, default=0)
	status = aun_db.Column(aun_db.Integer, default=0)  # 审核状态;0为未审核，１为通过，－１为未通过
	# is_important=1 用于首页重要文件展示
	is_important = aun_db.Column(aun_db.Boolean, default=False)

	def __init__(self, file_name, uploader):
		self.file_name = file_name
		self.uploader = uploader

    def __str__(self):
        return "file name:%s" % self.file_name
    __repr__ = __str__
_
