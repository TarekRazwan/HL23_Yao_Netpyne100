"""
Direct HOC Cell Creation Approach
Since NetPyNE's importCellParams doesn't preserve HOC template structure properly,
we create cells directly via HOC (like cellwrapper) and add them to NetPyNE network
"""

from neuron import h, gui
import numpy as np
import pandas as pd

# Load NEURON standard files
h.load_file('stdrun.hoc')
h.load_file('import3d.hoc')

# Load biophysics
h.xopen('models/biophys_HL23PYR.hoc')
h.xopen('models/biophys_HL23SST.hoc')
h.xopen('models/biophys_HL23PV.hoc')
h.xopen('models/biophys_HL23VIP.hoc')

# Load template
h.xopen('models/NeuronTemplate.hoc')

# CRITICAL: Load synapse mechanisms
# They should be auto-loaded from compiled mechanisms, but let's verify
print("Checking synapse mechanisms...")

has_GABA = False
try:
    # Test if ProbAMPANMDA exists
    test_sec = h.Section()
    test_syn = h.ProbAMPANMDA(test_sec(0.5))
    print("  ✓ ProbAMPANMDA found")
    del test_syn, test_sec
except:
    print("  ✗ ProbAMPANMDA NOT FOUND - check mechanisms compilation!")
    print("    Run: cd mechanisms/ && nrnivmodl && cd ..")
    exit(1)

try:
    test_sec = h.Section()
    test_syn = h.ProbGABAA(test_sec(0.5))
    print("  ✓ ProbGABAA found")
    has_GABA = True
    GABA_mechanism = 'ProbGABAA'
    del test_syn, test_sec
except:
    print("  ✗ ProbGABAA NOT FOUND")
    print("    Using ProbUDFsyn for inhibition (Yao's approach)")
    
    # Yao et al. uses ProbUDFsyn for GABA!
    try:
        test_sec = h.Section()
        test_syn = h.ProbUDFsyn(test_sec(0.5))
        print(f"  ✓ Found ProbUDFsyn - configuring as GABA")
        has_GABA = True
        GABA_mechanism = 'ProbUDFsyn'
        del test_syn, test_sec
    except:
        print("  ✗ ProbUDFsyn also not found!")
        print("    Cannot create inhibitory synapses")
        has_GABA = False
        GABA_mechanism = None


print("\n" + "="*70)
print("Direct HOC Cell Creation - Yao et al. 2022")
print("="*70)

# Network parameters
cell_counts = {
    'PYR': 80,
    'SST': 5,
    'PV': 7,
    'VIP': 8
}

morphologies = {
    'PYR': 'morphologies/HL23PYR.swc',
    'SST': 'morphologies/HL23SST.swc',
    'PV': 'morphologies/HL23PV.swc',
    'VIP': 'morphologies/HL23VIP.swc'
}

biophys_funcs = {
    'PYR': h.biophys_HL23PYR,
    'SST': h.biophys_HL23SST,
    'PV': h.biophys_HL23PV,
    'VIP': h.biophys_HL23VIP
}

# Create cells
print("\n[1/4] Creating cells with biophysics...")
cells = []
cell_types = []
gid = 0

for cell_type in ['PYR', 'SST', 'PV', 'VIP']:
    n_cells = cell_counts[cell_type]
    morph = morphologies[cell_type]
    biophys = biophys_funcs[cell_type]
    
    print(f"  Creating {n_cells} {cell_type} cells...")
    
    for i in range(n_cells):
        # Create cell via HOC template (like cellwrapper)
        cell = h.NeuronTemplate(morph)
        
        # Apply biophysics
        biophys(cell)
        
        # Store
        cells.append(cell)
        cell_types.append(cell_type)
        gid += 1

print(f"  Total: {len(cells)} cells created with full biophysics")

# Load connectivity parameters
print("\n[2/4] Loading connectivity parameters...")
circuit_params = pd.read_excel('Circuit_param.xls', sheet_name=None)

# CRITICAL: The Excel sheets have the cell types as BOTH row and column headers
# First column contains row labels, need to handle this correctly

print("  Excel sheets found:", list(circuit_params.keys()))

# Connection probabilities - first column is row labels
conn_probs_df = circuit_params['conn_probs']
print(f"  conn_probs shape: {conn_probs_df.shape}")
print(f"  conn_probs columns: {list(conn_probs_df.columns)}")
print(f"  First few rows:\n{conn_probs_df.head()}")

# The first column name is usually something like 'Unnamed: 0' or the first cell type
# Set it as index
first_col = conn_probs_df.columns[0]
conn_probs = conn_probs_df.set_index(first_col)

# Do the same for other parameters
syn_cond = circuit_params['syn_cond'].set_index(circuit_params['syn_cond'].columns[0])
n_cont = circuit_params['n_cont'].set_index(circuit_params['n_cont'].columns[0])
depression = circuit_params['Depression'].set_index(circuit_params['Depression'].columns[0])
facilitation = circuit_params['Facilitation'].set_index(circuit_params['Facilitation'].columns[0])
use = circuit_params['Use'].set_index(circuit_params['Use'].columns[0])
syn_pos = circuit_params['Syn_pos'].set_index(circuit_params['Syn_pos'].columns[0])

