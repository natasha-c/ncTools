class NcToolboxGlobals(object):

    def __getattr__(self, attr):
        return None

ncToolboxGlobals = NcToolboxGlobals()
