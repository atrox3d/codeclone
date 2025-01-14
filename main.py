import repos

for repo in repos.scan('~/code', True):
    print(repo)