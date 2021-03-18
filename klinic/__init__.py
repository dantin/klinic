# -*- coding: utf-8 -*-
"""Package's main module!"""

from flask import Flask, current_app
from werkzeug.local import LocalProxy


app: Flask = current_app
conf = LocalProxy(lambda: current_app.config)
