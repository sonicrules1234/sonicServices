import socket, time, traceback, json
class sonicServices :
    def __init__(self, **kwargs) :
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servername = kwargs["servername"]
        self.inpass = kwargs["inpass"]
        self.outpass = kwargs["outpass"]
        self.rhost = kwargs["remote host"]
        self.port = kwargs["remote port"]
        self.sid = kwargs["sid"]
        self.buff = ""
    def prettify(self, line) :
        if not line.startswith("CAPAB") :
            words = line.split(" ")
            if words[0].lower() == "server" :
                self.authServer(words)
            if len(words) >= 4 :
                if words[1].lower() == "ping" :
                    self.qsend("PONG %s %s" % (words[3], words[2]))
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
        if words[2] == self.inpass :
            self.qsend("BURST %d" % (time.time()))
            self.qsend("VERSION :SonicServices")
            self.qsend("UID %sAAAAAA %d sonicServices %s %s services 127.0.0.1 %d +iosw +ACKNOQcdfgklnoqtx :sonicServices" % (self.sid, time.time(), self.servername, self.servername, time.time()))
            self.qsend("FJOIN #services %d + :o,%sAAAAAA" % (time.time(), self.sid))
            self.qsend("ENDBURST %d" % (time.time()))
            self.qsend("SVSMODE #services +o %sAAAAAA" % (self.sid))
    def connect(self) :
        self.sock.connect((self.rhost, self.port))
        self.onConnect()
    def onConnect(self) :
        self.send("""
CAPAB START
CAPAB MODULES m_allowinvite.so,m_alltime.so,m_auditorium.so,m_banexception.so,m_blockcaps.so,m_blockcolor.so,m_botmode.so,m_callerid.so,m_cban.so,m_censor.so,m_chanfilter.so, m_chanprotect.so,m_chghost.so,m_chgident.so,m_chgname.so,m_cloaking.so,m_commonchans.so,m_dccallow.so,m_deaf.so,m_delayjoin.so,m_filter.so,m_globalload.so,m_globops.so, m_hidechans.so,m_hideoper.so,m_invisible.so,m_inviteexception.so,m_joinflood.so,m_kicknorejoin.so,m_knock.so,m_messageflood.so,m_nickflood.so,m_nicklock.so,m_noctcp.so
CAPAB MODULES m_nokicks.so,m_nonicks.so,m_nonotice.so,m_operchans.so,m_permchannels.so,m_redirect.so,m_remove.so,m_sajoin.so,m_samode.so,m_sanick.so,m_sapart.so,m_saquit.so, m_services_account.so,m_servprotect.so,m_sethost.so,m_setident.so,m_setname.so,m_showwhois.so,m_shun.so,m_silence.so,m_stripcolor.so,m_svshold.so,m_swhois.so,m_timebans.so, m_watch.so
CAPAB CAPABILITIES :NICKMAX=32 HALFOP=1 CHANMAX=65 MAXMODES=20 IDENTMAX=12 MAXQUIT=256 MAXTOPIC=308 MAXKICK=256 MAXGECOS=129 MAXAWAY=201 IP6NATIVE=0 IP6SUPPORT=1 PROTOCOL=1201 CHALLENGE=a%%'ski?#-uo1y5u'kka PREFIX=(qaohv)~&@%%+ CHANMODES=Ibeg,k,FJLfjl,ABCDGKMNOPQRSTcimnpstu SVSPART=1
CAPAB END
SERVER %(servername)s %(password)s 0 %(sid)s :sonicServices
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
instance = sonicServices(**mykwargs)
instance.connect()
