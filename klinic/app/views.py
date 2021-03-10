# -*- coding: utf-8 -*-

from flask import render_template
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_babel import lazy_gettext as _

from . import appbuilder, db
from .models import Device, Hospital, Department, DeviceBrand, DeviceType


class DeviceModelView(ModelView):
    datamodel = SQLAInterface(Device)

    list_columns = [
        'no',
        'name',
        'department.hospital.name',
        'department',
        'device_type',
    ]

    base_order = ('id', 'asc')

    show_fieldsets = [
        ('Summary', {'fields': ['no', 'name']}),
        (
            'Device Info',
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


class HospitalModelView(ModelView):
    datamodel = SQLAInterface(Hospital)
    related_views = [
        DepartmentModelView,
    ]
    list_title = _('List Hospital')


class DeviceTypeModelView(ModelView):
    datamodel = SQLAInterface(DeviceType)
    list_columns = ['device_brand.name', 'name']


class DeviceBrandModelView(ModelView):
    datamodel = SQLAInterface(DeviceBrand)
    related_views = [
        DeviceTypeModelView,
    ]


"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html",
            base_template=appbuilder.base_template,
            appbuilder=appbuilder
        ),
        404,
    )


db.create_all()

appbuilder.add_view(
    HospitalModelView,
    'List Hospital',
    icon='fa-folder-open-o',
    label=_('Hospital List'),
    category='Organizations',
    category_icon='fa-envelope',
    category_label=_('Organization Management'),
)
appbuilder.add_view(
    DepartmentModelView,
    'List Department',
    icon='fa-envelope',
    label=_('Department List'),
    category='Organizations',
    category_label=_('Organization Management'),
)
appbuilder.add_view(
    DeviceModelView,
    'List Device',
    icon='fa-envelope',
    label=_('Device List'),
    category='Devices',
    category_icon='fa-envelope',
    category_label=_('Device Management'),
)
appbuilder.add_view(
    DeviceBrandModelView,
    'List Device Brand',
    icon='fa-envelope',
    label=_('Device Brand List'),
    category='Meta',
    category_icon='fa-envelope',
    category_label=_('Meta Management'),
)
appbuilder.add_view(
    DeviceTypeModelView,
    'List Device Type',
    icon='fa-envelope',
    label=_('Device Type List'),
    category='Meta',
    category_label=_('Meta Management'),
)
