"""
cellwrapper.py
Fernando's exact approach - expects cell-specific template files
"""

import sys
import os

def loadCell_HL23PYR(cellName, ad=False, ad_stage=None):
    """
    Load HL23PYR cell with optional AD staging support.

    Args:
        cellName (str): Cell name (e.g., 'HL23PYR')
        ad (bool): If True, use AD variant biophysics
        ad_stage (int): AD stage (1=early hyperexcitability, 3=late hypoexcitability)

    Returns:
        NEURON cell object
    """
    templatepath = 'models/NeuronTemplate_HL23PYR.hoc'
    morphpath = 'morphologies/' + cellName + '.swc'

    # Select biophysics file based on AD flag and stage
    if ad:
        if ad_stage == 1:
            biophysics = 'models/biophys_' + cellName + '_AD_Stage1.hoc'
            print(f"[AD] Loading {cellName} with Stage 1 (Early Hyperexcitability) biophysics")
        elif ad_stage == 2:
            biophysics = 'models/biophys_' + cellName + '_AD_Stage2.hoc'
            print(f"[AD] Loading {cellName} with Stage 2 (Intermediate Transition) biophysics")
        elif ad_stage == 3:
            biophysics = 'models/biophys_' + cellName + '_AD_Stage3.hoc'
            print(f"[AD] Loading {cellName} with Stage 3 (Late Hypoexcitability) biophysics")
        else:
            # Default to Stage 1 if ad=True but no stage specified
            biophysics = 'models/biophys_' + cellName + '_AD_Stage1.hoc'
            print(f"[AD] Loading {cellName} with Stage 1 (Early Hyperexcitability, default) biophysics")
    else:
        biophysics = 'models/biophys_' + cellName + '.hoc'
        print(f"[HEALTHY] Loading {cellName} with healthy baseline biophysics")

    from neuron import h
    h.load_file("stdrun.hoc")
    h.load_file('import3d.hoc')
    h.xopen(biophysics)

    try:
       h.xopen(templatepath)
    except:
        pass

    cell = getattr(h, 'NeuronTemplate_HL23PYR')(morphpath)
    print(cell)
    h.biophys_HL23PYR(cell)

    # Print key conductances for verification
    print(f"  Kv3.1 gbar (soma): {cell.soma[0](0.5).gbar_Kv3_1:.6f}")
    print(f"  SK gbar (soma): {cell.soma[0](0.5).gbar_SK:.8f}")
    print(f"  NaTg gbar (axon): {cell.axon[0](0.5).gbar_NaTg:.6f}")

    return cell


def loadCell_HL23VIP(cellName):
    templatepath = 'models/NeuronTemplate_HL23VIP.hoc'
    biophysics = 'models/biophys_' + cellName + '.hoc'
    morphpath = 'morphologies/' + cellName + '.swc'
    
    from neuron import h
    h.load_file("stdrun.hoc")
    h.load_file('import3d.hoc')
    h.xopen(biophysics)
        
    try:
       h.xopen(templatepath)
    except:
        pass
    
    cell = getattr(h, 'NeuronTemplate_HL23VIP')(morphpath)
    print(cell)
    h.biophys_HL23VIP(cell)
    return cell


def loadCell_HL23PV(cellName):
    templatepath = 'models/NeuronTemplate_HL23PV.hoc'
    biophysics = 'models/biophys_' + cellName + '.hoc'
    morphpath = 'morphologies/' + cellName + '.swc'
    
    from neuron import h
    h.load_file("stdrun.hoc")
    h.load_file('import3d.hoc')
    h.xopen(biophysics)
        
    try:
       h.xopen(templatepath)
    except:
        pass
    
    cell = getattr(h, 'NeuronTemplate_HL23PV')(morphpath)
    print(cell)
    h.biophys_HL23PV(cell)
    return cell


def loadCell_HL23SST(cellName):
    templatepath = 'models/NeuronTemplate_HL23SST.hoc'
    biophysics = 'models/biophys_' + cellName + '.hoc'
    morphpath = 'morphologies/' + cellName + '.swc'
    
    from neuron import h
    h.load_file("stdrun.hoc")
    h.load_file('import3d.hoc')
    h.xopen(biophysics)
        
    try:
       h.xopen(templatepath)
    except:
        pass
    
    cell = getattr(h, 'NeuronTemplate_HL23SST')(morphpath)
    print(cell)
    h.biophys_HL23SST(cell)
    return cell