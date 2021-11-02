import json

class Header:
    def __init__(self, uid, cmd, gw_uid):
        self.UID = uid
        self.CMD = cmd
        self.GW_UID = gw_uid
    def toJSON(self):
        return self.__dict__
#     def toJSON(self):
#         return json.dumps(self.__dict__, cls=ComplexEncoder)
    
class SCG_RCFG_Body:
    def __init__(self, uid, cmd, long_poll_tmout, awaketime_dft, sht_poll_int, dwn_byte, temp, f_ver, h_ver, b_ver):
        self.UID = uid
        self.CMD = cmd 
        self.LONG_POLL_TMOUT = long_poll_tmout
        self.AWAKETIME_DFT = awaketime_dft
        self.SHT_POLL_INT = sht_poll_int
        self.DWN_BYTE = dwn_byte
        self.TEMP = temp
        self.F_VER = f_ver
        self.H_VER = h_ver
        self.B_VER = b_ver
    def toJSON(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)

class SCG_RNET_Body:
    def __init__(self, CMD, UID, DHCP, IP_ADR, SBNET, DNS1, DNS2, GTWY, MAC):
        self.CMD = CMD
        self.UID = UID
        self.DHCP = DHCP
        self.IP_ADR = IP_ADR 
        self.SBNET = SBNET
        self.DNS1 = DNS1
        self.DNS2 = DNS2 
        self.GTWY = GTWY
        self.MAC = MAC
    def toJSON(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)
    
class S_ON_Body:
    def __init__(self, pin, s_id, dur, cmd, uid, tbltxt):
        self.PIN = pin
        self.S_ID = s_id 
        self.DUR = dur
        self.CMD = cmd
        self.UID = uid
        self.TBLTXT = tbltxt
    def toJSON(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)
    
class S_OFF_Body:
    def __init__(self, pin, s_id, dur, cmd, uid, tbltxt):
        self.PIN = pin
        self.S_ID = s_id 
        self.DUR = dur
        self.CMD = cmd
        self.UID = uid
        self.TBLTXT = tbltxt
    def toJSON(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)
    
class SCG_BUSY_Body:
    def __init__(self, UID, DUR, OP, CMD):
        self.UID = UID
        self.DUR = DUR 
        self.OP = OP
        self.CMD = CMD
    def toJSON(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)
    
class CL_FWV_Body:
    def __init__(self, cmd, b_ver, h_ver, f_ver, con_name, con_fver, con_type, con_bver, con_hver, flag, apan, shid, uid, cmd_org):
        self.CMD = cmd
        self.B_VER = b_ver 
        self.H_VER = h_ver
        self.F_VER = f_ver
        self.CON_NAME = con_name
        self.CON_FVER = con_fver
        self.CON_TYPE = con_type
        self.CON_BVER = con_bver 
        self.CON_HVER = con_hver
        self.FLAG = flag
        self.APAN = apan
        self.SHID = shid
        self.UID = uid
        self.CMD_ORG = cmd_org
    def toJSON(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)

class CL_RSCFG_Body:
    def __init__(self, cmd, uid, cmd_org, shid, apan, msg_id, result, serversync, fail_list):
        self.CMD = cmd
        self.UID = uid 
        self.CMD_ORG = cmd_org
        self.SHID = shid
        self.APAN = apan
        self.MSG_ID = msg_id
        self.RESULT = result
        self.SERVERSYNC = serversync 
        self.FAIL_LIST = fail_list
    def toJSON(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)
    
class UL_RSCFG_Body:
    def __init__(self, cmd, uid, scg_result, retry_times, result, fail_list):
        self.CMD = cmd
        self.UID = uid 
        self.SCG_RESULT = scg_result
        self.RETRY_TIMES = retry_times
        self.RESULT = result
        self.FAIL_LIST = fail_list
    def toJSON(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)
    
class CL_RCFG_Body:
    def __init__(self, cmd, cmd_org, msg_id, uid, shid, apan, consync, con_type, f_ver, h_ver, b_ver, con_fever, con_hver, con_bver, r0, r1, r2, r3, r4, r5):
        self.CMD = cmd
        self.CMD_ORG = cmd_org
        self.MSG_ID = msg_id
        self.UID = uid
        self.SHID = shid
        self.APAN = apan
        self.CONSYNC = consync
        self.CON_TYPE = con_type 
        self.F_VER = f_ver
        self.H_VER = h_ver
        self.B_VER = b_ver 
        self.CON_FVER = con_fever
        self.CON_HVER = con_hver
        self.CON_BVER = con_bver 
        self.R0 = r0
        self.R1 = r1
        self.R2 = r2
        self.R3 = r3
        self.R4 = r4
        self.R5 = r5
    def toJSON(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)

