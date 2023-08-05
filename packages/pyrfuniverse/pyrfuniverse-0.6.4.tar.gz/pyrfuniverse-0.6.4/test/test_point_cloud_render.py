import json
import os.path

import numpy as np
from pyrfuniverse.envs.base_env import RFUniverseBaseEnv

main_path = 'E:/rfuniverse/rfuniverse/Build/Grasp/RFUniverse_Data/StreamingAssets/grasp'
point_path = os.path.join(main_path, 'point_list')
survive_path = os.path.join(main_path, 'survive_list')
index = 561
with open(os.path.join(point_path, f'scene_{str(index).zfill(4)}.json'), 'r', encoding='utf8') as fp:
    point_data = json.load(fp)
with open(os.path.join(survive_path, f'scene_{str(index).zfill(4)}.json'), 'r', encoding='utf8') as fp:
    survive_data = json.load(fp)

point = []
for i in point_data:
    for j in range(len(point_data[i])):
        if i == 'ground' or survive_data[i][j]:
            point.append(point_data[i][j])

point = np.array(point).reshape(-1, 3)
print(point.shape)
color = point.copy()

env2 = RFUniverseBaseEnv(executable_file='@Editor',)
env2.asset_channel.set_action(
    "InstanceObject",
    name='PointCloud',
    id=123456
)
env2.instance_channel.set_action(
    "ShowPointCloud",
    id=123456,
    positions=point.reshape(-1).tolist(),
    colors=point.reshape(-1).tolist(),
)
env2.instance_channel.set_action(
    "SetRadius",
    id=123456,
    radius=0.01
)
while 1:
    env2._step()