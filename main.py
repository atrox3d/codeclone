import json
import repos

data = {}
root = '~/code'

# repos.save_to_json('repos.json', root, relative=True)

# print(repos.load_from_json('repos.json'))

data = repos.load_from_json('repos.json')
descriptor = repos.get_descriptor(data)
data = repos.get_data(data)

reps = repos.parse(data, descriptor)

print(json.dumps(reps, indent=2))