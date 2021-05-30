from mac_maker import cli
from multiprocessing import freeze_support, set_start_method

freeze_support()
set_start_method('spawn')
cli.cli()
