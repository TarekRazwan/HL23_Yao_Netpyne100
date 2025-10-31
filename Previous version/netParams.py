"""
NetPyNE Network Parameters - Fernando Borges Style
Yao et al. 2022 Human L2/3 Model
Following the structure from Human_L23_NetPyNE
"""

from netpyne import specs
from neuron import h
import numpy as np
import pandas as pd

# Initialize
netParams = specs.NetParams()
h.load_file('stdrun.hoc')
h.load_file('import3d.hoc')

# Load Circuit_param.xls
circuit_params = pd.read_excel('Circuit_param.xls', sheet_name=None)

#==============================================================================
# Cell parameters - Fernando style with cellRule
#==============================================================================

# Load biophysics files
h.xopen('models/biophys_HL23PYR.hoc')
h.xopen('models/biophys_HL23SST.hoc')
h.xopen('models/biophys_HL23PV.hoc')
h.xopen('models/biophys_HL23VIP.hoc')

# CRITICAL: Use the GENERIC NeuronTemplate.hoc for all cell types
# NetPyNE needs cellArgs as a list, not dict

# Define cell rules using importCellParams - Fernando's approach
cellTypes = {
    'PYR': 'HL23PYR',
    'SST': 'HL23SST', 
    'PV': 'HL23PV',
    'VIP': 'HL23VIP'
}

for cellType, morphName in cellTypes.items():
    morphFile = f'morphologies/{morphName}.swc'
    
    netParams.importCellParams(
        label=f'{cellType}_rule',
        conds={'cellType': cellType},
        fileName='models/NeuronTemplate.hoc',  # Generic template for all
        cellName='NeuronTemplate',  # Generic class name
        cellArgs=[morphFile],  # Pass as list, not dict!
        importSynMechs=False
    )

#==============================================================================
# Population parameters - 100 cells total
#==============================================================================

netParams.popParams['PYR'] = {
    'cellType': 'PYR',
    'numCells': 80,
    'cellModel': 'PYR_rule'
}

netParams.popParams['SST'] = {
    'cellType': 'SST',
    'numCells': 5,
    'cellModel': 'SST_rule'
}

netParams.popParams['PV'] = {
    'cellType': 'PV',
    'numCells': 7,
    'cellModel': 'PV_rule'
}

netParams.popParams['VIP'] = {
    'cellType': 'VIP',
    'numCells': 8,
    'cellModel': 'VIP_rule'
}

#==============================================================================
# Synaptic mechanisms - from Circuit_param.xls
#==============================================================================

# ProbAMPANMDA (excitatory - from PYR cells)
netParams.synMechParams['ProbAMPANMDA'] = {
    'mod': 'ProbAMPANMDA',
    'tau_r_AMPA': 0.2,
    'tau_d_AMPA': 1.7,
    'tau_r_NMDA': 0.29,
    'tau_d_NMDA': 43,
    'e': 0
}

# ProbGABAA (inhibitory - from interneurons)
netParams.synMechParams['ProbGABAA'] = {
    'mod': 'ProbGABAA',
    'tau_r': 0.2,
    'tau_d': 8.0,
    'e': -80
}

#==============================================================================
# Connectivity rules - from Circuit_param.xls
#==============================================================================

# Connection probabilities
conn_probs = circuit_params['conn_probs'].set_index(circuit_params['conn_probs'].columns[0])

# Synaptic conductances (convert μS to nS)
syn_cond = circuit_params['syn_cond'].set_index(circuit_params['syn_cond'].columns[0]) * 1000

# Number of contacts
n_cont = circuit_params['n_cont'].set_index(circuit_params['n_cont'].columns[0])

# Depression time constant (ms)
depression = circuit_params['Depression'].set_index(circuit_params['Depression'].columns[0])

# Facilitation time constant (ms)
facilitation = circuit_params['Facilitation'].set_index(circuit_params['Facilitation'].columns[0])

# Use parameter for STP
use = circuit_params['Use'].set_index(circuit_params['Use'].columns[0])

# Synaptic position (0=soma, 1=dend, 2=apic)
syn_pos = circuit_params['Syn_pos'].set_index(circuit_params['Syn_pos'].columns[0])

# Create connectivity rules
for prePop in ['PYR', 'SST', 'PV', 'VIP']:
    for postPop in ['PYR', 'SST', 'PV', 'VIP']:
        
        # Get parameters from Circuit_param.xls
        try:
            prob = conn_probs.loc[prePop, postPop]
            weight = syn_cond.loc[prePop, postPop]
            ncontacts = int(n_cont.loc[prePop, postPop])
            dep = depression.loc[prePop, postPop]
            fac = facilitation.loc[prePop, postPop]
            u = use.loc[prePop, postPop]
            synloc = int(syn_pos.loc[prePop, postPop])
        except:
            continue
        
        if prob > 0:
            # Determine synapse type
            if prePop == 'PYR':
                synMech = 'ProbAMPANMDA'
            else:
                synMech = 'ProbGABAA'
            
            # Determine target section
            if synloc == 0:
                sec = 'soma'
            elif synloc == 1:
                sec = 'dend'
            else:
                sec = 'apic'
            
            # Create connection rule
            netParams.connParams[f'{prePop}→{postPop}'] = {
                'preConds': {'pop': prePop},
                'postConds': {'pop': postPop},
                'probability': prob,
                'weight': weight,
                'delay': 2.0,
                'sec': sec,
                'loc': 0.5,
                'synMech': synMech,
                'synsPerConn': ncontacts,
                'synMechParams': {
                    'Dep': dep,
                    'Fac': fac,
                    'Use': u
                }
            }

#==============================================================================
# Background stimulation
#==============================================================================

# Ornstein-Uhlenbeck process parameters from Circuit_param.xls
singcell_params = circuit_params['SING_CELL_PARAM'].set_index(
    circuit_params['SING_CELL_PARAM'].columns[0]
)

# NetStim background (simplified OU process)
for pop in ['PYR', 'SST', 'PV', 'VIP']:
    try:
        Gou = singcell_params.loc['GOU', pop]
    except:
        Gou = 0.00003  # default
    
    # Excitatory background
    netParams.stimSourceParams[f'bkg_exc_{pop}'] = {
        'type': 'NetStim',
        'rate': 50,  # Hz
        'noise': 0.5,
        'start': 0,
        'number': 1e9
    }
    
    netParams.stimTargetParams[f'bkg_exc→{pop}'] = {
        'source': f'bkg_exc_{pop}',
        'conds': {'pop': pop},
        'weight': Gou * 100,  # Scale for NetStim
        'delay': 1,
        'synMech': 'ProbAMPANMDA',
        'sec': 'dend',
        'loc': 0.5
    }
    
    # Inhibitory background
    netParams.stimSourceParams[f'bkg_inh_{pop}'] = {
        'type': 'NetStim',
        'rate': 30,  # Hz
        'noise': 0.5,
        'start': 0,
        'number': 1e9
    }
    
    netParams.stimTargetParams[f'bkg_inh→{pop}'] = {
        'source': f'bkg_inh_{pop}',
        'conds': {'pop': pop},
        'weight': Gou * 50,
        'delay': 1,
        'synMech': 'ProbGABAA',
        'sec': 'soma',
        'loc': 0.5
    }