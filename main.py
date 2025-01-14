import json
import repos

d = {}
root = '~/code'

for repo in repos.scan(root, True):
    d = repos.add_to_dict(repo, d)
    repos.add_remote(repo, root, d)

with open('repos.json', 'w') as fp:
    json.dump(d, fp, indent=2)
