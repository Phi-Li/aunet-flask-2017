# -*- coding: utf-8 -*-
from flask import Blueprint

material = Blueprint('material', __name__, url_prefix='/material',
                     static_folder='../static/material', template_folder='../templates/material')

from . import views
