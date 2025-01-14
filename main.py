import json
import repos

d = {}
root = '~/code'
for repo in repos.scan(root, True):
    d = repos.add_to_dict(repo, d)
    # print(json.dumps(d, indent=2))
    print('MAIN', repo)
    repos.add_remote(repo, root, d)
    # print(repo, repos.add_remote(repo, root))

print(json.dumps(d, indent=2))
