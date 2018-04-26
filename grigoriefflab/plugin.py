from pyworkflow.plugin import Plugin
import os

MAGDIST_HOME_VAR = 'MAGDIST_HOME'
SUMMOVIE_HOME = 'SUMMOVIE_HOME'
UNBLUR_HOME = 'UNBLUR_HOME'
FREALIGN_HOME_VAR = 'FREALIGN_HOME'
CTFFIND4_HOME = 'CTFFIND4_HOME'
CTFFIND_HOME = 'CTFFIND_HOME'

VARS = {
    MAGDIST_HOME_VAR: os.path.join(os.environ['EM_ROOT'], 'mag_distortion-1.0.1'),
    SUMMOVIE_HOME: os.path.join(os.environ['EM_ROOT'], 'summovie-1.0.2'),
    UNBLUR_HOME:   os.path.join(os.environ['EM_ROOT'], 'unblur-1.0.2'),
    FREALIGN_HOME_VAR: os.path.join(os.environ['EM_ROOT'], 'frealign-9.07'),
    CTFFIND4_HOME: os.path.join(os.environ['EM_ROOT'], 'ctffind4-4.1.8'),
    CTFFIND_HOME:  os.path.join(os.environ['EM_ROOT'], 'ctffind-3.6'),

}

def registerPluginBinaries(env):
    env.addPackage('ctffind', version='3.6',
                   tar='ctffind_V3.5.tgz')

    env.addPackage('ctffind4', version='4.0.15',
                   tar='ctffind_V4.0.15.tgz')

    env.addPackage('ctffind4', version='4.1.5',
                   tar='ctffind_V4.1.5.tgz')

    env.addPackage('ctffind4', version='4.1.8',
                   tar='ctffind_V4.1.8.tgz',
                   default=True  # Optional: install this binary by default
                   )

    env.addPackage('summovie', version='1.0.2',
                   tar='summovie_1.0.2.tgz')

    env.addPackage('unblur', version='1.0.15',
                   tar='unblur_1.0_150529.tgz')

    env.addPackage('unblur', version='1.0.2',
                   tar='unblur_1.0.2.tgz')

    env.addPackage('frealign', version='9.07',
                   tar='frealign_v9.07.tgz')

    env.addPackage('mag_distortion', version='1.0.1',
                   tar='mag_distortion-1.0.1.tgz')


_plugin = Plugin('grigoriefflab',
                 version="1.0.0",
                 configVars=VARS,
                 logo="brandeis_logo.png",
                 registerFunction=registerPluginBinaries)