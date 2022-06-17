import os
import sys

from mac_maker import cli
from multiprocessing import freeze_support, set_start_method

freeze_support()
set_start_method('spawn')
os.environ['SSL_CERT_FILE'] = os.path.join(sys._MEIPASS, 'lib', 'cert.pem')
cli.cli()
