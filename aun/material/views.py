# -- coding: UTF-8 --
from urllib.request import quote
from docxtpl import DocxTemplate, RichText
from time import time, mktime, strftime, strptime, localtime
from datetime import datetime
from flask import render_template, redirect, url_for, flash,\
    Blueprint, make_response, request, abort, send_file
# from flask_mail import Message
from flask_login import login_required, current_user
from flask_principal import Permission, ActionNeed
from os import path, remove
from random import randint
import json
from flask import current_app

from aun import aun_db
from aun.material import material
from aun.admin.email import send_email
from aun.admin.models import User
from aun.material.models import *


# Docx_path = path.join(current_app.config['BASEDIR'],.

# 'aun', 'static', 'Material', 'docx')
types = {
    'east4': (East4, '东四三楼'),
    'colorprint': (Colorprint, '彩喷悬挂'),
    'material': (Materials, '物资借用'),
    'outdoor': (Outdoor, '路演场地'),
    'sacenter': (Sacenter, '大活教室'),
    'special': (Special, '特殊场地'),
    'sports': (Sports, '体育场馆'),
    'teachingbuilding': (Teachingbuilding, '教学楼教室')
}

action_permission = Permission(ActionNeed('materialAction'))
admin_permission = Permission(ActionNeed('materialAdmin'))


def make_context(data, type):
    context = {}
    if type in ['east4', 'outdoor', 'special', 'sacenter']:
        context['is_sponsor'] = '是' if data.sponsor\
            else '否'
    if type == 'sacenter':
        context['site'+data.site_type] = data.site
    elif type == 'teachingbuilding':
        days = ['一', '二', '三', '四', '五', '六', '日']
        context['day'] = days[data.date.weekday()-1]
        for x in ['content', 'host', 'unit', 'title']:
            context[x+data.activity_type] = getattr(data, x)
    # 不需要进行渲染的字段
    except_fields = [
        'metadata', 'query', 'query_class',
        'id', 'apply_time', 'approve_time',
        'advice', 'result', 'applicant',
        'year1', 'month1', 'date1'
    ]
    # 生成context
    for x in dir(data):
        if x in except_fields or x[0] == '_':
            continue
        field = str(getattr(data, x))
        if field == 'None' or field == '0':
            field = ''
        context[x] = field

    return context


def query_data(type, id):
    if type not in types.keys():
        abort(404)
    data = types[type][0].query.filter_by(id=int(id)).first_or_404()
    if str(current_user.user_id) != data.applicant and \
            not admin_permission.can():
        abort(403)
    return data


@material.route('/download/<file_type>', methods=['POST'])
@login_required
@action_permission.require(403)
def download(file_type):
    '''下载接口'''

    Upload_path = path.join(
        current_app.config['BASEDIR'], 'aun', 'static', 'upload', 'material')
    Docx_path = path.join(current_app.config['BASEDIR'],
                          'aun', 'static', 'material', 'docx')

    if file_type not in ['form', 'scheme']:
        abort(404)
    id = request.form.get('id')
    type = request.form.get('type')
    data = query_data(type, id)
    # 下载策划
    if file_type == 'scheme':
        if data.filename == 'Nothing':
            abort(404)
        content = send_file(path.join(Upload_path, data.rand_filename))
        filename = quote(data.filename)
    # if data.applicant!=current_user.name :abort(404)
    else:
        # 生成context并进行渲染
        context = make_context(data, type)
        for key, value in context.items():
            context[key] = RichText(value)
        doc = DocxTemplate(path.join(Docx_path, type+'.docx'))
        doc.render(context)
        temp_file = path.join(Upload_path, str(
            current_user.user_id) + 'result.docx')
        doc.save(temp_file)
        # 读取渲染后的文件并将之删除
        with open(temp_file, 'rb') as f:
            content = f.read()
        if path.exists(temp_file):
            remove(temp_file)
        filename = quote(data.association+'-'+types[type][1]+'.docx')

    response = make_response(content)
    response.headers['Content-Disposition'] = \
        "attachment;filename*=UTF-8''" + filename
    response.headers['Content-Type'] = 'application/octet-stream'
    return response


