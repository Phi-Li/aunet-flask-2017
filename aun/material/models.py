#--coding:UTF-8--
from aun import aun_db


class Base(object):
    '''the base of all the apply tables'''
    id = aun_db.Column(aun_db.INT, primary_key=True)
    apply_time = aun_db.Column(aun_db.DateTime)
    approve_time = aun_db.Column(aun_db.DateTime, nullable=True)
    result = aun_db.Column(aun_db.CHAR(1), default='0', nullable=False)
    applicant = aun_db.Column(aun_db.String(10), nullable=False)
    advice = aun_db.Column(aun_db.String(20))
    pre_verify = aun_db.Column(aun_db.String(20))
    is_print = aun_db.Column(aun_db.CHAR(1))
    filename = aun_db.Column(aun_db.VARCHAR(50))
    rand_filename = aun_db.Column(aun_db.VARCHAR(15))

    association = aun_db.Column(aun_db.String(10), nullable=False)
    tel = aun_db.Column(aun_db.String(15))
    date = aun_db.Column(aun_db.DateTime)
    site = aun_db.Column(aun_db.String(10))
    submit_user_id = aun_db.Column(aun_db.Integer)


class Base1(object):
    '''the base of east4,outdoor,sacenter,special'''
    activity = aun_db.Column(aun_db.String(15))
    number = aun_db.Column(aun_db.SMALLINT)
    sponsor = aun_db.Column(aun_db.TEXT)
    opinion = aun_db.Column(aun_db.String(10))
    content = aun_db.Column(aun_db.TEXT)
    resp_person = aun_db.Column(aun_db.String(10), nullable=False)
    time = aun_db.Column(aun_db.String(6))


class East4(aun_db.Model, Base, Base1):
    '''model of east4'''
    __tablename__ = 'material_east4'
    site = None


class Outdoor(aun_db.Model, Base, Base1):
    '''model of outdoor'''
    __tablename__ = 'material_outdoor'


class Sacenter(aun_db.Model, Base, Base1):
    '''model of student activity center'''
    __tablename__ = 'material_sacenter'
    is_query = aun_db.Column(aun_db.CHAR(1))
    site_type = aun_db.Column(aun_db.CHAR(1))


class Special(aun_db.Model, Base, Base1):
    '''model of special'''
    __tablename__ = 'material_special'
    is_query = aun_db.Column(aun_db.CHAR(1))


class Colorprint(aun_db.Model, Base):
    '''model of colorprint'''
    __tablename__ = 'material_colorprint'
    finish_date = aun_db.Column(aun_db.DateTime)
    is_sponsor = aun_db.Column(aun_db.CHAR(1))
    remark = aun_db.Column(aun_db.TEXT)
    time = aun_db.Column(aun_db.String(6))
    content = aun_db.Column(aun_db.TEXT)
    resp_person = aun_db.Column(aun_db.String(10), nullable=False)


class Sports(aun_db.Model, Base):
    '''model of sports'''
    __tablename__ = 'material_sports'
    school_id = aun_db.Column(aun_db.String(10))
    remark = aun_db.Column(aun_db.TEXT)
    time = aun_db.Column(aun_db.String(6))
    resp_person = aun_db.Column(aun_db.String(10), nullable=False)
    department = aun_db.Column(aun_db.String(15))
    content = aun_db.Column(aun_db.TEXT)


class Materials(aun_db.Model, Base):
    '''model of material'''
    __tablename__ = 'material_material'
    resp_person = aun_db.Column(aun_db.String(10), nullable=False)
    activity = aun_db.Column(aun_db.String(15))
    opinion = aun_db.Column(aun_db.String(20))
    projector_date = aun_db.Column(aun_db.DATE)
    projector_num = aun_db.Column(aun_db.SMALLINT)
    chair_date = aun_db.Column(aun_db.DATE)
    electricity_num = aun_db.Column(aun_db.SMALLINT)
    desk_num = aun_db.Column(aun_db.SMALLINT)
    chair_num = aun_db.Column(aun_db.SMALLINT)
    trans_desk_num = aun_db.Column(aun_db.SMALLINT)
    trans_chair_num = aun_db.Column(aun_db.SMALLINT)


class Teachingbuilding(aun_db.Model, Base):
    '''model of teachingbuilding'''
    __tablename__ = 'material_teachingbuilding'
    content = aun_db.Column(aun_db.TEXT())
    activity = aun_db.Column(aun_db.String(15))
    signature = aun_db.Column(aun_db.String(10))
    capacity = aun_db.Column(aun_db.SMALLINT)
    number = aun_db.Column(aun_db.SMALLINT)
    week = aun_db.Column(aun_db.String(5))
    person_type = aun_db.Column(aun_db.CHAR(5))
    function = aun_db.Column(aun_db.CHAR(5))
    phone = aun_db.Column(aun_db.String(15))
    section = aun_db.Column(aun_db.CHAR(5))
    activity_type = aun_db.Column(aun_db.CHAR(1))
    host = aun_db.Column(aun_db.String(10))
    unit = aun_db.Column(aun_db.String(20))
    title = aun_db.Column(aun_db.String(10))
    resp_person = aun_db.Column(aun_db.String(10), nullable=False)
