import Bio.Seq
import sys
import lib_dzne_data


def data(*, seq, go, end):
    if lib_dzne_data.anyisna(seq, go, end):
        return None
    ans = dict()
    ans['go'] = go
    ans['end'] = end
    ans['seq'] = cut(seq, go, end, strict=True)
    ans['seq-len'] = len(ans['seq'])
    ans['tr'] = tr(ans['seq'])
    ans['tr-len'] = len(ans['tr'])
    ans['contains-stop'] = '*' in ans['tr']
    ans['gravy'] = gravy(ans['tr'])
    return ans



def seq3(seq, go=None, end=None):
    seq = Bio.Seq.Seq(seq)
    seq = cut(seq, go=go, end=end)
    while len(seq) % 3:
        seq += 'N'
    return seq

def cut(seq, go=None, end=None, strict=False):
    if go is not None and end is not None and go > end:
        raise IndexError(f"One cannot cut the seq {ascii(str(seq))} from {go} until {end}! ")
    if go is not None and go < 0:
        if strict:
            raise IndexError(f"The value go={go} will not be accepted! ")
        prefix = 'N' * (0 - go)
        go = None
    else:
        prefix = ""
    if end is not None and end > len(seq):
        if strict:
            raise IndexError(f"The value end={end} will not be accepted (len={len(seq)})! ")
        suffix = 'N' * (len(seq) - end)
        end = None
    else:
        suffix = ""
    if None not in {go, end}:
        if go > end:
            raise IndexError(f"The values go={go} and end={end} are incompatible! ")
    return prefix + seq[go:end] + suffix

def tr(seq, go=None, end=None):
    return str(seq3(seq, go=go, end=end).translate())


def normstr(seq):
    seq = str(seq).upper()
    if len(set(seq) - set("ACGTUN-")):
        raise ValueError(str(set(seq)))
    return seq


def gravy(translation):
    return 0.0
            
    




 
