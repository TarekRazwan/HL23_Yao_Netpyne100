"""
cfg.py 
Complete simulation configuration for Yao et al. L2/3 human cortical microcircuit
100-cell replica using NetPyNE

Based on: Fernando's L23 model + Yao's biophysics
"""

from netpyne import specs
import os

cfg = specs.SimConfig()  

#------------------------------------------------------------------------------
# SIMULATION CONFIGURATION
#------------------------------------------------------------------------------
cfg.simType = 'Yao_L23_100cell'
cfg.coreneuron = False

#------------------------------------------------------------------------------
# Run parameters
#------------------------------------------------------------------------------
cfg.duration = 2000.0           # Duration of simulation, in ms  
cfg.dt = 0.025                  # Internal integration timestep
cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
cfg.hParams = {'celsius': 34, 'v_init': -80}  
cfg.verbose = False
cfg.createNEURONObj = True
cfg.createPyStruct = True  
cfg.cvode_active = False
cfg.cache_efficient = True
cfg.printRunTime = 0.1

cfg.includeParamsLabel = False
cfg.printPopAvgRates = True
cfg.checkErrors = False

#------------------------------------------------------------------------------
# Network size
#------------------------------------------------------------------------------
cfg.scale = 1.0
cfg.sizeY = 3300.0              # Column height (um)
cfg.sizeX = 250.0               # Column radius (um) 
cfg.sizeZ = 250.0

#------------------------------------------------------------------------------
# Cell populations (100 cells total, matching Yao et al. proportions)
#------------------------------------------------------------------------------
cfg.allpops = ['HL23PYR', 'HL23SST', 'HL23PV', 'HL23VIP']

# Population sizes (total = 100)
# Yao ratios: PYR ~80%, SST ~8%, PV ~6%, VIP ~6%
cfg.cellNumber = {
    'HL23PYR': 80,      # Excitatory pyramidal
    'HL23SST': 8,       # Somatostatin interneurons
    'HL23PV': 6,        # Parvalbumin interneurons
    'HL23VIP': 6        # VIP interneurons
}

#------------------------------------------------------------------------------
# Recording 
#------------------------------------------------------------------------------
cfg.recordCells = [(pop, 0) for pop in cfg.allpops]  # Record first cell of each type

cfg.recordTraces = {
    'V_soma': {'sec': 'soma_0', 'loc': 0.5, 'var': 'v'},
}

cfg.recordStim = False			
cfg.recordTime = False  		
cfg.recordStep = 0.1            

#------------------------------------------------------------------------------
# Saving
#------------------------------------------------------------------------------
cfg.simLabel = 'Yao_L23_100cell'
cfg.saveFolder = 'output'
cfg.savePickle = False         	
cfg.saveJson = True	           	
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams']
cfg.backupCfgFile = None 		
cfg.gatherOnlySimData = False	
cfg.saveCellSecs = True			
cfg.saveCellConns = True	

#------------------------------------------------------------------------------
# Analysis and plotting 
#------------------------------------------------------------------------------
cfg.analysis['plotRaster'] = {
    'include': cfg.allpops, 
    'saveFig': True, 
    'showFig': False, 
    'orderInverse': True, 
    'timeRange': [0, cfg.duration], 
    'figSize': (14, 8), 
    'fontSize': 12, 
    'lw': 2, 
    'markerSize': 8, 
    'marker': '|', 
    'dpi': 300
}

cfg.analysis['plotTraces'] = {
    'include': cfg.recordCells, 
    'oneFigPer': 'cell', 
    'overlay': False, 
    'timeRange': [0, cfg.duration], 
    'saveFig': True, 
    'showFig': False, 
    'figSize': (14, 10)
}

cfg.analysis['plot2Dnet'] = {
    'include': cfg.allpops, 
    'saveFig': True, 
    'showFig': False,
    'figSize': (12, 12), 
    'fontSize': 10
}

cfg.analysis['plotConn'] = {
    'include': cfg.allpops,
    'saveFig': True,
    'showFig': False,
    'figSize': (10, 10)
}

#------------------------------------------------------------------------------
# Connectivity (from Circuit_param.xls)
#------------------------------------------------------------------------------
cfg.addConn = True

# Synaptic strength multipliers (for tuning E/I balance)
cfg.EEGain = 1.0    # E -> E
cfg.EIGain = 1.0    # E -> I
cfg.IEGain = 1.0    # I -> E
cfg.IIGain = 1.0    # I -> I

#------------------------------------------------------------------------------
# Background stimulation (NetStim inputs)
#------------------------------------------------------------------------------
cfg.addBackground = True

# Background rates (Hz) for each cell type
cfg.backgroundRate = {
    'HL23PYR': 100.0,
    'HL23SST': 100.0,
    'HL23PV': 100.0,
    'HL23VIP': 100.0
}

# Background weights (synaptic strength)
cfg.backgroundWeight = {
    'HL23PYR': 0.0002,
    'HL23SST': 0.0002,
    'HL23PV': 0.0005,
    'HL23VIP': 0.0004
}

#------------------------------------------------------------------------------
# Current clamp (for testing individual cells)
#------------------------------------------------------------------------------
cfg.addIClamp = False

cfg.IClamp1 = {
    'pop': 'HL23PYR',  
    'sec': 'soma_0', 
    'loc': 0.5, 
    'start': 500, 
    'dur': 500, 
    'amp': 0.2
}

