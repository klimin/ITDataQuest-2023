from config import conf, config
from flask import Flask
from flask_bootstrap import Bootstrap
from datetime import datetime
import logging
import os
from flask_moment import Moment


bootstrap = Bootstrap()
moment = Moment()

def create_app(config_name):
    if os.name == 'nt':
        import ctypes
        kernel32 = ctypes.WinDLL('kernel32')
        hStdOut = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
        mode.value |= 4
        kernel32.SetConsoleMode(hStdOut, mode)

    # Create 'logs' folder
    if not os.path.exists(conf.log_path):
        os.makedirs(conf.log_path)

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)

    cur_date_time = datetime.utcnow().strftime("%Y-%m-%d_%H%M%S")
    logging.basicConfig(filename=conf.log_path + '\\flask_' + cur_date_time + '.log',
                        level=logging.DEBUG,
                        format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    # Debug Toolbar Extension
    if app.debug:
        try:
            from flask_debugtoolbar import DebugToolbarExtension
            debug_toolbar = DebugToolbarExtension()
            debug_toolbar.init_app(app)
        except:
            pass

    from .general import general as general_blueprint
    app.register_blueprint(general_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix ='/')

    return app
