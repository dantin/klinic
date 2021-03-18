# -*- coding: utf-8 -*-
import logging
import os

from flask import Flask, render_template
from flask_babel import lazy_gettext as _

from klinic.extensions import (
    APP_DIR,
    appbuilder,
    db,
    migrate,
)
from klinic.utils.core import pessimistic_connection_handling


logger = logging.getLogger(__name__)


def create_app() -> Flask:
    app = Flask(__name__)

    try:
        # Allow user to override config completely.
        config_module = os.environ.get('KLINIC_CONFIG', 'klinic.config')
        app.config.from_object(config_module)

        app_initializer = app.config.get('APP_INITIALIZER', KlinicAppInitializer)(app)
        app_initializer.init_app()

        return app
    except Exception as ex:
        logger.exception('Failed to create app')
        raise ex


class KlinicAppInitializer:
    def __init__(self, app: Flask) -> None:
        super().__init__()

        self.flask_app = app
        self.config = app.config

    def init_app(self) -> None:
        """
        Main entry point which will delegate to other methods in
        order to fully init the app.
        """
        self.setup_db()
        self.configure_logging()
        with self.flask_app.app_context():
            self.init_app_in_ctx()

    def configure_logging(self) -> None:
        self.config['LOGGING_CONFIGURATOR'].configure_logging(
            self.config, self.flask_app.debug)

    def setup_db(self) -> None:
        db.init_app(self.flask_app)

        with self.flask_app.app_context():
            pessimistic_connection_handling(db.engine)

        migrate.init_app(self.flask_app, db=db, directory=APP_DIR + '/migrations')

    def init_app_in_ctx(self) -> None:
        self.configure_fab()
        self.init_views()

    def configure_fab(self) -> None:
        if self.config['SILENCE_FAB']:
            logging.getLogger('flask_appbuilder').setLevel(logging.ERROR)
        appbuilder.init_app(self.flask_app, db.session)

    def init_views(self) -> None:
        db.create_all()
        from klinic.views import (
            HospitalModelView,
            DepartmentModelView,
            DeviceModelView,
            DeviceBrandModelView,
            DeviceTypeModelView,
        )

        appbuilder.add_view(
            HospitalModelView,
            'List Hospital',
            icon='fa-hospital-o',
            label=_('Hospital List'),
            category='Organizations',
            category_icon='fa-sitemap',
            category_label=_('Organization Management'),
        )
        appbuilder.add_view(
            DepartmentModelView,
            'List Department',
            icon='fa-medkit',
            label=_('Department List'),
            category='Organizations',
            category_label=_('Organization Management'),
        )
        appbuilder.add_view(
            DeviceModelView,
            'List Device',
            icon='fa-tachometer',
            label=_('Device List'),
            category='Devices',
            category_icon='fa-server',
            category_label=_('Device Management'),
        )
        appbuilder.add_view(
            DeviceBrandModelView,
            'List Device Brand',
            icon='fa-book',
            label=_('Device Brand List'),
            category='Meta',
            category_icon='fa-cubes',
            category_label=_('Meta Management'),
        )
        appbuilder.add_view(
            DeviceTypeModelView,
            'List Device Type',
            icon='fa-tags',
            label=_('Device Type List'),
            category='Meta',
            category_label=_('Meta Management'),
        )
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