# CRITICAL FIX: Rename indices and columns to match our cell_types
# Excel has 'HL23PYR', code uses 'PYR'
name_map = {
    'HL23PYR': 'PYR',
    'HL23SST': 'SST',
    'HL23PV': 'PV',
    'HL23VIP': 'VIP'
}

conn_probs.rename(index=name_map, columns=name_map, inplace=True)
syn_cond.rename(index=name_map, columns=name_map, inplace=True)
n_cont.rename(index=name_map, columns=name_map, inplace=True)
depression.rename(index=name_map, columns=name_map, inplace=True)
facilitation.rename(index=name_map, columns=name_map, inplace=True)
use.rename(index=name_map, columns=name_map, inplace=True)
syn_pos.rename(index=name_map, columns=name_map, inplace=True)

print("  Connectivity parameters loaded")
print(f"  conn_probs index: {list(conn_probs.index)}")
print(f"  conn_probs columns: {list(conn_probs.columns)}")
print(f"\n  Sample connection probabilities after renaming:")
print(f"    PYR→PYR: {conn_probs.loc['PYR', 'PYR']}")
print(f"    SST→VIP: {conn_probs.loc['SST', 'VIP']}")
print(f"    PV→PV: {conn_probs.loc['PV', 'PV']}")

# Create connections
print("\n[3/4] Creating synaptic connections...")
print("  This may take a few minutes...")

n_connections = 0
connection_attempts = 0
errors = []

# Debug: Show connection probabilities
print("\n  Connection probabilities:")
for pre_type in ['PYR', 'SST', 'PV', 'VIP']:
    for post_type in ['PYR', 'SST', 'PV', 'VIP']:
        try:
            prob = conn_probs.loc[pre_type, post_type]
            print(f"    {pre_type}→{post_type}: {prob:.3f}")
        except:
            print(f"    {pre_type}→{post_type}: N/A")

print("\n  Creating connections...")

for post_idx, post_cell in enumerate(cells):
    post_type = cell_types[post_idx]
    
    for pre_idx, pre_cell in enumerate(cells):
        if pre_idx == post_idx:
            continue  # No autapses
        
        pre_type = cell_types[pre_idx]
        
        try:
            prob = conn_probs.loc[pre_type, post_type]
            
            if prob <= 0:
                continue
            
            connection_attempts += 1
            
            # Draw random number for connection
            if np.random.random() < prob:
                # Determine synapse type and location
                if pre_type == 'PYR':
                    syn_mech = 'ProbAMPANMDA'
                else:
                    if not has_GABA:
                        continue  # Skip inhibitory connections if no GABA
                    syn_mech = GABA_mechanism  # Use ProbUDFsyn or ProbGABAA
                
                synloc = int(syn_pos.loc[pre_type, post_type])
                
                # Get target sections based on location
                if synloc == 0:  # soma
                    target_sec_list = [post_cell.soma[0]]
                elif synloc == 1:  # basal
                    # Iterate through dend sections
                    target_sec_list = []
                    for sec in post_cell.basal:
                        target_sec_list.append(sec)
                else:  # apical
                    target_sec_list = []
                    for sec in post_cell.apical:
                        target_sec_list.append(sec)
                
                if len(target_sec_list) == 0:
                    errors.append(f"No target sections for {pre_type}→{post_type} (loc={synloc})")
                    continue
                
                # Get weight and STP parameters
                weight = syn_cond.loc[pre_type, post_type] * 1000  # μS to nS
                ncontacts = int(n_cont.loc[pre_type, post_type])
                dep = depression.loc[pre_type, post_type]
                fac = facilitation.loc[pre_type, post_type]
                u = use.loc[pre_type, post_type]
                
                # Create synapse(s) on target sections
                for _ in range(ncontacts):
                    try:
                        # Choose random section from target
                        target_sec = target_sec_list[np.random.randint(len(target_sec_list))]
                        
                        # Create synapse
                        syn = getattr(h, syn_mech)(target_sec(0.5))
                        
                        # Set parameters based on synapse type
                        if syn_mech == 'ProbAMPANMDA':
                            # Excitatory parameters
                            syn.tau_r_AMPA = 0.3  # From Yao circuit.py
                            syn.tau_d_AMPA = 3.0
                            syn.tau_r_NMDA = 2.0
                            syn.tau_d_NMDA = 65.0
                            syn.e = 0
                        elif syn_mech == 'ProbUDFsyn':
                            # Inhibitory parameters (GABA) - From Yao circuit.py
                            syn.tau_r = 1.0   # Rise time
                            syn.tau_d = 10.0  # Decay time
                            syn.e = -80       # GABA reversal potential
                        
                        # Short-term plasticity (same for both)
                        syn.Dep = dep
                        syn.Fac = fac
                        syn.Use = u
                        
                        # Create NetCon
                        nc = h.NetCon(pre_cell.soma[0](0.5)._ref_v, syn, sec=pre_cell.soma[0])
                        nc.weight[0] = weight
                        nc.delay = 2.0
                        nc.threshold = -30
                        
                        n_connections += 1
                    except Exception as e:
                        errors.append(f"Synapse creation error: {e}")
        
        except KeyError:
            pass  # Connection parameters don't exist for this pair
        except Exception as e:
            errors.append(f"Connection error {pre_type}→{post_type}: {e}")

    if (post_idx + 1) % 20 == 0:
        print(f"    Processed {post_idx + 1}/{len(cells)} cells, {n_connections} connections so far...")

