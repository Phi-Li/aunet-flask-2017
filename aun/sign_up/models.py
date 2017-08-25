# -*-coding:utf-8 -*-
"""
Applicant related table 
"""
from datetime import datetime
from aun import aun_db


class Applicant(aun_db.Model):
    """
    applicant that want to join in AU
    """
    __tablename__ = "applicant"
    id = aun_db.Column(aun_db.Integer, primary_key=True)
    name = aun_db.Column(aun_db.String(20))
    gender = aun_db.Column(aun_db.String(20))
    major = aun_db.Column(aun_db.String(40))
    phone = aun_db.Column(aun_db.String(20))
    first_choice = aun_db.Column(aun_db.String(30))
    second_choice = aun_db.Column(aun_db.String(30))
    is_adjust = aun_db.Column(aun_db.Boolean)
    self_introduction = aun_db.Column(aun_db.String)
    apply_time = aun_db.Column(aun_db.DateTime)

    def __init__(self, name, gender, major, phone, first_choice, second_choice, is_adjust, self_introduction):

        self.name = name
        self.gender = gender
        self.major = major
        self.phone = phone
        self.first_choice = first_choice
        self.second_choice = second_choice
        self.is_adjust = is_adjust
        self.self_introduction = self_introduction
        self.apply_time = datetime.utcnow()
