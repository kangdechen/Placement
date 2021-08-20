import splitfolders

import os

os.makedirs('output')
os.makedirs('output/train')
os.makedirs('output/val')

audio_loc = 'data/images/apple_pie'

splitfolders.ratio(audio_loc, output='output', seed=1337, ratio=(0.8, 0.2))
