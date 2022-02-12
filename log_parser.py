import json
from pathlib import Path
from lostark.lostark_tools import datum_parser

LOGDIR = 'accessory_logs'


log_dir = Path(LOGDIR)

total_logs = []

for logpath in log_dir.iterdir():
    with open(logpath, 'r') as f:
        raw_log = json.load(f)
    no_copies = []
    for r in raw_log:
        