import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Conf(object):
    site_title = "IT&Data Quest 2023"
    version = 'v.1.8.10'
    site_copyright = '(c) 2022 by Andrey KLIMIN'

    log_path = 'logs'
    log_filename = 'flask.log'

    last_stage = 23

    god_mode = False            # Allow to skip stages using ?stage=X parameter
    show_progress = True        # Show Dan'IT Quest progress bar
    show_pagination = False     # Show pagination for all stages
    show_wrong_answers = True   # Show total wrong answers counter in Hall of Fame (All data)
    show_email = True           # Show E-Mail addresses in Hall of Fame

    db = "data/danquest2023.db"

    url_bugreport = 'https://forms.office.com/r/8Tbif4qKtU'
    url_feedback = 'https://forms.office.com/r/2XFe8gfgSJ'

class BaseConfig(object):
    DEBUG = False

    SECRET_KEY = 'B2crL4wLpdJrSzKvMfGsSNnuCCj7adGLDByiEDBPA'
    PERMANENT_SESSION_LIFETIME = timedelta(days=365)
    SESSION_COOKIE_NAME = 'session_Danquest2023'

    # Flask bootstrap settings
    BOOTSTRAP_SERVE_LOCAL = True

    @staticmethod
    def init_app(app):
        pass


class ProdConfig(BaseConfig):
    pass

class DevConfig(BaseConfig):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True

    # Debug toolbar
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
    DEBUG_TB_HOSTS = ('127.0.0.1', '192.168.1.55')
    DEBUG_TB_PANELS = ['flask_debugtoolbar.panels.versions.VersionDebugPanel',
                       'flask_debugtoolbar.panels.timer.TimerDebugPanel',
                       'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
                       'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
                       'flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel',
                       'flask_debugtoolbar.panels.template.TemplateDebugPanel',
                       'flask_debugtoolbar.panels.logger.LoggingPanel',
                       'flask_debugtoolbar.panels.route_list.RouteListDebugPanel',
                       'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel']

class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False

conf = Conf()

config = {
    'DevConfig': DevConfig,
    'TestConfig': TestConfig,
    'ProdConfig': ProdConfig,

    'default': ProdConfig
}
