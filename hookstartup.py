import imp, glob, os, traceback

def main(self, world) :
    world.loaded = True
    for x in glob.glob("essentials/*.py") :
        plugin = imp.load_source(x.replace("essentials\\", "").replace("essentials/", "").replace(".py", ""), x)
        self.addHook(plugin.keyword, plugin, plugin.minlevel, plugin.arguments)
    #hookOldPlugins(self, world)
    hookPlugins(self, world)

def hookPlugins(self, world) :
    plugins = {}
    for filename in glob.glob("plugins/*.pyc") :
        os.remove(filename)
    for plugin in glob.glob("plugins/*.py") :
        if plugin != "plugins/__init__.py" and plugin != "plugins\\__init__.py" :
            plugins[plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", "")] = imp.load_source(plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", ""), plugin)
    for plugin in plugins.keys() :
        x = plugins[plugin]
        x.startup(addHookPlugin, self.addHook, world)

def addHookPlugin(world, keyword, function, minlevel, arguments) :
    try :
        if not world.plugins.has_key(keyword) :
            world.plugins[keyword.lower()] = []
        docs = function.__doc__
        docs = docs.replace("\r", "")
        lines = docs.split("\n")
        helpstring = lines[0]
        detailedhelp = "\n".join(lines[1:])
        world.plugins[keyword.lower()].append({"minlevel":minlevel, "arguments":arguments, "function":function, "syntax":helpstring, "detailedhelp":detailedhelp})
    except : traceback.print_exc()
