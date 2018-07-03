from pyworkflow.plugin import Plugin
from bibtex import _bibtex  # Load bibtex dict with references

import os

MAGDIST_HOME_VAR = 'MAGDIST_HOME'
SUMMOVIE_HOME = 'SUMMOVIE_HOME'
UNBLUR_HOME = 'UNBLUR_HOME'
FREALIGN_HOME_VAR = 'FREALIGN_HOME'
CTFFIND4_HOME = 'CTFFIND4_HOME'
CTFFIND_HOME = 'CTFFIND_HOME'


class GrigoriefflabPlugin(Plugin):

    def __init__(self):
        configVars = {MAGDIST_HOME_VAR: os.path.join(os.environ['EM_ROOT'], 'mag_distortion-1.0.1'),
                      SUMMOVIE_HOME: os.path.join(os.environ['EM_ROOT'], 'summovie-1.0.2'),
                      UNBLUR_HOME: os.path.join(os.environ['EM_ROOT'], 'unblur-1.0.2'),
                      FREALIGN_HOME_VAR: os.path.join(os.environ['EM_ROOT'], 'frealign-9.07'),
                      CTFFIND4_HOME: os.path.join(os.environ['EM_ROOT'], 'ctffind4-4.1.10'),
                      CTFFIND_HOME: os.path.join(os.environ['EM_ROOT'], 'ctffind-3.6'),
                      }
        Plugin.__init__(self, 'scipion_grigoriefflab',
                              version="1.0.0b5",
                              logo="brandeis_logo.png",
                              configVars=configVars,
                              bibtex=_bibtex)

    def registerPluginBinaries(self, env):
        env.addPackage('ctffind', version='3.6',
                       tar='ctffind_V3.5.tgz')

        env.addPackage('ctffind4', version='4.0.15',
                       tar='ctffind_V4.0.15.tgz')

        env.addPackage('ctffind4', version='4.1.5',
                       tar='ctffind_V4.1.5.tgz')

        env.addPackage('ctffind4', version='4.1.8',
                       url="http://scipion.cnb.csic.es/downloads/scipion/software/em/ctffind_V4.1.8.tgz",
                       tar='ctffind_V4.1.8.tgz',
                       )

        env.addPackage('ctffind4', version='4.1.10',
                       default=True,  # Optional: install this binary by default
                       tar='ctffind4-4.1.10.tgz')

        env.addPackage('summovie', version='1.0.2',
                       tar='summovie_1.0.2.tgz')

        env.addPackage('unblur', version='1.0.15',
                       url="http://scipion.cnb.csic.es/downloads/scipion/software/em/unblur_1.0_150529.tgz",
                       tar='unblur_1.0_150529.tgz',
                       default=True  # Optional: install this binary by default
                       )

        env.addPackage('unblur', version='1.0.2',
                       tar='unblur_1.0.2.tgz')

        env.addPackage('frealign', version='9.07',
                       default=True,  # Optional: install this binary by default
                       tar='frealign_v9.07.tgz')

        env.addPackage('mag_distortion', version='1.0.1',
                       default=True,  # Optional: install this binary by default
                       tar='mag_distortion-1.0.1.tgz')


_plugin = GrigoriefflabPlugin()

