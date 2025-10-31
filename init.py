"""
init.py
COMPLETE Main simulation runner for Yao et al. L2/3 human microcircuit
100-cell replica using NetPyNE

Usage:
    python init.py
    
Output:
    - output/Yao_L23_100cell_data.json
    - output/Yao_L23_100cell_raster.png
    - output/Yao_L23_100cell_traces.png
"""

import os
import sys
from neuron import h
import neuron

# Load NEURON mechanisms
print("\n" + "="*70)
print("YAO ET AL. L2/3 HUMAN CORTICAL MICROCIRCUIT - 100 CELLS")
print("="*70)

print("\n[1/6] Checking prerequisites...")

# Check for required files
required_files = [
    'cfg.py',
    'netParams.py',
    'cellwrapper.py',
    'Circuit_param.xls'
]

missing_files = []
for fname in required_files:
    if not os.path.exists(fname):
        missing_files.append(fname)

if missing_files:
    print(f"✗ ERROR: Missing required files: {missing_files}")
    sys.exit(1)

print("✓ All required Python files present")

# Check for cell-specific templates
required_templates = [
    'models/NeuronTemplate_HL23PYR.hoc',
    'models/NeuronTemplate_HL23SST.hoc',
    'models/NeuronTemplate_HL23PV.hoc',
    'models/NeuronTemplate_HL23VIP.hoc'
]

missing_templates = []
for template in required_templates:
    if not os.path.exists(template):
        missing_templates.append(template)

if missing_templates:
    print(f"\n✗ ERROR: Missing cell-specific template files!")
    print(f"   Missing: {missing_templates}")
    print(f"\n   Run this first: python create_templates.py")
    sys.exit(1)

print("✓ All cell-specific templates present")

print("\n[2/6] Loading NEURON mechanisms...")
if os.path.exists('x86_64'):
    neuron.load_mechanisms('x86_64')
    print("✓ Loaded mechanisms from x86_64/")
elif os.path.exists('mod'):
    print("✗ ERROR: mod/ folder exists but not compiled!")
    print("   Run: nrnivmodl mod/")
    sys.exit(1)
else:
    print("⚠ WARNING: No mechanism folder found, using default NEURON mechanisms")

# Import NetPyNE
print("\n[3/6] Importing NetPyNE...")
from netpyne import sim

# Import configuration
print("\n[4/6] Loading configuration...")
from cfg import cfg
print(f"✓ Simulation duration: {cfg.duration} ms")
print(f"✓ Time step: {cfg.dt} ms")
print(f"✓ Cell populations: {cfg.allpops}")
print(f"✓ Total cells: {sum(cfg.cellNumber.values())}")

# Import network parameters
print("\n[5/6] Loading network parameters...")
from netParams import netParams

# Create output directory
if not os.path.exists(cfg.saveFolder):
    os.makedirs(cfg.saveFolder)
    print(f"✓ Created output directory: {cfg.saveFolder}/")

# Run simulation
print("\n[6/6] Running simulation...")
print("-" * 70)

try:
    sim.createSimulateAnalyze(netParams=netParams, simConfig=cfg)
    
    print("\n" + "="*70)
    print("✅ SIMULATION COMPLETE!")
    print("="*70)
    print(f"\nResults saved to: {cfg.saveFolder}/")
    print("\nGenerated files:")
    
    # List generated files
    output_files = []
    if os.path.exists(cfg.saveFolder):
        for fname in os.listdir(cfg.saveFolder):
            if fname.startswith(cfg.simLabel):
                output_files.append(fname)
                print(f"  ✓ {fname}")
    
    if not output_files:
        print("  (No output files found - check cfg.saveFolder)")
    
    # Print summary statistics
    print("\n" + "="*70)
    print("SUMMARY STATISTICS")
    print("="*70)
    
    if hasattr(sim, 'allSimData') and 'spkt' in sim.allSimData:
        total_spikes = len(sim.allSimData['spkt'])
        duration_sec = cfg.duration / 1000.0
        num_cells = sum(cfg.cellNumber.values())
        avg_rate = total_spikes / (duration_sec * num_cells) if num_cells > 0 else 0
        
        print(f"Total spikes: {total_spikes}")
        print(f"Average firing rate: {avg_rate:.2f} Hz")
        print(f"Simulation time: {cfg.duration} ms")
        print(f"Number of cells: {num_cells}")
        
        # Per-population stats
        print("\nPer-population firing rates:")
        for pop in cfg.allpops:
            pop_spikes = [spk for i, spk in enumerate(sim.allSimData['spkt']) 
                         if sim.allSimData['spkid'][i] in sim.net.cells and 
                         sim.net.cells[int(sim.allSimData['spkid'][i])].tags.get('pop') == pop]
            pop_cells = cfg.cellNumber[pop]
            pop_rate = len(pop_spikes) / (duration_sec * pop_cells) if pop_cells > 0 else 0
            print(f"  {pop}: {pop_rate:.2f} Hz ({len(pop_spikes)} spikes)")
    else:
        print("No spike data available")
    
    print("\n" + "="*70)
    print("🎉 SUCCESS! Check the output/ folder for results!")
    print("="*70 + "\n")
    
