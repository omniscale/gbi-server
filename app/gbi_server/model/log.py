# This file is part of the GBI project.
# Copyright (C) 2013 Omniscale GmbH & Co. KG <http://omniscale.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import shapely
import datetime

from sqlalchemy.orm import backref
from geoalchemy2.types import Geometry
from geoalchemy2.shape import to_shape

from gbi_server.extensions import db


class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=backref('logs', cascade="all,delete,delete-orphan"))

    action = db.Column(db.String(24), nullable=False)
    geometry = db.Column(Geometry('MULTIPOLYGON', srid=4326))
    format = db.Column(db.String)
    srs = db.Column(db.String)
    mapping = db.Column(db.String)
    source = db.Column(db.String)
    layer = db.Column(db.String)
    zoom_level_start = db.Column(db.Integer)
    zoom_level_end = db.Column(db.Integer)
    refreshed = db.Column(db.Boolean)

    @property
    def geometry_as_geojson(self):
        if self.geometry is not None:
            geom = json.dumps(
                shapely.geometry.mapping(to_shape(self.geometry))
            )
            return geom
        return False


class SearchLog(db.Model):
    __tablename__ = 'search_logs'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=backref('search_logs', cascade="all,delete,delete-orphan"))


class SearchLogGeometry(db.Model):
    __tablename__ = 'search_log_geometries'

    id = db.Column(db.Integer, primary_key=True)

    search_log_id = db.Column(db.Integer, db.ForeignKey('search_logs.id'), nullable=False)
    search_log = db.relationship('SearchLog', backref=backref('geometries', cascade="all,delete,delete-orphan"))

    geometry = db.Column(Geometry('POLYGON', srid=3857))
    identifier = db.Column(db.String)

