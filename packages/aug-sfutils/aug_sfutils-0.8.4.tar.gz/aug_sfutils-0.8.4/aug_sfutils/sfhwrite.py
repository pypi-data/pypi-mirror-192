import logging
from struct import pack
import numpy as np
from aug_sfutils import sfmap, str_byt
from aug_sfutils.sfmap import ostruc, oattr, header_sfmt

logger = logging.getLogger('aug_sfutils.sfhwrite')
#logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)


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
        param = np.atleast_1d(param)
        for jitem in range(n_items):
            if len(param[jitem]) > 0:
                byt[18 + jitem*dlen: 18 + (jitem+1)*dlen] = param[jitem].ljust(dlen)
    elif dfmt in sfmap.dtf['SFfmt'].values: # number
        if dfmt == 7: # logical, bug if n_items > 1?
            byt[16: 22] = pack('>?2x?1x?', param.dmin, param.dmax, param)
        else:
            byt[16: 16+2*type_len] = pack('>2%s' %sfmt, param.dmin, param.dmax)
            param = np.atleast_1d(param)
            for jitem in range(n_items):
                byt[16 + (jitem+2)*type_len: 16 + (jitem+3)*type_len] = pack('>%s' %sfmt, param[jitem])

    return byt


def set_signals(sffull):

# SIGNALS list generated automatically, override input entry
    sigs = type('', (), {})()
    sigs.nitems = len(sffull.properties.objects)
    sigs.address = len(sffull.properties.SFobjects)*128
    sigs.length = sigs.nitems*2
    sigs.dataFormat = 3
    sfmt = sfmap.typeMap('SFfmt', 'struc', sigs.dataFormat)
    objid = [sfo.objid for sfo in sffull.properties.SFobjects if sfo.objectName in sffull.properties.objects]
    byt_objlist = pack('>%d%s' %(sigs.nitems, sfmt), *objid)
    bytlen = len(byt_objlist)
    dj0 = str_byt.next8(bytlen)
    sigs.objlist = bytearray(dj0)
    sigs.objlist[:bytlen] = byt_objlist

    return sigs


def set_length_address(sffull):

# ParSets

    len_psets = 0
    for sfo in sffull.properties.SFobjects: # sequence not important
        if sfo.SFOtypeLabel == 'ParamSet':
            sfo.length = parset_length(sfo.data)
            len_psets += sfo.length

# Set lengths and addresses

    sigs = set_signals(sffull)

    addr_diag = sigs.address + sigs.length + len_psets
    par_addr  = sigs.address + sigs.length 
    addr_diag = str_byt.next8(addr_diag)
    par_addr  = str_byt.next8(par_addr)

    addr = addr_diag

    for sfo in sffull.properties.SFobjects:

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
                for key, val in sigs.__dict__.items():
                    sfo.__dict__[key] = val
                addr = addr_diag
        elif SFOlbl in ('Device', 'ParamSet'):
            sfo.address = par_addr
            par_addr += sfo.length
        elif SFOlbl == 'Signal':
            sfo.length = sfmap.objectLength(sfo)
            sfo.address = addr
            addr += str_byt.next8(sfo.length)
        elif SFOlbl == 'TimeBase':
            sfo.length = sfmap.objectLength(sfo)
            sfo.address = addr
            addr += str_byt.next8(sfo.length)
        elif SFOlbl == 'SignalGroup':
            shape_arr = np.array(sfo.index[::-1][:sfo.num_dims])
            sfo.length = sfmap.objectLength(sfo)
            sfo.address = addr
            n_block = 2*((sfo.length + 7)//8)
            addr += n_block*((sfo.length + n_block-1)//n_block) + shape_arr[1]*2
        elif SFOlbl == 'AreaBase':
            sfo.length = sfmap.objectLength(sfo)
            sfo.address = addr
            addr += 8*((sfo.length + 9)//8)
        else:
            continue

        logger.debug('Address in, out: %d %d', addr_in, sfo.address)
        logger.debug('Length  in, out: %d %d', len_in , sfo.length )

    len_tot = addr + sfo.length + addr_diag

    len_in = sfodiag.length
    sfodiag.length = len_tot
    logger.debug('Length  in, out: %d %d', len_in , sfodiag.length )

    return sffull


def write_sfh(sffull_in, fout):
# Write SFH file

    sffull = set_length_address(sffull_in)
    f = open(fout, 'wb')

    len_sfh = 0
    for sfo in sffull.properties.SFobjects:
# Encode all attributes into byte strings(128)
        sfhbytes = SFH_WRITE(sfo)
        f.write(sfhbytes)
        len_sfh += len(sfhbytes)

# Write SIGNALS list

    sigs = sffull.SIGNALS
    f.write(sigs.objlist)
    len_sfh += len(sigs.objlist)

# Write content of ParSets
    for sfo in sffull.properties.SFobjects:
         if sfo.SFOtypeLabel == 'ParamSet':
            pset2byt = bytearray(parset_length(sfo.data))
            j0 = 0
            for pname, param in sfo.data.items():
                p2b = par2byt(pname, param)
                j1 = j0 + len(p2b)
                pset2byt[j0: j1] = p2b
                j0 = j1
            f.write(pset2byt)
    f.close()
    logger.info('Stored binary %s' %fout)


def SFH_WRITE(sfo):
    """
    Writes a generic SFH object metadata to a byte string
    """

    val = bytearray(24)

    SFOlbl = sfo.SFOtypeLabel
    sfmt = ostruc[SFOlbl]

    SFOlist = []
    for SFOattr in sfmap.oattr[SFOlbl]:
        SFOlist.append(getattr(sfo, SFOattr))
    val = pack(sfmt, *tuple(SFOlist))

    objectName = str_byt.to_byt(sfo.objectName)
    descr      = str_byt.to_byt(sfo.descr)

    byte_str = pack(header_sfmt, objectName.ljust(8), sfo.objectType, sfo.level, sfo.status, \
        sfo.errcode, *sfo.rel, sfo.address, sfo.length, val, descr.ljust(64))

    return byte_str
