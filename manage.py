# -*- coding: utf-8 -*-
import logging
from typing import Any, Dict

import click
from colorama import Fore, Style
from flask.cli import FlaskGroup, with_appcontext
from klinic import app
from klinic.app import create_app
from klinic.extensions import db


logger = logging.getLogger(__name__)


def normalize_token(token_name: str) -> str:
    return token_name.replace('_', '-')


# @click.group(
#     context_settings={'token_normalize_func': normalize_token},
# )
@click.group(
    cls=FlaskGroup,
    create_app=create_app,
    context_settings={'token_normalize_func': normalize_token},
)
@with_appcontext
def cli():
    """This is a management script for the Klinic application."""
    @app.shell_context_processor
    def make_shell_context() -> Dict[str, Any]:
        return dict(app=app, db=db)


@cli.command()
@click.option('--listen_addr', default='0.0.0.0:8080', type=str,
              help='listen address, default: 0.0.0.0:8080')
def server(listen_addr):
    """Run backend server"""
    from klinic.app import create_app
    app = create_app()

    run_flask(app, listen_addr)


@cli.command()
@click.option('--verbose', '-v', is_flag=True, help='')
def version(verbose: bool) -> None:
    """Prints the current version number"""
    print(Fore.BLUE + '==' * 15)
    print(
        Fore.YELLOW + 'Klinic ' + Fore.CYAN + '0.1-dev'
    )
    print(Fore.BLUE + '==' * 15)
    if verbose:
        print(f'[DB] : {db.engine}')
    print(Style.RESET_ALL)


def run_flask(app, listen_addr):
    import gunicorn.app.base

    class StandaloneApplication(gunicorn.app.base.BaseApplication):
        def __init__(self, app, options=None):
            self.application = app
            self.options = options or {}
            super(StandaloneApplication, self).__init__()

        def load_config(self):
            _config = dict([(key, val) for key, val in self.options.items()
                            if key in self.cfg.settings and val is not None])
            print(_config)
            for key, val in _config.items():
                self.cfg.set(key.lower(), val)

        def load(self):
            return self.application

    _options = {
        'bind': listen_addr,
        'workers': 4,
        'accesslog': '-',  # log to stdout
        'access_log_format': '%(h)s %(l)s %(t)s "%(r)s" %(s)s "%(a)s"'
    }

    StandaloneApplication(app, _options).run()


if __name__ == '__main__':
    cli()
