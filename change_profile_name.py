#!/usr/bin/env python3

import os
import json
import argparse
from lib.chromium import get_chromium_profiles_path
from lib.helpers import get_browsers

list_browser_name_based_chromium = ['chrome', 'Chrome Canary', 'Chromium', 'Brave', 'Edge']

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--browser', type=str, default='chrome', help='Browser name', 
    choices=list_browser_name_based_chromium, required=True)
parser.add_argument('-bb', '--browser-base', type=str, default='chromium', help='Browser base name')
parser.add_argument('-n', '--name', type=str, help='Profile name', required=True)
parser.add_argument('-i', '--index', type=int, help='Profile index', required=True)

args = parser.parse_args()
browser_name = args.browser
browser_name_index = list_browser_name_based_chromium.index(browser_name)
browser_base_name = args.browser_base
profile_name = args.name
profile_index = args.index

home = os.path.expanduser("~")
supported_browsers = get_browsers()

browser_chrome = get_browsers()[browser_base_name][browser_name_index]
path_profile = "{}/{}".format(home, browser_chrome['path'])
profile = get_chromium_profiles_path(browser_chrome, path_profile)

file_path_profile = profile[profile_index]
with open(file_path_profile) as f:
    data = json.load(f)

user_name_old = data['profile']['name']
data['profile']['name'] = profile_name
user_name_new = data['profile']['name']

print('Old profile name: {}'.format(user_name_old))
print('New profile name: {}'.format(user_name_new))

with open(file_path_profile, 'w') as f:
    json.dump(data, f)