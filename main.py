import json
import repos

data = {}
root = '~/code'

# repos.save('repos.json', root, relative=True)

data = repos.load('repos.json')
repos.restore(data, '~/code')
