# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""


class Department(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    hospital_id = Column(Integer, ForeignKey('hospital.id'))
    hospital = relationship('Hospital')

    def __repr__(self):
        return self.hospital.name + self.name


class Hospital(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return self.name


class DeviceBrand(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return self.name


class DeviceType(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    device_brand_id = Column(Integer, ForeignKey('device_brand.id'))
    device_brand = relationship('DeviceBrand')

    def __repr__(self):
        return self.device_brand.name + self.name


class Device(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    no = Column(String(255), nullable=False)
    apm_id = Column(String(50), nullable=False)
    department_id = Column(Integer, ForeignKey('department.id'))
    device_type_id = Column(Integer, ForeignKey('device_type.id'))
    department = relationship('Department')
    device_type = relationship('DeviceType')
