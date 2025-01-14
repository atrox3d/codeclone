import json
import repos

data = {}
root = '~/code'

repos.save_to_json('repos.json', root, 'python', relative=True)

# print(repos.load_from_json('repos.json'))