@material.route('/delete/', methods=['POST'])
@login_required
@action_permission.require(403)
def delete():
    '''删除申请'''
    Upload_path = path.join(
        current_app.config['BASEDIR'], 'aun', 'static', 'upload', 'material')
    id = request.form.get('id')
    type = request.form.get('type')
    data = query_data(type, id)

    if data.filename != 'Nothing' and \
            path.exists(path.join(Upload_path, data.rand_filename)):
        remove(path.join(Upload_path, data.rand_filename))
    aun_db.session.delete(data)
    aun_db.session.commit()
    flash('删除成功！')
    return redirect(url_for('material.status'))


@material.route('/submit/', methods=['POST'])
@login_required
@action_permission.require(403)
def submit():
    '''申请提交接口'''

    Upload_path = path.join(
        current_app.config['BASEDIR'], 'aun', 'static', 'upload', 'material')
    form = request.form
    print(form)
    type = form['type']
    id = form['uid']
    if type not in types:
        abort(404)
    time = localtime()
    if id != "":
        data = query_data(type, id)
    else:
        data = types[type][0]()
        upload_file = request.files['file']
        if upload_file.filename != '':
            data.filename = upload_file.filename
            rand_filename = str(randint(10000, 99999))+str(int(mktime(time)))
            data.rand_filename = rand_filename
            upload_file.save(path.join(Upload_path, rand_filename))
        else:
            data.filename = 'Nothing'

    data.applicant = current_user.user_name
    data.date = datetime.strptime(
        form['year1']+'-'+form['month1']+'-'+form['date1'], '%Y-%m-%d')
    data.apply_time = datetime.now()  # strftime('%Y-%m-%d %H:%M:%S', time)
    data.submit_user_id = current_user.user_id

    if type == 'material':
        if form['material_type'] == '2':
            data.chair_date = form['year2']+'-'\
                + form['month2']+'-'+form['date2']
        if form['material_type'] == '4':
            data.projector_date = form['year3']+'-'\
                + form['month3']+'-'+form['date3']
    date_items = [a+b for a in ['year', 'month', 'date']
                  for b in ['1', '2', '3']]

    for key, value in form.items():
        if key in date_items or key in ['uid', 'file']:
            continue
        if key[-3:] == 'num' or key == 'number':
            value = 0 if value == '' else int(value)
        setattr(data, key, value)
    try:
        aun_db.session.add(data)
        aun_db.session.commit()
    except:
            # if upload_file.name != '' and path.exists(path.join(Upload_path, rand_filename)):
            #     remove(path.join(Upload_path, rand_filename))
        aun_db.session.rollback()
        flash("表单数据有误，未能成功提交！")
        return redirect(url_for('material.status'))
    # 发送邮件
    html = render_template(
        'material/mail/submit_success.html',
        userName=current_user.user_name, type=types[type][1])
    send_email("场地物资申请提交成功", [current_user.email], html)  # current_user.email

    flash("申请提交成功，等待审批！")
    return redirect(url_for('material.status'))


@material.route('/<option>/<type>/', methods=['POST', 'GET'])
@login_required
@action_permission.require(403)
def main(option, type):
    '''apply'''
    if type not in types.keys() or \
            option not in ['apply', 'modify']:
        abort(404)
    data = {}
    if option == 'modify':
        id = request.form.get('id')
        data = types[type][0].query.filter_by(id=id,
                                              applicant=current_user.user_id).first_or_404()
    apply_type = types[type][1]

    return render_template('/pages/'+type+'.html', data=data,
                           apply_type=apply_type)


