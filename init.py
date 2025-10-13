"""
Main initialization script for Yao et al. 2022 NetPyNE conversion
FULL morphologically and biophysically detailed model
Run with: python init.py
"""

from netpyne import sim
from neuron import h
import os
import sys

# Add parent directory to path to access original model files
parent_dir = os.path.dirname(os.getcwd())
sys.path.insert(0, parent_dir)

# Load NEURON mechanisms
print("Loading NEURON mechanisms...")
mech_dir = os.path.join(parent_dir, 'x86_64')
if os.path.exists(mech_dir):
    print(f"Mechanisms directory: {mech_dir}")
else:
    print(f"Warning: Mechanisms not found at {mech_dir}")

# Load helper functions
net_functions = os.path.join(parent_dir, 'net_functions.hoc')
if os.path.exists(net_functions):
    h.load_file(net_functions)
    print(f"Loaded net_functions.hoc")

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

print("="*80)
print("Yao et al. 2022 L2/3 Microcircuit Model - NetPyNE Conversion")
print("FULL MORPHOLOGICALLY DETAILED MODEL")
print("="*80)

# Import network and simulation parameters
print("\n[1/5] Loading full morphological cell models...")
from netParams import netParams

print("\n[2/5] Importing simulation configuration...")
from simConfig import simConfig

# Create network
print("\n[3/5] Creating network...")
sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)

print("\n[4/5] Simulation complete!")

# Print summary statistics
print("\n[5/5] Summary:")
print(f"  Total simulation time: {simConfig.duration} ms")
print(f"  Number of cells: {sum([p['numCells'] for p in netParams.popParams.values()])}")
print(f"  Output saved to: {simConfig.saveFolder}/{simConfig.filename}")

print("\n" + "="*80)
print("NetPyNE simulation finished successfully!")
print("="*80)