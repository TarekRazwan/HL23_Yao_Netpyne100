"""
NetPyNE Network Parameters for Yao et al. 2022 L2/3 Microcircuit Model
Conversion from LFPy implementation to NetPyNE
Based on: https://github.com/FernandoSBorges/Human_L23_NetPyNE
"""

from netpyne import specs
import os

# Initialize network parameters
netParams = specs.NetParams()

#==============================================================================
# Import MOD mechanisms
#==============================================================================
# NetPyNE will automatically find mechanisms in current directory or x86_64/
netParams.importCellParamsFromNet = True

#==============================================================================
# Cell Parameters - Using HOC templates instead of direct SWC import
#==============================================================================

# Get absolute paths
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)

# Path to models and morphologies
model_dir = os.path.join(parent_dir, 'models')
morph_dir = os.path.join(parent_dir, 'morphologies')

#------------------------------------------------------------------------------
# HL23PYR - Layer 2/3 Pyramidal Cell
#------------------------------------------------------------------------------
netParams.cellParams['HL23PYR'] = {
    'conds': {'cellType': 'HL23PYR'},
    'secs': {}
}

# Import using HOC template approach
netParams.cellParams['HL23PYR']['cellModel'] = 'HH_reduced'  # Use reduced model for now
netParams.cellParams['HL23PYR']['morphology'] = os.path.join(morph_dir, 'HL23PYR.swc')

# Define soma properties
netParams.cellParams['HL23PYR']['secs']['soma'] = {
    'geom': {
        'diam': 18.8,
        'L': 18.8,
        'Ra': 100,
        'cm': 1
    },
    'mechs': {
        'pas': {'g': 0.0000954, 'e': -80},
        'Ih': {'gbar': 0.000148},
        'SK': {'gbar': 0.000853},
        'CaDynamics': {'gamma': 0.0005, 'decay': 20.0},
        'Ca_LVA': {'gbar': 0.00296},
        'Ca_HVA': {'gbar': 0.00155},
        'K_T': {'gbar': 0.0605},
        'K_P': {'gbar': 0.000208},
        'Kv3_1': {'gbar': 0.0424},
        'NaTg': {'gbar': 0.272, 'vshiftm': 13, 'vshifth': 15, 'slopem': 7},
        'Im': {'gbar': 0.000306}
    },
    'ions': {
        'k': {'e': -85},
        'na': {'e': 50}
    }
}

# Simplified apical dendrite
netParams.cellParams['HL23PYR']['secs']['apic'] = {
    'geom': {
        'diam': 2.0,
        'L': 400,
        'Ra': 100,
        'cm': 2
    },
    'topol': {
        'parentSec': 'soma',
        'parentX': 1.0,
        'childX': 0
    },
    'mechs': {
        'pas': {'g': 0.0000954, 'e': -80},
        'Ih': {'gbar': 0.000148}
    }
}

# Simplified basal dendrite
netParams.cellParams['HL23PYR']['secs']['dend'] = {
    'geom': {
        'diam': 2.0,
        'L': 200,
        'Ra': 100,
        'cm': 2
    },
    'topol': {
        'parentSec': 'soma',
        'parentX': 0,
        'childX': 0
    },
    'mechs': {
        'pas': {'g': 0.0000954, 'e': -80},
        'Ih': {'gbar': 0.000000709}
    }
}

# Simplified axon
netParams.cellParams['HL23PYR']['secs']['axon'] = {
    'geom': {
        'diam': 1.0,
        'L': 100,
        'Ra': 100,
        'cm': 1
    },
    'topol': {
        'parentSec': 'soma',
        'parentX': 0.5,
        'childX': 0
    },
    'mechs': {
        'pas': {'g': 0.0000954, 'e': -80},
        'NaTg': {'gbar': 1.38, 'vshiftm': 0, 'vshifth': 10, 'slopem': 9}
    }
}

#------------------------------------------------------------------------------
# HL23SST - Somatostatin Interneuron (simplified)
#------------------------------------------------------------------------------
netParams.cellParams['HL23SST'] = {
    'conds': {'cellType': 'HL23SST'},
    'secs': {}
}

netParams.cellParams['HL23SST']['secs']['soma'] = {
    'geom': {'diam': 15, 'L': 15, 'Ra': 100, 'cm': 1},
    'mechs': {
        'pas': {'g': 0.0000232, 'e': -81.5},
        'Ih': {'gbar': 0.0000431},
        'NaTg': {'gbar': 0.127, 'vshiftm': 13, 'vshifth': 15, 'slopem': 7},
        'Kv3_1': {'gbar': 0.871},
        'K_P': {'gbar': 0.0111}
    },
    'ions': {'k': {'e': -85}, 'na': {'e': 50}}
}

netParams.cellParams['HL23SST']['secs']['dend'] = {
    'geom': {'diam': 2, 'L': 150, 'Ra': 100, 'cm': 1},
    'topol': {'parentSec': 'soma', 'parentX': 1, 'childX': 0},
    'mechs': {'pas': {'g': 0.0000232, 'e': -81.5}}
}

#------------------------------------------------------------------------------
# HL23PV - Parvalbumin Interneuron (simplified)
#------------------------------------------------------------------------------
netParams.cellParams['HL23PV'] = {
    'conds': {'cellType': 'HL23PV'},
    'secs': {}
}

netParams.cellParams['HL23PV']['secs']['soma'] = {
    'geom': {'diam': 15, 'L': 15, 'Ra': 100, 'cm': 2},
    'mechs': {
        'pas': {'g': 0.000118, 'e': -83.93},
        'Ih': {'gbar': 2.767e-05},
        'NaTg': {'gbar': 0.4996, 'vshiftm': 0, 'vshifth': 10, 'slopem': 9},
        'Kv3_1': {'gbar': 2.992},
        'K_T': {'gbar': 0.00117}
    },
    'ions': {'k': {'e': -85}, 'na': {'e': 50}}
}

