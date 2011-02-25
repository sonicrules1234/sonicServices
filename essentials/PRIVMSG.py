import traceback
minlevel = 1
arguments = ["self", "line", "world", "words"]
keyword = "PRIVMSG"
def main(self, line, world, words) :
    if words[2] == self.sid + "AAAAAA" :
        message = " ".join(words[3:])[1:]
        args = message.split(" ")
        sender = words[0][1:]
        if args[0] == "rehash" :
            self.rehash()
            self.sendnotice(sender, "Rehashed")
        if world.plugins.has_key(args[0].lower()) :
            for plugin in world.plugins[args[0].lower()] :
                arguments = eval(", ".join(plugin["arguments"]))
        #            if self.allowed(info, plugin["minlevel"]) and args[0].lower() in self.users["channels"][info["channel"]]["enabled"] :
                try :
                    plugin["function"](*arguments)
                except :
                    self.error = traceback.format_exc()
        #            self.msg(info["channel"], "Error")
                    print self.error

