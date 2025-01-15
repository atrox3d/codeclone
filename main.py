import json
import repos

data = {}
root = '~/code'
json_path = 'repos.json'

repos.backup(json_path, root, relative=True)

repos.restore(json_path, '~/code')
