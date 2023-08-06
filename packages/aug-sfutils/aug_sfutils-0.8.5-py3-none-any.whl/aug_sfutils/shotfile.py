import os, logging, traceback
from struct import unpack, pack
import numpy as np
from aug_sfutils import sfmap, sfobj, str_byt
from aug_sfutils.sfmap import olbl, ostruc, oattr, header_sfmt

fmt = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s', '%H:%M:%S')

logger = logging.getLogger('aug_sfutils.read')

if len(logger.handlers) == 0:
    hnd = logging.StreamHandler()
    hnd.setFormatter(fmt)
    logger.addHandler(hnd)

logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)

PPGCLOCK = [1e-6, 1e-5, 1e-4, 1e-3]
LOGICAL  = sfmap.typeMap('descr', 'SFfmt', 'LOGICAL')


def getChunk(fname, start, length):
    """Reads the requested byteblock from the binary shotfile"""
    rdata = None
    with open(fname, 'rb') as f:
        f.seek(start)
        rdata = f.read(length)
    return rdata


def param_length(param):

    parmlen = 16 # ParName(=key), unit, dfmt, n_items
    dfmt = param.dataFormat
    bytlen = param.n_items * sfmap.typeLength(dfmt)
    parmlen += 8 * ( (bytlen + 13)//8 )

    return parmlen


def parset_length(pset_d):

    psetlen = 0
    for param in pset_d.values():
        psetlen += param_length(param)

    return psetlen


def par2byt(pname, param):

    dfmt = param.dataFormat
    n_items = param.n_items

    if dfmt in sfmap.fmt2len.keys(): # char variable
        dlen = sfmap.fmt2len[dfmt]
        bytlen = n_items * dlen
        dj0 = 8 * ( (bytlen + 9)//8 ) 
    elif dfmt in sfmap.dtf['SFfmt'].values: # number
        sfmt = sfmap.typeMap('SFfmt', 'struc', dfmt)
        type_len = np.dtype(sfmt).itemsize
        val_len = n_items + 2
        bytlen = val_len * type_len
        dj0 = str_byt.next8(bytlen)
    blen = 16 + dj0
    byt = bytearray(blen)
    byt[  :  8] = str_byt.to_byt(pname.ljust(8))
    byt[ 8: 16] = pack('>4h', param.physunit, dfmt, n_items, param.status)
    if dfmt in sfmap.fmt2len.keys(): # character variable
        byt[16: 17] = param.dmin
        byt[17: 18] = param.dmax
        param2 = np.atleast_1d(param)
        for jitem in range(n_items):
            if len(param[jitem]) > 0:
                byt[18 + jitem*dlen: 18 + (jitem+1)*dlen] = param2[jitem].ljust(dlen)
    elif dfmt in sfmap.dtf['SFfmt'].values: # number
        if dfmt == LOGICAL: # logical, bug if n_items > 1?
            byt[16: 22] = pack('>?2x?1x?', param.dmin, param.dmax, param)
        else:
            byt[16: 16+2*type_len] = pack('>2%s' %sfmt, param.dmin, param.dmax)
            param2 = np.atleast_1d(param)
            byt[16: 16 + (n_items+2)*type_len] = pack('>%d%s' %(2+n_items, sfmt), param.dmin, param.dmax, *param2)
    return byt



class SHOTFILE(dict):


    def __init__(self, sfpath, sfobj=None):

        self.__dict__ = self

        if not os.path.isfile(sfpath):
            logger.error('Shotfile %s not found', sfpath)
            return None

        self.properties = type('', (), {})()
        self.properties.path = sfpath

        if sfobj is None: #read automatically
            self.read_sfh()
            self.set_attributes()
        else: # for SF writin
            for key, val in sfobj.__dict__.items():
                setattr(self, key, val)
            self.sfout = sfpath


    def read_sfh(self, psets=True):
        """Reads a full shotfile header, including the data of ParamSets, Devices, Lists"""

        sfile = self.properties.path

        self.properties.lists   = []
        self.properties.parsets = []
        self.properties.objects = []
        self.properties.objid   = []
        self.properties.SFobjects = []
        self.properties.addrlen = 1

        n_max = 1000
        n_obj = n_max
        self.properties.related = []
        for j in range(n_max):
            sfo = SF_OBJECT(j, self.properties)
            if hasattr(sfo, 'objectType'):
                sfo.objid = j
                onam = str_byt.to_str(sfo.objectName.strip())
                if sfo.SFOtypeLabel == 'Diagnostic':
                    self.properties.shot = sfo.shot_nr
                    if n_obj == n_max: # There might be several diags objects in a SFH
                        n_obj = sfo.num_objs
                self.properties.related.append(onam)
                self.properties.SFobjects.append(sfo)
                self.properties.objid.append(j)
                if sfo.SFOtypeLabel in ('ParamSet', 'Device'):
                    self.properties.parsets.append(onam)
                elif sfo.SFOtypeLabel == 'List':
                    self.properties.lists.append(onam)
                elif sfo.SFOtypeLabel in ('SignalGroup', 'Signal', 'TimeBase', 'AreaBase'):
                    self.properties.objects.append(onam)
                elif sfo.SFOtypeLabel == 'ADDRLEN':
                    self.properties.addrlen = sfmap.addrsizes[sfo.addrlen]
                self.__dict__[onam] = sfo
            if j >= n_obj - 1:
                break


    def set_attributes(self):
        """Sets useful context info for the entire shotfile, plus data for Lists, ParmSets, Devices"""

        for sfo in self.properties.SFobjects:
            sfo.address *= self.properties.addrlen
            sfo.relations  = [self.properties.related[jid]   for jid in sfo.rel if jid != 65535]
            sfo.relobjects = [self.properties.SFobjects[jid] for jid in sfo.rel if jid != 65535]
            if hasattr(sfo, 'dataFormat'):
                if sfo.dataFormat in sfmap.dtf['SFfmt'].values:
                    sfo.dataType = sfmap.typeMap('SFfmt', 'descr', sfo.dataFormat)
            if sfo.SFOtypeLabel == 'List':
                sfo.getData()
                sfo.data = [self.properties.related[jid] for jid in sfo.data]

            elif sfo.SFOtypeLabel in ('Device', 'ParamSet'):
                sfo.getData()
                if sfo.SFOtypeLabel == 'Device':
                    if 'TS06' in sfo.data.keys(): # former get_ts06
                        ts06 = sfo.data['TS06']
                        if ts06 > 1e15:
                            sfo.ts06 = ts06

            elif sfo.SFOtypeLabel in ('Signal', 'SignalGroup'):
                for jrel, robj in enumerate(sfo.relobjects):
# check where the related timebase is
                    if robj.SFOtypeLabel == 'TimeBase':
                        shape_arr = sfo.index[::-1][:sfo.num_dims]
                        nt = robj.n_steps
                        if shape_arr.count(nt) == 1:
                            sfo.time_dim = shape_arr.index(nt)
                        sfo.timebase = robj
                        sfo.time_dim = jrel
# For data calibration
                        if sfo.phys_unit == 'counts':
                            sfo.cal_fac = robj.s_rate
# check where the related areabase is
                    elif robj.SFOtypeLabel == 'AreaBase':
                        sfo.areabase = robj
                        sfo.area_dim = jrel

#----------------
# Writing section
#----------------
    def write_sfh(self):
# Write SFH file

        self.set_length_address()

        f = open(self.sfout, 'wb')
        for sfo in self.properties.SFobjects:
# Encode all attributes into byte strings(128)
            sfo.to_byte()
            f.write(sfo.sfh_byte)

# Write SIGNALS list

        sigs = self.SIGNALS
        f.write(sigs.objlist)

# Write content of ParSets
        for sfo in self.properties.SFobjects:
            if sfo.SFOtypeLabel == 'ParamSet':
                pset2byt = b''
                for pname, param in sfo.data.items():
                    pset2byt += par2byt(pname, param)
                f.seek(sfo.address) # Ensure proper localisation
                f.write(pset2byt)
        f.close()
        logger.info('Stored binary %s' %self.sfout)


    def set_signals(self):

# SIGNALS list generated automatically, override input entry
        self.sigs = type('', (), {})()
        self.sigs.nitems = len(self.properties.objects)
        self.sigs.address = len(self.properties.SFobjects)*128
        self.sigs.length = self.sigs.nitems*2
        self.sigs.dataFormat = 3
        sfmt = sfmap.typeMap('SFfmt', 'struc', self.sigs.dataFormat)
        objid = [sfo.objid for sfo in self.properties.SFobjects if sfo.objectName in self.properties.objects]
        byt_objlist = pack('>%d%s' %(self.sigs.nitems, sfmt), *objid)
        bytlen = len(byt_objlist)
        dj0 = str_byt.next8(bytlen)
        self.sigs.objlist = bytearray(dj0)
        self.sigs.objlist[:bytlen] = byt_objlist


    def set_length_address(self):

# ParSets

        len_psets = 0
        for sfo in self.properties.SFobjects: # sequence not important
            if sfo.SFOtypeLabel == 'ParamSet':
                sfo.length = parset_length(sfo.data)
                len_psets += sfo.length

# Set lengths and addresses

        self.set_signals()

        addr_diag = self.sigs.address + self.sigs.length + len_psets
        par_addr  = self.sigs.address + self.sigs.length 
        addr_diag = str_byt.next8(addr_diag)
        par_addr  = str_byt.next8(par_addr)

        addr = addr_diag

        for sfo in self.properties.SFobjects:

            objectName = sfo.objectName
            SFOlbl     = sfo.SFOtypeLabel
            addr_in    = sfo.address # For debugging
            len_in     = sfo.length  # For debugging
            if hasattr(sfo, 'dataFormat'):
                type_len = sfmap.typeLength(sfo.dataFormat)
            else:
                type_len = 0

            if SFOlbl == 'Diagnostic':
                sfodiag = sfo
                sfo.length = sfo.length # GIT: evaluated at the end of the loop
                sfo.address = addr
            elif SFOlbl == 'List':
                if objectName == 'SIGNALS':
                    for key, val in self.sigs.__dict__.items():
                        setattr(sfo, key, val)
                    addr = addr_diag
            elif SFOlbl in ('Device', 'ParamSet'):
                sfo.address = par_addr
                par_addr += sfo.length
            elif SFOlbl in ('Signal', 'TimeBase', 'SignalGroup', 'AreaBase'):
                sfo.length = sfmap.objectLength(sfo)
                sfo.address = addr
                addr += str_byt.next8(sfo.length)
            else:
                continue

            logger.debug('Address in, out: %d %d', addr_in, sfo.address)
            logger.debug('Length  in, out: %d %d', len_in , sfo.length )

        len_tot = addr + sfo.length + addr_diag
        len_in = sfodiag.length
        sfodiag.length = len_tot
        logger.debug('Length  in, out: %d %d', len_in , sfodiag.length )


class SF_OBJECT:
    """Reads the metadata of a generic SF object (sfo) from the SFH's 128byte string.
    For data, call getData()"""


    def __init__(self, jobj, properties):

        self.properties = properties
        self.sfname = self.properties.path
        byte_str = getChunk(self.sfname, jobj*128, 128)

        objnam, self.objectType, self.level, self.status, self.errcode, *rel, \
            self.address, self.length, val, descr = unpack(header_sfmt, byte_str)

        self.objectName = str_byt.to_str(objnam)
        if not self.objectName:
            logger.error('Error: empty object name')
            return
        self.rel = list(rel)
        self.descr = str_byt.to_str(descr.strip())

        logger.debug('%s %d %d', self.objectName, self.address, self.length)
        logger.debug(self.descr)

        if self.objectType in olbl.keys():
            self.SFOtypeLabel = olbl[self.objectType]
            sfmt = ostruc[self.SFOtypeLabel]
        else:
            sfmt = None
            self.SFOtypeLabel = 'Unknown'

# Read SFheader, plus data for Lists, Devices, ParSets
        SFOlbl = self.SFOtypeLabel
        SFOtup = unpack(sfmt, val)
        for jattr, SFOattr in enumerate(oattr[SFOlbl]):
            setattr(self, SFOattr, SFOtup[jattr])

        if SFOlbl == 'ParamSet':
            self.calibration_type = sfmap.calibLabel[self.cal_type]
        elif SFOlbl in ('SignalGroup', 'Signal'):
            self.index = [self.index1, self.index2, self.index3, self.index4]
            if self.physunit in sfmap.unit_d.keys():
                self.phys_unit = sfmap.unit_d[self.physunit]
            else:
                logger.warning('No phys. unit found for object %s, key=%d', self.objectName, self.physunit)
                self.phys_unit = ''
        elif SFOlbl == 'TimeBase':
            self.timebase_type = sfmap.timebaseLabel[self.tbase_type]
        elif SFOlbl == 'AreaBase':
            self.physunit = [self.physunit1, self.physunit2, self.physunit3]
            self.phys_unit = [sfmap.unit_d[x] for x in self.physunit]
            self.sizes = [self.size_x, self.size_y, self.size_z]


    def getData(self, nbeg=0, nend=None):
        """Stores the data part of a SF object into sfo.data"""

        if self.SFOtypeLabel in ('ParamSet', 'Device'):
            self.getParamSet()
        elif self.SFOtypeLabel == 'List':
            self.getList()
        elif self.SFOtypeLabel in ('TimeBase', 'AreaBase', 'Signal', 'SignalGroup'):
            self.getObject(nbeg=nbeg, nend=nend)


    def getList(self):
        """Stores the object IDs contained in a SF list (such as SIGNALS)"""

        buf = getChunk(self.sfname, self.address, self.length)
        sfmt = sfmap.typeMap('SFfmt', 'struc', self.dataFormat)
        self.data = unpack('>%d%s' %(self.nitems, sfmt), buf) # IDs, not labels


    def getParamSet(self):
        """Returns data and metadata of a Parameter Set.
        Called by default on SFH reading"""

        buf = getChunk(self.sfname, self.address, self.length)

        j0 = 0
        self.data = {}
        logger.debug('PS: %s, addr: %d, n_item: %d, length: %d', self.objectName, self.address, self.nitems, self.length)
        for j in range(self.nitems):
            pname = str_byt.to_str(buf[j0: j0+8])
            meta = type('', (), {})()
            meta.physunit, dfmt, n_items, meta.status = unpack('>4h', buf[j0+8:  j0+16])
            if meta.physunit in sfmap.unit_d.keys():
                meta.phys_unit = sfmap.unit_d[meta.physunit]
            meta.n_items = n_items
            meta.dataFormat = dfmt

            j0 += 16

            if dfmt in sfmap.fmt2len.keys(): # char variable
                dlen = sfmap.fmt2len[dfmt]
                bytlen = n_items * dlen
                meta.dmin = buf[j0  : j0+1]
                meta.dmax = buf[j0+1: j0+2]
                if len(meta.dmin) == 0:
                    meta.dmin = b' '
                if len(meta.dmax) == 0:
                    meta.dmax = b' '
                data = np.chararray((n_items,), itemsize=dlen, buffer=buf[j0+2: j0+2+bytlen])
                dj0 = 8 * ( (bytlen + 9)//8 )
                j0 += dj0
            elif dfmt in sfmap.dtf['SFfmt'].values:
                sfmt = sfmap.typeMap('SFfmt', 'struc', dfmt)
                logger.debug('Numerical par %d', dfmt)
                val_len = n_items + 2
                bytlen = val_len * np.dtype(sfmt).itemsize
                if n_items >= 0:
                    if dfmt == LOGICAL: # Logical, bug if n_items > 1?
                        meta.dmin, meta.dmax, data = unpack('?2x?1x?', buf[j0: j0+6])
                    else:
                        data = np.ndarray((val_len, ), '>%s' %sfmt, buf[j0: j0+bytlen], order='F').copy()
                        meta.dmin = data[0]
                        meta.dmax = data[1]
                        data = np.squeeze(data[2:]) # no array if n_items=1
                dj0 = str_byt.next8(bytlen)
                j0 += dj0
            else: # faulty dfmt
                break

            self.data[pname] = sfobj.SFOBJ(data, sfho=meta)

            if j0 >= self.length:
                break


    def getObject(self, nbeg=0, nend=None):
        """Stores data part of Sig, SigGrou, TimeBase, AreaBase"""

        if hasattr(self, 'nbeg'):
           if self.nbeg == nbeg and self.nend == nend:
               return # do not re-read object if data are there already
        self.nbeg = nbeg
        self.nend = nend
        if self.SFOtypeLabel in ('SignalGroup', 'Signal', 'TimeBase', 'AreaBase'):
            shape_arr = sfmap.arrayShape(self)
        else:
            logger.error('Object %s is no signal, signalgroup, timebase nor areabase, skipping')
            return None

        dfmt = self.dataFormat
        if self.SFOtypeLabel == 'TimeBase' and self.length == 0:
            if self.tbase_type == sfmap.TimebaseType.PPG_prog: # e.g. END:T-LM_END
                self.ppg_time()
            else:   # ADC_intern, e.g. DCN:T-ADC-SL
                self.data = (np.arange(self.n_steps, dtype=np.float32) - self.n_pre)/self.s_rate
        else:
            type_len = sfmap.typeLength(dfmt)
            bytlen = np.prod(shape_arr) * type_len
            if dfmt in sfmap.fmt2len.keys(): # char variable
                self.data = np.chararray(shape_arr, itemsize=type_len, buffer=getChunk(self.sfname, self.address, bytlen), order='F')
            else: # numerical variable
                sfmt = sfmap.typeMap('SFfmt', 'struc', dfmt)
                addr = self.address
# Read data only in the time range of interest
                if self.SFOtypeLabel in ('Signal', 'TimeBase', 'AreaBase') or self.time_last():
                    addr += type_len*nbeg*np.prod(shape_arr[:-1])
                    if nend is None:
                        nend = shape_arr[-1]
                    bytlen = (nend - nbeg)*np.prod(shape_arr[:-1])*type_len
                    shape_arr[-1] = nend - nbeg

                self.data = np.ndarray(shape_arr, '>%s' %sfmt, getChunk(self.sfname, addr, bytlen), order='F')


    def ppg_time(self): # Bug MAG:27204; e.g. END
        """Returns the time-array in [s] for TB of type PPG_prog"""

        nptyp = sfmap.typeMap('SFfmt', 'np', self.dataFormat)
        for robj in self.relobjects:
            if robj.SFOtypeLabel == 'Device':
                ppg = robj.data # Device/ParSet dictionary
                if not 'PRETRIG' in ppg.keys():
                    continue
                if self.n_pre > 0:
                    if ppg['PRETRIG'] > 0:
                        dt = ppg['RESOLUT'][15] * PPGCLOCK[ppg['RESFACT'][15]] + 1e-6
                    else:
                        dt = 0.
                    time_ppg = dt*np.arange(self.n_pre, dtype=nptyp) - dt*self.n_pre
                    start_phase = time_ppg[-1] + dt
                else:
                    time_ppg = []
                    start_phase = 0
                for jphase in range(16):
                    if ppg['PULSES'][jphase] > 0:
                        dt = ppg['RESOLUT'][jphase]*PPGCLOCK[ppg['RESFACT'][jphase]]
                        tb_phase = dt*np.arange(ppg['PULSES'][jphase], dtype=nptyp) + start_phase
                        time_ppg = np.append(time_ppg, tb_phase)
                        start_phase = time_ppg[-1] + dt
                if len(time_ppg) != 0:
                    self.data = time_ppg[:self.n_steps]


    def time_last(self):
        """True if SigGroup has time as last coordinate"""

        if not hasattr(self, 'time_dim'):
            return False
        else:
            return (self.time_dim == self.num_dims-1)


    def to_byte(self):

        SFOlbl = self.SFOtypeLabel
        sfmt = ostruc[SFOlbl]
        SFOlist = []
        for SFOattr in sfmap.oattr[SFOlbl]:
            SFOlist.append(getattr(self, SFOattr))
        val = pack(sfmt, *SFOlist)

        objectName = str_byt.to_byt(self.objectName)
        descr      = str_byt.to_byt(self.descr)

        self.sfh_byte = pack(header_sfmt, objectName.ljust(8), self.objectType, \
            self.level, self.status, self.errcode, *self.rel, self.address, \
            self.length, val, descr.ljust(64))
        