class UL_CFG_Body:
    def __init__(self,CMD,APAN,SHID,YR,MO,DAY,HR,MIN,SEC,WKD,TMZ,DST,LAT,LONG,DSK_OFST,DWN_OFST,SS_HR,SS_MIN,SR_HR,SR_MIN,S_ID,SC_1AON,SC_1AOFF,SC_2AON,SC_2AOFF,WKD_A,SC_1BON,SC_1BOFF,SC_2BON,SC_2BOFF,WKD_B,UID,PIN,F_VER,H_VER,B_VER,TEMP,SCH,IS_ON,IS_AUTO_ON,MS_DATA):
        self.CMD = CMD
        self.APAN = APAN
        self.SHID = SHID
        self.YR = YR
        self.MO = MO
        self.DAY = DAY
        self.HR = HR 
        self.MIN = MIN
        self.SEC = SEC
        self.WKD = WKD 
        self.TMZ = TMZ
        self.DST = DST
        self.LAT = LAT 
        self.LONG = LONG
        self.DSK_OFST = DSK_OFST
        self.DWN_OFST = DWN_OFST
        self.SS_HR = SS_HR
        self.SS_MIN = SS_MIN
        self.SR_HR = SR_HR
        self.SR_MIN = SR_MIN        
        self.S_ID = S_ID
        self.SC_1AON = SC_1AON
        self.SC_1AOFF = SC_1AOFF
        self.SC_2AON = SC_2AON
        self.SC_2AOFF = SC_2AOFF
        self.WKD_A = WKD_A        
        self.SC_1BON = SC_1BON
        self.SC_1BOFF = SC_1BOFF
        self.SC_2BON = SC_2BON
        self.SC_2BOFF = SC_2BOFF         
        self.WKD_B = WKD_B                  
        self.UID = UID
        self.PIN = PIN
        self.F_VER = F_VER
        self.H_VER = H_VER
        self.B_VER = B_VER
        self.TEMP = TEMP
        self.SCH = SCH
        self.IS_ON = IS_ON
        self.IS_AUTO_ON = IS_AUTO_ON
        self.MS_DATA = MS_DATA
    def toJSON(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)
    
class AcknowledgeMsg(object):
    def __init__(self, messageId, registration_id, wasSuccess = True, failureCode = 0, commandOrigin = None, typeCode = 0, execTime = 0, responseText = None, includeDiagnostics = False):        
        self.messageId = messageId
        self.wasSuccess = wasSuccess
        self.failureCode = failureCode
        self.commandOrigin = commandOrigin
        self.typeCode = typeCode
        self.execTime = execTime
        self.responseText = responseText
        self.includeDiagnostics = includeDiagnostics
        self.uid = registration_id
    def toJSON(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)

class FirmwareDownloadMsg(object):
    def __init__(self, fileid, seglen, stbyt, uid, includeDiagnostics = False):
        self.fileid = fileid
        self.seglen = seglen
        self.stbyt = stbyt
        self.uid = uid
        self.includeDiagnostics = includeDiagnostics
    def toJSON(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)

class FirmwareUpgradeProgress(object):
    def __init__(self, CMD, PCT, UID, F_VER, H_VER, B_VER, APAN, SHID, FW_STAT, CMD_ORG, UID_ORG):
        self.CMD = CMD
        self.PCT = PCT
        self.UID = UID
        self.F_VER = F_VER
        self.H_VER = H_VER
        self.B_VER = B_VER
        self.APAN = APAN
        self.SHID = SHID
        self.FW_STAT = FW_STAT
        self.CMD_ORG = CMD_ORG
        self.UID_ORG = UID_ORG
    def toJSON(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)

class LPCUDiscoverySignal(object):
    def __init__(self, CMD, S_ID, APAN, SHID, PIN, F_VER, H_VER, B_VER, IS_ON, UID):
        self.CMD = CMD
        self.S_ID = S_ID
        self.APAN = APAN
        self.SHID = SHID
        self.PIN = PIN
        self.F_VER = F_VER
        self.H_VER = H_VER
        self.B_VER = B_VER
        self.IS_ON = IS_ON
        self.UID = UID
    def toJSON(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)

class FirmwareInfo(object):
    def __init__(self, CMD, F_VER, H_VER, B_VER, UID, TRIG, TEMP, SW1, DHCP, IP_ADR, SBNET, DNS1, DNS2, GTWY, MAC):
        self.CMD = CMD
        self.F_VER = F_VER
        self.H_VER = H_VER
        self.B_VER = B_VER
        self.UID = UID
        self.TRIG = TRIG
        self.TEMP = TEMP
        self.SW1 = SW1
        self.DHCP = DHCP
        self.IP_ADR = IP_ADR
        self.SBNET = SBNET
        self.DNS1 = DNS1
        self.DNS2 = DNS2
        self.GTWY = GTWY
        self.MAC = MAC
    def toJSON(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)
    
class LpcuFirmwareInfo(object):
    def __init__(self, CMD, S_ID, APAN, SHID, PIN, F_VER, H_VER, B_VER, IS_ON, UID):
        self.CMD = CMD
        self.S_ID = S_ID
        self.APAN = APAN
        self.SHID = SHID
        self.PIN = PIN
        self.F_VER = F_VER
        self.H_VER = H_VER
        self.B_VER = B_VER
        self.IS_ON = IS_ON
        self.UID = UID       
    def toJSON(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)

class Report(object):
    def __init__(self, header, body):
        self.Header = header
        self.Body = body
    def toJSON(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)
    
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.toJSON()
#         if isinstance(obj, Abc) or isinstance(obj, Doc):
#             return obj.toJSON()
#         else:
#             return json.JSONEncoder.default(self, obj)