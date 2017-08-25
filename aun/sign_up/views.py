# -*-coding:utf-8 -*-
"""
register the rest api
"""
from aun.sign_up.apply import ApplicantApi, ApplicantsApi, ApplicantsDownloadApi
from aun import aun_api

aun_api.add_resource(ApplicantApi, "/api/sign-up/<string:id>")
aun_api.add_resource(ApplicantsApi, "/api/sign-up")
aun_api.add_resource(ApplicantsDownloadApi, "/api/sign-up/download")
