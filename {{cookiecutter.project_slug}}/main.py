import os
import sys

from flask import Flask, render_template

from empty import Empty

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_PATH, "apps"))


class App(Empty):
    def configure_views(self):
        @self.route('/')
        def index():
            return render_template('index.html')


def config_str_to_obj(cfg):
    if isinstance(cfg, str):
        module = __import__('config', fromlist=[cfg])
        return getattr(module, cfg)
    return cfg


def app_factory(config, app_name, blueprints=None):
    # you can use Empty directly if you wish
    app = App(app_name, template_folder=os.path.join(PROJECT_PATH, 'templates'))
    config = config_str_to_obj(config)

    app.configure(config)
    app.add_blueprint_list(blueprints or config.BLUEPRINTS)
    app.setup()

    return app
