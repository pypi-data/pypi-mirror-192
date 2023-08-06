from om_py.om_functions import f2mc
from om_py.score import get_midi_class_of_midicent
    
# ========================================
def FreqsInsideRange(pitches, range_down, range_up):
    ''' It checks if all the pitches are inside the range '''
    if pitches is None or pitches == []:
        return []
    good_pitches = []
    for pitch in pitches:
        midicent = f2mc(pitch)
        midi_alterations = get_midi_class_of_midicent(midicent)[1]
        if midicent < range_up and midicent > range_down:
            good_pitches.append(pitch)
    return good_pitches

# ========================================
def FreqsAndAmps_InsideRange(pitches, amps, range_down, range_up):
    ''' It checks if all the pitches are inside the range '''
    if pitches is None or pitches == []:
        return []
    good_pitches = []
    good_amps = []
    for pitch in pitches:
        midicent = f2mc(pitch)
        midi_alterations = get_midi_class_of_midicent(midicent)[1]
        if midicent < range_up and midicent > range_down:
            good_pitches.append(pitch)
            good_amps.append(amps[pitches.index(pitch)])
    if good_pitches == []:
        return [], []
    else:
        return good_pitches, good_amps 