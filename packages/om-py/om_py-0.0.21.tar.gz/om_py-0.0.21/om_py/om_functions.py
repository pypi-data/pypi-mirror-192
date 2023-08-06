import math

def om_scale(om_self, minout, maxout, minin=0, maxin=0):
    "return a list of samples between min and max"
    if minin == 0 and maxin == 0:
        minin = min(list)
        maxin = max(list)
    new_scale = []
    if type(om_self) != list:
        om_self = [om_self]
    for index in range(len(om_self)):
        new_scale.append(minout + (((om_self[index] - minin) * (maxout - minout)) / (maxin - minin )))
    return new_scale


def f2mc(freq):
    if isinstance(freq, list):
        return [f2mc(i) for i in freq]
    if isinstance(freq, int) or isinstance(freq, float):
        ref_pitch = 440 
        diferenca_com_A4 =  6900 + (math.log(abs(freq / ref_pitch)) / math.log(2)) * 1200
        return round(diferenca_com_A4, 2)

def mc2f(mc): 
    if isinstance(mc, list):
        return [mc2f(i) for i in mc]
    if isinstance(mc, int) or isinstance(mc, float):
        ref_pitch = 440 
        return ref_pitch * (2 ** ((mc - 6900) / 1200))

def approx_mc(mc, approx=100):
    if isinstance(mc, list):
        return [approx_mc(i, approx) for i in mc]
    if isinstance(mc, int) or isinstance(mc, float):
        return round(mc / approx) * approx 
