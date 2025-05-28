import os
import sys

from mac_maker import cli
from multiprocessing import freeze_support
from pathlib import Path

freeze_support()
os.putenv('SSL_CERT_FILE', (Path(sys._MEIPASS) / 'lib' / 'cert.pem').resolve())
WORKER_FLAG = Path(sys._MEIPASS) / "worker_process"

if not WORKER_FLAG.exists():
  WORKER_FLAG.touch()
  cli.cli()
else:
  sys.argv = sys.argv[1:]
  exec(open(sys.argv[0]).read())
