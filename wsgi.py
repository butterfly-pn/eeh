from main import APP
from eeh.views.login import *
from eeh.views.home import *
from eeh.views.settings import *
from eeh.views.add import *
from eeh.views.delete import *
from eeh.views.app import *
from eeh.api.v1 import *

if __name__ == '__main__':
    APP.run(debug=True)
