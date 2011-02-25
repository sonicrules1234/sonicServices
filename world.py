import shelve
usermap = {}
nicks = {}
plugins = {}
userdb = shelve.open("userdb.db", writeback=True)
chandb = shelve.open("chandb.db", writeback=True)
hooks = {}