print(f"  Total connection attempts: {connection_attempts}")
print(f"  Total connections created: {n_connections}")
if errors:
    print(f"  Errors encountered: {len(errors)}")
    print("  First 5 errors:")
    for err in errors[:5]:
        print(f"    - {err}")

# Add background stimulation
print("\n[4/4] Adding background stimulation...")
n_stims = 0
iclamps = []  # Store IClamps to prevent garbage collection

for cell_idx, cell in enumerate(cells):
    cell_type = cell_types[cell_idx]
    
    # Get soma section (it's an array)
    soma_sec = cell.soma[0]
    
    # Add IClamp to ~20% of cells to kick-start activity
    if np.random.random() < 0.2:
        iclamp = h.IClamp(soma_sec(0.5))
        iclamp.delay = np.random.uniform(10, 100)  # Start between 10-100 ms
        iclamp.dur = 50  # 50 ms duration
        iclamp.amp = 0.5  # 0.5 nA current
        iclamps.append(iclamp)
        n_stims += 1
    
    # Excitatory background (keep this too)
    stim_exc = h.NetStim()
    stim_exc.interval = 1000 / 100  # Increased to 100 Hz from 50
    stim_exc.number = 1e9
    stim_exc.noise = 0.5
    stim_exc.start = 0
    
    syn_exc = h.ProbAMPANMDA(soma_sec(0.5))
    nc_exc = h.NetCon(stim_exc, syn_exc)
    nc_exc.weight[0] = 0.05  # Much stronger: 0.05 from 0.01
    nc_exc.delay = 1
    n_stims += 1
    
    # Inhibitory background (only if GABA available)
    if has_GABA:
        stim_inh = h.NetStim()
        stim_inh.interval = 1000 / 30  # 30 Hz
        stim_inh.number = 1e9
        stim_inh.noise = 0.5
        stim_inh.start = 0
        
        # Use the correct GABA mechanism
        syn_inh = getattr(h, GABA_mechanism)(soma_sec(0.5))
        
        # Set GABA parameters
        if GABA_mechanism == 'ProbUDFsyn':
            syn_inh.tau_r = 1.0   # Rise time
            syn_inh.tau_d = 10.0  # Decay time  
            syn_inh.e = -80       # GABA reversal
        
        nc_inh = h.NetCon(stim_inh, syn_inh)
        nc_inh.weight[0] = 0.0005
        nc_inh.delay = 1
        n_stims += 1

print(f"  Total stimuli: {n_stims} (including {len(iclamps)} IClamps)")

# Setup recording
print("\n" + "="*70)
print("NETWORK SUMMARY")
print("="*70)
print(f"Cells: {len(cells)}")
for ctype in ['PYR', 'SST', 'PV', 'VIP']:
    count = cell_types.count(ctype)
    print(f"  {ctype}: {count}")
print(f"Connections: {n_connections}")
print(f"Stimuli: {n_stims}")
print("="*70)

# Record from sample cells
print("\nSetting up recording...")
t_vec = h.Vector().record(h._ref_t)
v_vecs = []
recorded_cells = [0, 1, 80, 85, 92, 95]  # Sample from each population

for idx in recorded_cells:
    if idx < len(cells):
        v = h.Vector().record(cells[idx].soma[0](0.5)._ref_v)
        v_vecs.append((idx, cell_types[idx], v))

# Run simulation
print("\nRunning simulation...")
print("Duration: 2000 ms")
print("This will take 30-60 minutes...")
print("="*70)

h.dt = 0.025
h.tstop = 2000
h.celsius = 34
h.v_init = -70

h.init()
h.run()

print("\n" + "="*70)
print("SIMULATION COMPLETE")
print("="*70)

# Save results
print("\nSaving results...")
import pickle

results = {
    't': np.array(t_vec),
    'v_traces': [(idx, ctype, np.array(v)) for idx, ctype, v in v_vecs],
    'n_cells': len(cells),
    'cell_types': cell_types,
    'n_connections': n_connections
}

with open('direct_hoc_results.pkl', 'wb') as f:
    pickle.dump(results, f)

print("Results saved to: direct_hoc_results.pkl")

# Quick analysis
print("\nQuick analysis:")
for idx, ctype, v in v_vecs:
    spikes = np.where(np.diff(np.array(v) > -20) == 1)[0]
    rate = len(spikes) / 2.0  # Hz (2 second simulation)
    print(f"  Cell {idx} ({ctype}): {len(spikes)} spikes, {rate:.2f} Hz")

print("\nDone!")