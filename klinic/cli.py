# -*- coding: utf-8 -*-

import logging
from typing import Any, Dict

import click
from flask.cli import FlaskGroup, with_appcontext

from klinic import app
from klinic.app import create_app
from klinic.extensions import db


logger = logging.getLogger(__name__)


def normalize_token(token_name: str) -> str:
    return token_name.replace('_', '-')


@click.group(
    cls=FlaskGroup,
    create_app=create_app,
    context_settings={'token_normalize_func': normalize_token},
)
@with_appcontext
def cli() -> None:
    """This is a management script for the Klinic application."""
    @app.shell_context_processor
    def make_shell_context() -> Dict[str, Any]:
        return dict(app=app, db=db)


if __name__ == '__main__':
    cli()
