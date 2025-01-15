import json
import repo

data = {}
root = '~/code'
json_path = 'repos.json'

repo.backup(json_path, root, relative=True)

repo.restore(json_path, '~/code')
