"""
registe the rest api
"""

from aun import aun_api

from aun.data_station.data_station import DataStationApi, DataStationsApi, DataDownloadApi

aun_api.add_resource(DataStationApi, "/api/data-station/<file_id>")
aun_api.add_resource(DataStationsApi, "/api/data-station")
aun_api.add_resource(DataDownloadApi, "/api/data-station/<file_id>/download")
