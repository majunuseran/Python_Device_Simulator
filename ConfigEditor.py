import config as constants
import configparser

class ConfigEditor:

    def __init__(self):
        self.configfile = constants.CONFIG_FILE
        self.firmwareconfigfile = constants.FIRMWARE_CONFIG_FILE
        self.config = configparser.ConfigParser()

    def getValue(self,section,key):
        self.config.read(self.configfile)
        value = ''
        return self.config.get(section,key)
    
    def setValue(self,section,key,value):
        if self.config.has_section(section) == False:
            self.config.add_section(section)
        self.config.set(section,key,value)
        cfgfile = open(self.configfile,'w+')
        self.config.write(cfgfile)
        cfgfile.close()
        
    def getfirmwareValue(self,section,key):
        self.config.read(self.firmwareconfigfile)
        value = ''
        return self.config.get(section,key)
    
    def setfirmwareValue(self,section,key,value):
        if self.config.has_section(section) == False:
            self.config.add_section(section)
        self.config.set(section,key,value)
        cfgfile = open(self.firmwareconfigfile,'w+')
        self.config.write(cfgfile)
        cfgfile.close()
        
#     def ConfigSectionMap(self,section):
#         dict1 = {}
#         options = self.config.options(section)
#         for option in options:
#             try:
#                 dict1[option] = self.config.get(section, option)
#                 if dict1[option] == -1:
#                     DebugPrint("skip: %s" % option)
#             except:
#                 print("exception on %s!" % option)
#                 dict1[option] = None
#         return dict1
            
