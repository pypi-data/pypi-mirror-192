# python setup.py sdist bdist_wheel

import os
from om_py.python_to_om import to_om, lispify, om_print
#from om_py.musicxml2om import musicxml2om
from om_py.score import add_dots, names2ratio, notes_divisions, fix_min_pulses, fix_nested_tuplets, check_the_var, remove_the_var, list_depth, ckn_notes, om_pulse, om_group, om_measure, om_voice, om_part
from om_py.om_functions import om_scale, f2mc, mc2f, approx_mc
from om_py.neimog import FreqsInsideRange, FreqsAndAmps_InsideRange


