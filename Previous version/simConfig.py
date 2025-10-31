"""
NetPyNE Simulation Configuration - Fernando Borges Style
Yao et al. 2022 Human L2/3 Model
"""

from netpyne import specs

cfg = specs.SimConfig()

#==============================================================================
# Simulation parameters
#==============================================================================

cfg.duration = 2000  # 2 seconds
cfg.dt = 0.025       # 40 kHz sampling
cfg.hParams = {
    'v_init': -70,   # Initial voltage
    'celsius': 34    # Temperature (physiological)
}
cfg.verbose = False
cfg.printPopAvgRates = True
cfg.printRunTime = 0.1

#==============================================================================
# Recording
#==============================================================================

cfg.recordCells = ['all']
cfg.recordTraces = {
    'V_soma': {
        'sec': 'soma',
        'loc': 0.5,
        'var': 'v'
    }
}

cfg.recordStim = True
cfg.recordStep = 0.1

#==============================================================================
# Saving
#==============================================================================

cfg.filename = 'Yao_100cell_output'
cfg.saveFolder = 'data'
cfg.savePickle = True
cfg.saveJson = False
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']

#==============================================================================
# Analysis and plotting
#==============================================================================

cfg.analysis = {
    'plotRaster': {
        'include': ['all'],
        'saveFig': True,
        'showFig': False,
        'popRates': True,
        'orderInverse': True,
        'timeRange': [0, 2000],
        'figSize': (12, 8),
        'fontSize': 12
    },
    'plotTraces': {
        'include': [0, 1, 80, 85, 92, 95],  # Sample from each pop
        'saveFig': True,
        'showFig': False,
        'timeRange': [0, 2000],
        'figSize': (14, 10)
    },
    'plotConn': {
        'include': ['all'],
        'saveFig': True,
        'showFig': False,
        'groupBy': 'pop',
        'figSize': (10, 10)
    },
    '2Dnet': {
        'saveFig': True,
        'showFig': False,
        'figSize': (10, 10)
    }
}