@material.route('/procedure')
@material.route('/')
@login_required
@action_permission.require(403)
def procedure():
    data = {'association': 'procedure'}
    return render_template('/pages/'+'procedure.html',
                           data=data, apply_type="流程查询")


@material.route('/admin/')
# @login_required
# @admin_permission.require(403)
def admin():
    mark = request.args.get('mark')
    if mark == '0':
        mark = '03'
    if mark is None:
        mark = '0123'
    datas = []
    for aun_db_type in types.values():
        data = aun_db_type[0].query.all()
        if data is None:
            continue
        datas.extend(data)
    datas.sort(key=lambda x: x.apply_time, reverse=True)
    return render_template('admin.html', datas=datas, types=types, mark=mark)


@material.route('/status/')
@login_required
@action_permission.require(403)
def status():
    results = {'0': '审批中', '1': '已通过', '2': '未通过'}
    datas = []
    for aun_db_type in types.values():
        data = aun_db_type[0].query.all()
        if data is None:
            continue
        datas.extend(data)
    data = {'association': 'status'}
    return render_template('/pages/status.html',
                           datas=datas, types=types, results=results, data=data, apply_type='状态查询')


@material.route('/approve/', methods=['POST'])
@login_required
@admin_permission.require(403)
def approve():
    '''审批操作接口'''
    type = request.form.get('type')
    if type not in types.keys():
        abort(404)
    id = request.form.get('id')
    data = types[type][0].query.filter_by(id=int(id)).first_or_404()
    data.advice = request.form.get('advice')
    data.result = request.form.get('result')
    is_print = request.form.get('is_print')
    data.is_print = '否' if is_print is None else '是'
    data.pre_verify = request.form.get('pre_verify')
    data.approve_time = datetime.now()  # strftime('%Y-%m-%d %H:%M:%S', localtime())
    aun_db.session.add(data)
    aun_db.session.commit()
    flash('审批操作成功！')
    submit_user = User.query.filter(
        User.user_id == data.submit_user_id).first()
    # 发送邮件
    if data.result == "1":
        result = "通过"
        print(current_user.email)
        html = render_template(
            'material/mail/approve_status.html',
            userName=submit_user.user_name, submitTime=data.apply_time.strftime("%Y %b %d %H:%M"), type=types[type][1], result=result)
        send_email("场地物资申请审批结果", [submit_user.email], html)
    elif data.result == "2":
        result = "未通过"
        html = render_template(
            'material/mail/approve_status.html',
            userName=submit_user.user_name, submitTime=data.apply_time.strftime("%Y %b %d %H:%M"), type=types[type][1], result=result)
        send_email("场地物资申请审批结果", [submit_user.email], html)
    else:
        pass
    return redirect(url_for('material.admin'))


@material.route('/multiApprove/', methods=['POST'])
@login_required
@admin_permission.require(403)
def mult_approve():
    '''多项审批'''
    items = json.loads(request.get_data().decode('utf-8'))

    is_print = items['is_print']
    result = items['result']
    # data.advice = item['advice']
    # data.pre_verify = item['pre_verify']
    for item in items['items']:
        type = item['type']
        if type not in types.keys():
            abort(404)
        id = item['id']
        data = types[type][0].query.filter_by(id=int(id)).first_or_404()
        data.is_print = is_print
        data.result = result
        data.approve_time = datetime.now()  # strftime('%Y-%m-%d %H:%M:%S', localtime())
        aun_db.session.add(data)
        aun_db.session.commit()

    return 'ok!!'


@material.route('/modal/', methods=['POST'])
@login_required
@action_permission.require(403)
def modal():
    id = request.form.get('id')
    type = request.form.get('type')
    modal_type = request.form.get('modal_type')
    data = types[type][0].query.filter_by(id=int(id)).first_or_404()
    context = make_context(data, type)
    template = '/modal/'+'modal-' + type + '.html'
    return render_template(template, data=data, context=context,
                           type=types[type][1], modal_type=modal_type)