#------------------------------------------------------------------------------
# External stimulation (TMS/tACS - disabled for basic model)
#------------------------------------------------------------------------------
cfg.addExternalStimulation = False
"""
cfg.py 
Simulation configuration for Yao et al. L2/3 human cortical microcircuit
100-cell replica using NetPyNE

Based on: Fernando's L23 model + Yao's biophysics
"""

from netpyne import specs
import os

cfg = specs.SimConfig()  

#------------------------------------------------------------------------------
# SIMULATION CONFIGURATION
#------------------------------------------------------------------------------
cfg.simType = 'Yao_L23_100cell'
cfg.coreneuron = False

#------------------------------------------------------------------------------
# Run parameters
#------------------------------------------------------------------------------
cfg.duration = 2000.0           # Duration of simulation, in ms  
cfg.dt = 0.025                  # Internal integration timestep
cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
cfg.hParams = {'celsius': 34, 'v_init': -80}  
cfg.verbose = False
cfg.createNEURONObj = True
cfg.createPyStruct = True  
cfg.cvode_active = False
cfg.cache_efficient = True
cfg.printRunTime = 0.1

cfg.includeParamsLabel = False
cfg.printPopAvgRates = True
cfg.checkErrors = False

#------------------------------------------------------------------------------
# Network size
#------------------------------------------------------------------------------
cfg.scale = 1.0
cfg.sizeY = 3300.0              # Column height (um)
cfg.sizeX = 250.0               # Column radius (um) 
cfg.sizeZ = 250.0

#------------------------------------------------------------------------------
# Cell populations (100 cells total, matching Yao et al. proportions)
#------------------------------------------------------------------------------
cfg.allpops = ['HL23PYR', 'HL23SST', 'HL23PV', 'HL23VIP']

# Population sizes (total = 100)
# Yao ratios: PYR ~80%, SST ~8%, PV ~6%, VIP ~6%
cfg.cellNumber = {
    'HL23PYR': 80,      # Excitatory pyramidal
    'HL23SST': 8,       # Somatostatin interneurons
    'HL23PV': 6,        # Parvalbumin interneurons
    'HL23VIP': 6        # VIP interneurons
}

#------------------------------------------------------------------------------
# Recording 
#------------------------------------------------------------------------------
cfg.recordCells = [(pop, 0) for pop in cfg.allpops]  # Record first cell of each type

cfg.recordTraces = {
    'V_soma': {'sec': 'soma_0', 'loc': 0.5, 'var': 'v'},
}

cfg.recordStim = False			
cfg.recordTime = False  		
cfg.recordStep = 0.1            

#------------------------------------------------------------------------------
# Saving
#------------------------------------------------------------------------------
cfg.simLabel = 'Yao_L23_100cell'
cfg.saveFolder = 'output'
cfg.savePickle = False         	
cfg.saveJson = True	           	
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams']
cfg.backupCfgFile = None 		
cfg.gatherOnlySimData = False	
cfg.saveCellSecs = True			
cfg.saveCellConns = True	

#------------------------------------------------------------------------------
# Analysis and plotting 
#------------------------------------------------------------------------------
cfg.analysis['plotRaster'] = {
    'include': cfg.allpops, 
    'saveFig': True, 
    'showFig': False, 
    'orderInverse': True, 
    'timeRange': [0, cfg.duration], 
    'figSize': (14, 8), 
    'fontSize': 12, 
    'lw': 2, 
    'markerSize': 8, 
    'marker': '|', 
    'dpi': 300
}

cfg.analysis['plotTraces'] = {
    'include': cfg.recordCells, 
    'oneFigPer': 'cell', 
    'overlay': False, 
    'timeRange': [0, cfg.duration], 
    'saveFig': True, 
    'showFig': False, 
    'figSize': (14, 10)
}

cfg.analysis['plot2Dnet'] = {
    'include': cfg.allpops, 
    'saveFig': True, 
    'showFig': False,
    'figSize': (12, 12), 
    'fontSize': 10
}

cfg.analysis['plotConn'] = {
    'include': cfg.allpops,
    'saveFig': True,
    'showFig': False,
    'figSize': (10, 10)
}

#------------------------------------------------------------------------------
# Connectivity (from Circuit_param.xls)
#------------------------------------------------------------------------------
cfg.addConn = True

# Synaptic strength multipliers (for tuning E/I balance)
cfg.EEGain = 1.0    # E -> E
cfg.EIGain = 1.0    # E -> I
cfg.IEGain = 1.0    # I -> E
cfg.IIGain = 1.0    # I -> I

#------------------------------------------------------------------------------
# Background stimulation (NetStim inputs)
#------------------------------------------------------------------------------
cfg.addBackground = True

# Background rates (Hz) for each cell type
cfg.backgroundRate = {
    'HL23PYR': 100.0,
    'HL23SST': 100.0,
    'HL23PV': 100.0,
    'HL23VIP': 100.0
}

# Background weights (synaptic strength)
cfg.backgroundWeight = {
    'HL23PYR': 0.0002,
    'HL23SST': 0.0002,
    'HL23PV': 0.0005,
    'HL23VIP': 0.0004
}

#------------------------------------------------------------------------------
# Current clamp (for testing individual cells)
#------------------------------------------------------------------------------
cfg.addIClamp = False

cfg.IClamp1 = {
    'pop': 'HL23PYR',  
    'sec': 'soma_0', 
    'loc': 0.5, 
    'start': 500, 
    'dur': 500, 
    'amp': 0.2
}

#------------------------------------------------------------------------------
# External stimulation (TMS/tACS - disabled for basic model)
#------------------------------------------------------------------------------
cfg.addExternalStimulation = False