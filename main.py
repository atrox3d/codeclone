import json
import repos

data = {}
root = '~/code'

# for repo in repos.scan(root, relative=True):
    # data = repos.add_to_dict(repo, data)
    # repos.add_remote(repo, data, root)
# 
# with open('repos.json', 'w') as fp:
    # json.dump(data, fp, indent=2)
# 
# 
repos.save_to_json('repos.json', root, relative=True)


