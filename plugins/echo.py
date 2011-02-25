def startup(addPluginHook, addHook, world) :
    addPluginHook(world, "echo", main, 1, ["self", "sender", "message", "args", "world"])
def main(self, sender, message, args, world) :
    """/msg sonicServices echo <message>
Will reply to you the message"""
    self.sendnotice(sender, " ".join(args[1:]))
