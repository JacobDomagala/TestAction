import datetime
import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import matplotlib.dates as dates
import argparse
from github import Github
import requests
import os
import numpy as np
import wget

BUILD_TIME = "50min"
BADGE_COLOR = "green"

url = f'https://img.shields.io/badge/vt:develop%20build%20time-{BUILD_TIME}-{BADGE_COLOR}.svg'

print(f'Beginning file {url}')
#wget.download(url)

r = requests.get(url)
open('google.svg', 'wb').write(r.content)
