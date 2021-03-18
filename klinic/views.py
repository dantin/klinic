# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_babel import lazy_gettext as _

from .models import Device, Hospital, Department, DeviceBrand, DeviceType


class DeviceModelView(ModelView):
    datamodel = SQLAInterface(Device)
    list_title = _('List Device')
    show_title = _('Show Device')
    add_title = _('Add Device')
    edit_title = _('Edit Device')

    list_columns = [
        'no',
        'name',
        'department.hospital.name',
        'department',
        'device_type',
    ]

    label_columns = {
        'no': _('Device No.'),
        'name': _('Device Name'),
        'department.hospital.name': _('Hospital Name'),
        'department': _('Department'),
        'device_type': _('Device Type'),
        'apm_id': _('APM ID'),
    }

    base_order = ('id', 'asc')

    show_fieldsets = [
        (
            _('Summary'),
            {'fields': ['no', 'name']}
        ),
        (
            _('Device Info'),
            {
                'fields': [
                    'no',
                    'name',
                    'apm_id',
                ],
                'expanded': False,
            },
        ),
    ]


class DepartmentModelView(ModelView):
    datamodel = SQLAInterface(Department)
    list_columns = ['hospital.name', 'name']
    list_title = _('List Department')
    show_title = _('Show Department')
    add_title = _('Add Department')
    edit_title = _('Edit Department')

    label_columns = {
        'hospital.name': _('Hospital Name'),
        'name': _('Department Name'),
    }


class HospitalModelView(ModelView):
    datamodel = SQLAInterface(Hospital)
    related_views = [
        DepartmentModelView,
    ]
    list_title = _('List Hospital')
    show_title = _('Show Hospital')
    add_title = _('Add Hospital')
    edit_title = _('Edit Hospital')

    label_columns = {
        'name': _('Hospital Name'),
    }


class DeviceTypeModelView(ModelView):
    datamodel = SQLAInterface(DeviceType)
    list_columns = ['device_brand.name', 'name']
    list_title = _('List Device Type')
    show_title = _('Show Device Type')
    add_title = _('Add Device Type')
    edit_title = _('Edit Device Type')
    label_columns = {
        'device_brand.name': _('Device Brand Name'),
        'name': _('Device Type'),
    }


class DeviceBrandModelView(ModelView):
    datamodel = SQLAInterface(DeviceBrand)
    related_views = [
        DeviceTypeModelView,
    ]
    list_title = _('List Device Brand')
    show_title = _('Show Device Brand')
    add_title = _('Add Device Brand')
    edit_title = _('Edit Device Brand')
    label_columns = {
        'name': _('Device Brand'),
    }
