import json
from pathlib import Path
from lostark.lostark_tools import datum_parser
import tqdm

LOGDIR = 'accessory_logs/_202221822205'

log_dir = Path(LOGDIR)
all_names = list(log_dir.iterdir())
total_logs = {
    '팔찌' : [],
    '귀걸이' : [],
    '반지' : [],
    '목걸이' : [],
}
dup_counts = 0
for logpath in tqdm.tqdm(all_names):
    with open(logpath, 'r') as f:
        raw_log = json.load(f)
    no_copies = [raw_log[0]]
    for r in raw_log[1:]:
        duplicated = False
        for nc in no_copies:
            if r[0]==nc[0] and r[3]==nc[3]:
                duplicated=True
                dup_counts+=1
                break
        if not duplicated:
            no_copies.append(r)
    for nc in tqdm.tqdm(no_copies,leave=False):
        parsed = datum_parser(nc)
        dup=False # For the very first item
        # Scan at most 25000 items
        for t in total_logs[parsed['acc_type']][-25000:]:
            dup=True
            for k, v in t.items():
                if parsed[k] != v:
                    dup=False
                    break
            if dup:
                dup_counts += 1
                break
        if not dup:
            total_logs[parsed['acc_type']].append(parsed)

print(f'total {dup_counts}items duplicated')
print(f"목걸이: {len(total_logs['목걸이'])} 귀걸이: {len(total_logs['귀걸이'])} 반지: {len(total_logs['반지'])}")
output_name = '_'.join([str(i) for i in raw_log[0][0]])

for a_t, l in total_logs.items():
    with open(output_name+a_t+'.json','w') as f:
        json.dump(l,f)