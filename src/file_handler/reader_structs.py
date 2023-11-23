'''
ALL THE IMPORTANT CONSTANTS TO CONSTRACT KEYWORDS FROM DIFFERENT FILES!
'''
GEO_FILE_LINES = {
    0: 'aerogel_b1',
    1: 'aerogel_b2',
    2: 'aerogel_b3',
    3: 'frontal_mirror_b1',
    4: 'frontal_mirror_b2',
    5: 'planar_mirror_a2l',
    6: 'planar_mirror_a2r',
    7: 'planar_mirror_a3',
    8: 'planar_mirror_a1l',
    9: 'planar_mirror_a1r',
    10: 'spherical_mirror_s1',
    11: 'spherical_mirror_s2',
    12: 'spherical_mirror_s3',
    13: 'spherical_mirror_s4',
    14: 'spherical_mirror_s2c',
    15: 'spherical_mirror_s3c',
    16: 'spherical_mirror_s4c',
    17: 'spherical_mirror_s5',
    18: 'spherical_mirror_s5c',
    19: 'spherical_mirror_s6',
    20: 'mapmt'
}

GEO_FILE_EUCLIDE_PARAMS = {
    0: 'x',
    1: 'y',
    2: 'z'
}

GEO_FILE_ANGLE_PARAMS = {
    0: 'theta_x',
    1: 'theta_y',
    2: 'theta_z'
}

VARIATION_FILE_LINES = {
    0: 'mapmt',
    201: 'aerogel_0',
    202: 'aerobel_1',
    203: 'aerogel_2_1',
    204: 'aerogel_2_2',
    301: 'plannar_mirror',
    302: 'shperical_mirror',
    401: 'full'
}

VARIATION_PARAMS = {
    0: 'x',
    1: 'y',
    2: 'z',
    3: 'theta_x',
    4: 'theta_y',
    5: 'theta_z',
}


AERO_FILE_AEROGEL_LINES = {
    0: 'aerogel_b1',
    1: 'aerogel_b2',
    2: 'aerogel_b3'
}

AERO_FILE_TOPOLOGY_LINES = {
    0: 'dp',
    1: 'a2l',
    2: 'a2r',
    3: 'a3',
    4: 'a1l',
    5: 'a1r',
    6: 'other',
    10: 's1_b1',
    11: 's2_b1',
    12: 's3_b1',
    13: 's4_b1',
    14: 's2c_b1',
    15: 's3c_b1',
    16: 's4c_b1',
    17: 's5_b1',
    18: 's5c_b1',
    19: 's6_b1',
    20: 's1_b2',
    21: 's2_b2',
    22: 's3_b2',
    23: 's4_b2',
    24: 's2c_b2',
    25: 's3c_b2',
    26: 's4c_b2',
    27: 's5_b2',
    28: 's5c_b2',
    29: 's6_b2'
}

AERO_FILE_PARAMS = {
    0: 'mean',
    1: 'mean_err',
    2: 'std',
    3: 'std_err',
    4: 'entries',
    5: 'chi2'
}

OPT_FILE_LINES = {
    0: 'aerogel_b1',
    1: 'aerogel_b2',
    2: 'aerogel_b3',
    3: 'frontal_mirror_b1',
    4: 'frontal_mirror_b2',
    5: 'planar_mirror_a2l',
    6: 'planar_mirror_a2r',
    7: 'planar_mirror_a3',
    8: 'planar_mirror_a1l',
    9: 'planar_mirror_a1r',
    10: 'spherical_mirror_s1',
    11: 'spherical_mirror_s2',
    12: 'spherical_mirror_s3',
    13: 'spherical_mirror_s4',
    14: 'spherical_mirror_s2c',
    15: 'spherical_mirror_s3c',
    16: 'spherical_mirror_s4c',
    17: 'spherical_mirror_s5',
    18: 'spherical_mirror_s5c',
    19: 'spherical_mirror_s6',
    20: 'mapmt'
}

OPT_FILE_PARAMS = {
    0: 'ref_index',
    1: 'Npe',
    2: 'smearing',
    3: 'efficiency',
    4: 'avg_hits'
}

TOP_FILE_PARAMS = {
    0: 'entries',
    1: 'mean',
    2: 'mean_err',
    3: 'std',
    4: 'std_err',
    5: 'chi2'
}

TOP_FILE_NAMES = [
    'dir',
    'planA1L',
    'planA1R',
    'planA2L',
    'planA2R',
    'planA3',
    'spheS10B1',
    'spheS10B2',
    'spheS1B1',
    'spheS1B2',
    'spheS2B1',
    'spheS2B2',
    'spheS3B1',
    'spheS3B2',
    'spheS4B1',
    'spheS4B2',
    'spheS5B1',
    'spheS5B2',
    'spheS6B1',
    'spheS6B2',
    'spheS7B1',
    'spheS7B2',
    'spheS8B1',
    'spheS8B2',
    'spheS9B1',
    'spheS9B2'
]

TRACKS_PARAMS = {
    0: 'nevents',   
    1: 'mean',
    2: 'mean_err',
    3: 'std',
    4: 'std_err',
    5: 'chi2' 
}