except KeyboardInterrupt:
    print("\n\n" + "="*70)
    print("⚠ SIMULATION INTERRUPTED BY USER")
    print("="*70 + "\n")
    sys.exit(0)
    
except Exception as e:
    print("\n" + "="*70)
    print("❌ SIMULATION FAILED!")
    print("="*70)
    print(f"\nError: {e}")
    print("\nTroubleshooting steps:")
    print("1. Make sure you ran: python create_templates.py")
    print("2. Check that all HOC files exist in models/")
    print("3. Check that all SWC files exist in morphologies/")
    print("4. Check that Circuit_param.xls exists")
    print("5. Verify mechanisms compiled: ls x86_64/")
    print("6. Check cellwrapper.py functions load correctly")
    
    import traceback
    print("\nFull error traceback:")
    print("-" * 70)
    traceback.print_exc()
    print("="*70 + "\n")
    sys.exit(1)
    """
init.py
Main simulation runner for Yao et al. L2/3 human microcircuit
100-cell replica using NetPyNE

Usage:
    python init.py
    
Output:
    - output/Yao_L23_100cell_data.json
    - output/Yao_L23_100cell_raster.png
    - output/Yao_L23_100cell_traces.png
"""

import os
import sys
from neuron import h
import neuron

# Load NEURON mechanisms
print("\n" + "="*70)
print("YAOER AL. L2/3 HUMAN CORTICAL MICROCIRCUIT - 100 CELLS")
print("="*70)

print("\n[1/5] Loading NEURON mechanisms...")
if os.path.exists('x86_64'):
    neuron.load_mechanisms('x86_64')
    print("✓ Loaded mechanisms from x86_64/")
elif os.path.exists('mod'):
    print("ERROR: mod/ folder exists but not compiled!")
    print("Run: nrnivmodl mod/")
    sys.exit(1)
else:
    print("WARNING: No mechanism folder found, using default NEURON mechanisms")

# Import NetPyNE
print("\n[2/5] Importing NetPyNE...")
from netpyne import sim

# Import configuration and network parameters
print("\n[3/5] Loading configuration...")
from cfg import cfg
print(f"✓ Simulation duration: {cfg.duration} ms")
print(f"✓ Time step: {cfg.dt} ms")
print(f"✓ Cell populations: {cfg.allpops}")
print(f"✓ Total cells: {sum(cfg.cellNumber.values())}")

print("\n[4/5] Loading network parameters...")
from netParams import netParams

# Create output directory
if not os.path.exists(cfg.saveFolder):
    os.makedirs(cfg.saveFolder)
    print(f"✓ Created output directory: {cfg.saveFolder}/")

# Run simulation
print("\n[5/5] Running simulation...")
print("-" * 70)

try:
    sim.createSimulateAnalyze(netParams=netParams, simConfig=cfg)
    
    print("\n" + "="*70)
    print("SIMULATION COMPLETE!")
    print("="*70)
    print(f"\nResults saved to: {cfg.saveFolder}/")
    print("\nGenerated files:")
    print(f"  - {cfg.simLabel}_data.json")
    print(f"  - {cfg.simLabel}_raster.png")
    print(f"  - {cfg.simLabel}_traces.png")
    print(f"  - {cfg.simLabel}_net.png")
    print(f"  - {cfg.simLabel}_conn.png")
    
    # Print summary statistics
    print("\nSummary:")
    if hasattr(sim, 'allSimData'):
        if 'spkt' in sim.allSimData:
            total_spikes = len(sim.allSimData['spkt'])
            duration_sec = cfg.duration / 1000.0
            num_cells = sum(cfg.cellNumber.values())
            avg_rate = total_spikes / (duration_sec * num_cells)
            print(f"  Total spikes: {total_spikes}")
            print(f"  Average firing rate: {avg_rate:.2f} Hz")
    
    print("\n" + "="*70)
    
except Exception as e:
    print("\n" + "="*70)
    print("SIMULATION FAILED!")
    print("="*70)
    print(f"Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check that all HOC files exist in models/")
    print("2. Check that all SWC files exist in morphologies/")
    print("3. Check that Circuit_param.xls exists")
    print("4. Verify mechanisms compiled: ls x86_64/")
    print("5. Check cellwrapper.py functions load correctly")
    import traceback
    traceback.print_exc()
    sys.exit(1)