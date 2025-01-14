import json
import repos

data = {}
root = '~/code'

# repos.save_to_json('repos.json', root, relative=True)

# print(repos.load_from_json('repos.json'))




data = repos.load_from_json('repos.json')
repos.restore(data, '~/code')