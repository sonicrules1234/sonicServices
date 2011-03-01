import socket, time, traceback, json, shelve, world, imp, glob, hookstartup, ssl
class sonicServices :
    def __init__(self, **kwargs) :
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servername = kwargs["servername"]
        self.inpass = kwargs["inpass"]
        self.outpass = kwargs["outpass"]
        self.rhost = kwargs["remote host"]
        self.port = kwargs["remote port"]
        self.sid = kwargs["sid"]
        self.ssl = kwargs["ssl"]
        self.buff = ""
        self.bursting = False
        if self.ssl :
            self.sock = ssl.wrap_socket(self.sock)
        hookstartup.main(self, world)
    def sendnotice(self, uid, message) :
        self.send(":%sAAAAAA NOTICE %s :%s" % (self.sid, uid, message))
    def addHook(self, keyword, function, minlevel, arguments) :
        if not world.hooks.has_key(keyword) :
            world.hooks[keyword] = []
        world.hooks[keyword].append({"minlevel":minlevel, "arguments":arguments, "function":function})
    def channelsend(self, channel, message) :
        self.send(":%sAAAAAA PRIVMSG %s :%s" % (self.sid, channel, message))
    def rehash(self) :
#        essentialslist = glob.glob("essentials/*.py")
#        essentialslist.sort()
#        pluginlist = glob.glob("plugins/*.py")
#        pluginlist.sort()
#        essentials = {}
#        plugins = {}
#        for x in essentialslist :
#            essentials[x.replace("essentials\\", "").replace("essentials/", "").replace(".py", "")] = imp.load_source(x.replace("essentials\\", "").replace("essentials/", "").replace(".py", ""), x)
#        for plugin in pluginlist :
#                if plugin != "plugins/__init__.py" and plugin != "plugins\\__init__.py" :
#                    plugins[plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", "")] = imp.load_source(plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", ""), plugin)
        del world.plugins
        del world.hooks
        world.hooks = {}
        world.plugins = {}
        hookstartup.main(self, world)
    def prettify(self, line) :
        if not line.startswith("CAPAB") :
            words = line.split(" ")
            if words[0].lower() == "pass" :
                if words[1] != self.inpass :
                    self.sock.close()
            if words[0].lower() == "server" :
                self.authServer(words)
            if len(words) == 4 :
                if words[1].lower() == "ping" :
                    self.qsend("PONG %s" % (words[2]))
            #if len(line.split(":")[0].strip().split(" ")) == 11 :
            if len(words) > 1: 
                if words[1].lower() == "uid" :
                    serversid = words[0][1:]
                    uid = words[9]
                    nick = words[2]
                    hostname = words[7]
                    ident = words[6]
                    ip = words[8]
                    modes = words[5]
                    realname = " ".join(words[10:])[1:]
                    world.usermap[uid] = nick
                    world.nicks[nick] = {"serversid":serversid, "uid":uid, "hostname":hostname, "ident":ident, "ip":ip, "modes":modes, "realname":realname}
                    print "Added user " + uid
                    if not self.bursting :
                        self.channelsend("#services", "%(nick)s!%(ident)s@%(hostname)s has connected." % dict(nick=nick, ident=ident, hostname=hostname))
                if len(words[0]) == 10 :
                    if words[0][1:] in world.usermap.keys() :
                        senderuid = words[0][1:]
                        sender = world.usermap[senderuid]
                        if words[1].lower() == "privmsg" :
                            if words[2] == self.sid + "AAAAAA" :
                                message = " ".join(words[3:])[1:]
                                #self.runplugins(senderuid, message)
                if words[1].lower() == "endburst" : self.bursting = False
                if words[1].lower() == "burst" : self.bursting = True
                if world.hooks.has_key(words[1]) :
                    for hook in world.hooks[words[1]] :
                        arguments = eval(", ".join(hook["arguments"]))
                        hook["function"].main(*arguments)
                    
#    def runplugins(self, senderuid, message) :
        #Identifying what plugin to run and running it would go here
        #But for now we will just code a built in command, then make an actual plugin once it works
#        args = message.split(" ")
#        if args[0].lower() == "echo" :
#            self.sendnotice(senderuid, " ".join(args[1:]))

    def send(self, message) :
        print "[OUT]%s" % (message)
        self.rawsend(message+"\r\n")
    def rawsend(self, message) :
        self.sock.send(message)
    def qsend(self, message, space=True) :
        if space == True :
            extra = " "
        else: extra = ""
        self.send(":" + self.sid + extra + message)
    def authServer(self, words) :
            #self.qsend("BURST %d" % (time.time()))
            #self.qsend("VERSION :SonicServices")
            self.qsend("UID sonicServices 0 %(timestamp)d +iosw sonicServices %(hostname)s 127.0.0.1 %(sid)sAAAAAA :sonicServices" % (sid=self.sid, timestamp=time.time(), hostname="sonicServices"))
            self.qsend("AAAAAA JOIN %d #services +" % (time.time()), False)
            self.qsend("TMODE %d #services +o" % (time.time()))
            #self.qsend("ENDBURST %d" % (time.time()))
            #self.qsend("SVSMODE #services +o %sAAAAAA" % (self.sid))
    def connect(self) :
        self.sock.connect((self.rhost, self.port))
        self.onConnect()
    def onConnect(self) :
        self.send("""
PASS %(password)s TS 6 %(sid)s
CAPAB :QS EX IE KLN UNKLN ENCAP TB SERVICES EUID EOPMOD
SERVER %(servername)s 1 :sonicServices
""" % dict(servername=self.servername, password=self.outpass, sid=self.sid))
        self.dataReceived()
    def dataReceived(self) :
        try :
            while True :
                data = self.sock.recv(4096)
                lines = data.replace("\r", "").split("\n")
                lines[0] = self.buff + lines[0]
                self.buff = lines[-1]
                lines = lines[:-1]
                for line in lines :
                    if line != "" :
                        print line
                        self.prettify(line)
        except :
            traceback.print_exc()
            self.sock.close()

fileobj = open("conf.json", "r")
config = fileobj.read()
fileobj.close()
config = json.loads(config)
mykwargs = {}
mykwargs["servername"] = config[u"servername"].encode("utf8")
mykwargs["inpass"] = config[u"inpass"].encode("utf8")
mykwargs["outpass"] = config[u"outpass"].encode("utf8")
mykwargs["remote port"] = config[u"port"]
mykwargs["sid"] = config[u"sid"].encode("utf8")
mykwargs["remote host"] = config[u"remote host"].encode("utf8")
mykwargs["ssl"] = config[u"ssl"]
instance = sonicServices(**mykwargs)
instance.connect()
world.userdb.close()
world.chandb.close()
