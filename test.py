import time

from tqdm import tqdm
'''
t = tqdm(range(10))
for i in range(10):
    print(f"hello: {i:0>5}")
for i in t:
    time.sleep(0.1)
    t.set_description(f"hello: {i:0>3}")
    t.write(f"{i}")

for i in tqdm(range(10), position=0, leave=False):
    for j in tqdm(range(2), position=1, leave=False):
        print("1")

t.close()
'''
from pathlib import Path
path_str = Path('/home/nolan/DOCKER_SHARE/whisper/V1_0_0/csv')
file_example = [str(p) for p in path_str.glob('*') if p.suffix in [".json", ".csv"]]
print(file_example)