netParams.cellParams['HL23PV']['secs']['dend'] = {
    'geom': {'diam': 2, 'L': 150, 'Ra': 100, 'cm': 2},
    'topol': {'parentSec': 'soma', 'parentX': 1, 'childX': 0},
    'mechs': {'pas': {'g': 0.000118, 'e': -83.93}}
}

#------------------------------------------------------------------------------
# HL23VIP - VIP Interneuron (simplified)
#------------------------------------------------------------------------------
netParams.cellParams['HL23VIP'] = {
    'conds': {'cellType': 'HL23VIP'},
    'secs': {}
}

netParams.cellParams['HL23VIP']['secs']['soma'] = {
    'geom': {'diam': 12, 'L': 12, 'Ra': 100, 'cm': 2},
    'mechs': {
        'pas': {'g': 0.0001, 'e': -80},
        'Ih': {'gbar': 0.00005},
        'NaTg': {'gbar': 0.15}
    },
    'ions': {'k': {'e': -85}, 'na': {'e': 50}}
}

netParams.cellParams['HL23VIP']['secs']['dend'] = {
    'geom': {'diam': 1.5, 'L': 120, 'Ra': 100, 'cm': 2},
    'topol': {'parentSec': 'soma', 'parentX': 1, 'childX': 0},
    'mechs': {'pas': {'g': 0.0001, 'e': -80}}
}

#==============================================================================
# Population Parameters
#==============================================================================

netParams.popParams['HL23PYR'] = {
    'cellType': 'HL23PYR',
    'numCells': 8,
    'xRange': [-125, 125],
    'yRange': [-725, -275],
    'zRange': [-125, 125]
}

netParams.popParams['HL23SST'] = {
    'cellType': 'HL23SST',
    'numCells': 1,
    'xRange': [-125, 125],
    'yRange': [-725, -275],
    'zRange': [-125, 125]
}

netParams.popParams['HL23PV'] = {
    'cellType': 'HL23PV',
    'numCells': 1,
    'xRange': [-125, 125],
    'yRange': [-725, -275],
    'zRange': [-125, 125]
}

netParams.popParams['HL23VIP'] = {
    'cellType': 'HL23VIP',
    'numCells': 1,
    'xRange': [-125, 125],
    'yRange': [-725, -275],
    'zRange': [-125, 125]
}

#==============================================================================
# Synaptic Mechanisms
#==============================================================================

# Excitatory synapse (simplified - will use Exp2Syn for now)
netParams.synMechParams['AMPA'] = {
    'mod': 'Exp2Syn',
    'tau1': 0.3,
    'tau2': 3,
    'e': 0
}

# Inhibitory synapse
netParams.synMechParams['GABA'] = {
    'mod': 'Exp2Syn',
    'tau1': 1,
    'tau2': 10,
    'e': -80
}

#==============================================================================
# Connectivity Rules
#==============================================================================

# Connection probabilities from Circuit_param.xls
connData = {
    ('HL23PYR', 'HL23PYR'): (0.15, 'AMPA', 0.001),
    ('HL23PYR', 'HL23SST'): (0.19, 'AMPA', 0.001),
    ('HL23PYR', 'HL23PV'): (0.09, 'AMPA', 0.001),
    ('HL23PYR', 'HL23VIP'): (0.09, 'AMPA', 0.001),
    ('HL23SST', 'HL23PYR'): (0.19, 'GABA', 0.002),
    ('HL23SST', 'HL23SST'): (0.04, 'GABA', 0.002),
    ('HL23SST', 'HL23PV'): (0.20, 'GABA', 0.002),
    ('HL23SST', 'HL23VIP'): (0.06, 'GABA', 0.002),
    ('HL23PV', 'HL23PYR'): (0.094, 'GABA', 0.003),
    ('HL23PV', 'HL23SST'): (0.05, 'GABA', 0.003),
    ('HL23PV', 'HL23PV'): (0.37, 'GABA', 0.003),
    ('HL23PV', 'HL23VIP'): (0.03, 'GABA', 0.003),
    ('HL23VIP', 'HL23PYR'): (0.0, 'GABA', 0.001),
    ('HL23VIP', 'HL23SST'): (0.35, 'GABA', 0.001),
    ('HL23VIP', 'HL23PV'): (0.10, 'GABA', 0.001),
    ('HL23VIP', 'HL23VIP'): (0.05, 'GABA', 0.001)
}

# Create connectivity rules
for (pre, post), (prob, synMech, weight) in connData.items():
    netParams.connParams[f'{pre}->{post}'] = {
        'preConds': {'pop': pre},
        'postConds': {'pop': post},
        'probability': prob,
        'weight': weight,
        'delay': 'uniform(0.5, 2.0)',
        'synMech': synMech,
        'sec': 'soma',
        'loc': 0.5
    }

#==============================================================================
# Stimulation - Background activity
#==============================================================================

netParams.stimSourceParams['background'] = {
    'type': 'NetStim',
    'rate': 5,
    'noise': 1.0,
    'start': 0
}

netParams.stimTargetParams['bg->PYR'] = {
    'source': 'background',
    'conds': {'pop': 'HL23PYR'},
    'weight': 0.001,
    'delay': 1,
    'synMech': 'AMPA',
    'sec': 'soma',
    'loc': 0.5
}

print("NetParams configuration complete!")
print(f"Model directory: {model_dir}")
print(f"Morphology directory: {morph_dir}")