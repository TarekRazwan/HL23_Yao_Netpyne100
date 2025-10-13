"""
NetPyNE Simulation Configuration for Yao et al. 2022 L2/3 Microcircuit Model
"""

from netpyne import specs

# Initialize simulation configuration
simConfig = specs.SimConfig()

#==============================================================================
# Simulation Parameters
#==============================================================================

simConfig.duration = 1000  # Duration of simulation (ms) - 1 second test
simConfig.dt = 0.025  # Internal integration timestep (ms) - same as original
simConfig.hParams = {
    'celsius': 34,  # Temperature (°C)
    'v_init': -80  # Initial membrane potential (mV)
}

simConfig.seeds = {
    'conn': 1,
    'stim': 1,
    'loc': 1
}

simConfig.createNEURONObj = True
simConfig.createPyStruct = True
simConfig.verbose = True

#==============================================================================
# Recording
#==============================================================================

simConfig.recordTraces = {
    'V_soma': {
        'sec': 'soma',
        'loc': 0.5,
        'var': 'v'
    }
}

simConfig.recordCells = ['all']  # Record from all cells
simConfig.recordStims = False
simConfig.recordStep = 0.1  # Step size for recording (ms)

#==============================================================================
# Saving
#==============================================================================

simConfig.filename = 'yao_netpyne_test'
simConfig.saveFolder = 'data'
simConfig.savePickle = True
simConfig.saveJson = False
simConfig.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']

#==============================================================================
# Analysis and Plotting
#==============================================================================

simConfig.analysis = {
    'plotRaster': {
        'saveFig': True,
        'showFig': False,
        'orderBy': 'pop',
        'timeRange': [0, simConfig.duration],
        'figSize': (10, 8),
        'fontSize': 12
    },
    'plotTraces': {
        'include': [0, 1, 2],  # Plot first 3 cells
        'saveFig': True,
        'showFig': False,
        'timeRange': [0, 1000],
        'figSize': (12, 8)
    },
    'plot2Dnet': {
        'saveFig': True,
        'showFig': False,
        'figSize': (8, 8)
    },
    'plotConn': {
        'saveFig': True,
        'showFig': False,
        'figSize': (10, 10)
    }
}

#==============================================================================
# Multi-run Configuration (for parameter exploration)
#==============================================================================

simConfig.checkErrors = True

print("SimConfig configuration complete!")
