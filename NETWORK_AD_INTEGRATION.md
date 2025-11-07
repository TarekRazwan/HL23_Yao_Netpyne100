# AD-Enabled Network Integration Complete

**Date**: 2025-11-01
**Network**: Yao et al. L2/3 Human Cortical Microcircuit (100 cells)
**AD Integration**: HL23PYR population with staged AD biophysics

---

## Integration Summary

The single-neuron AD staging framework (Healthy, Stage 1, Stage 3) has been successfully integrated into the 100-cell L2/3 network model. The network can now simulate **healthy baseline** or **Alzheimer's Disease variants** with pyramidal neuron hyperexcitability (early AD) or hypoexcitability (late AD).

---

## Network Architecture

### Cell Populations (100 cells total)
| Population | Count | Type | AD Support |
|-----------|-------|------|------------|
| **HL23PYR** | 80 | Excitatory pyramidal | **✓ Yes** (Stage 1 & 3) |
| **HL23SST** | 8 | Somatostatin interneurons | No (future) |
| **HL23PV** | 6 | Parvalbumin interneurons | No (future) |
| **HL23VIP** | 6 | VIP interneurons | No (future) |

**Total**: 100 cells (80% excitatory, 20% inhibitory)

### Connectivity
- **Source**: Circuit_param.xls (experimentally-derived connection probabilities)
- **Synaptic mechanisms**: AMPA, NMDA, GABAA (Exp2Syn)
- **Background drive**: NetStim inputs to all populations (100 Hz, tuned weights)

---

## AD Integration Details

### Files Modified/Created

#### 1. [models/biophys_HL23PYR_AD_Stage1.hoc](models/biophys_HL23PYR_AD_Stage1.hoc) ✓
**Purpose**: Early AD hyperexcitability biophysics
**Changes**:
- SK ↓25% (reduced adaptation)
- M-current ↓25% (reduced spike frequency adaptation)
- Kv3.1 ↓10% (modest repolarization impairment)
- **Nav unchanged** (intact spike generation)

#### 2. [models/biophys_HL23PYR_AD_Stage3.hoc](models/biophys_HL23PYR_AD_Stage3.hoc) ✓
**Purpose**: Late AD hypoexcitability biophysics
**Changes**:
- Nav ↓30% (impaired spike initiation)
- Kv3.1 ↓30% (severe repolarization failure)
- SK ↓25% (reduced AHP)

#### 3. [cellwrapper.py](cellwrapper.py:9-59) ✓
**Updated**: `loadCell_HL23PYR()` function
**New parameters**:
- `ad` (bool): Enable AD variant
- `ad_stage` (int): 1 (early hyperexcitability) or 3 (late hypoexcitability)

**Functionality**:
```python
def loadCell_HL23PYR(cellName, ad=False, ad_stage=None):
    # Selects appropriate biophysics file:
    # - Healthy: biophys_HL23PYR.hoc
    # - Stage 1: biophys_HL23PYR_AD_Stage1.hoc
    # - Stage 3: biophys_HL23PYR_AD_Stage3.hoc
```

#### 4. [cfg.py](cfg.py:20-25) ✓
**Added**: AD configuration options
```python
cfg.ADmodel = False             # Set to True to enable AD variant
cfg.ADstage = 1                 # 1 = early hyperexcitability, 3 = late hypoexcitability
cfg.ADpopulations = ['HL23PYR'] # Which populations to apply AD to
```

#### 5. [netParams.py](netParams.py:52-76) ✓
**Updated**: Cell import loop to pass AD parameters
```python
for cellName in cfg.allpops:
    cellArgs = {'cellName': cellName}

    # Add AD parameters for specified populations
    if cfg.ADmodel and cellName in cfg.ADpopulations:
        cellArgs['ad'] = True
        cellArgs['ad_stage'] = cfg.ADstage

    cellRule = netParams.importCellParams(..., cellArgs=cellArgs)
```

---

## Running the Network

### Healthy Baseline

```bash
cd /Users/tarek/Desktop/HL23_Yao_Netpyne100
python init.py
```

**Expected behavior**:
- All 100 cells loaded with healthy biophysics
- HL23PYR cells: Normal excitability (baseline)
- Output: `output/Yao_L23_100cell_data.json`

### AD Stage 1 (Early Hyperexcitability)

**Edit cfg.py**:
```python
cfg.ADmodel = True
cfg.ADstage = 1
cfg.simLabel = 'Yao_L23_100cell_AD_Stage1'
```

```bash
python init.py
```

**Expected behavior**:
- 80 HL23PYR cells: **Hyperexcitable** (SK↓, Im↓, Kv3.1↓10%, Nav unchanged)
- 20 interneurons: Healthy (unchanged)
- **Prediction**: Increased network firing rate, more synchronous activity
- Output: `output/Yao_L23_100cell_AD_Stage1_data.json`

### AD Stage 3 (Late Hypoexcitability)

**Edit cfg.py**:
```python
cfg.ADmodel = True
cfg.ADstage = 3
cfg.simLabel = 'Yao_L23_100cell_AD_Stage3'
```

```bash
python init.py
```

**Expected behavior**:
- 80 HL23PYR cells: **Severely hypoexcitable** (Nav↓30%, Kv3.1↓30%, SK↓25%)
- 20 interneurons: Healthy (unchanged)
- **Prediction**: Drastically reduced network firing rate, sparse activity
- Output: `output/Yao_L23_100cell_AD_Stage3_data.json`

---

## Expected Network-Level Results

### Single-Cell Predictions (from isolated neuron simulations)

| Condition | Firing @ 310 pA | Change from Healthy |
|-----------|------------------|---------------------|
| Healthy | 21 Hz | — |
| Stage 1 | 23 Hz | **+9.5%** ↑ |
| Stage 3 | 2 Hz | **-90.5%** ↓ |

### Network-Level Predictions

**Healthy Baseline**:
- Population firing rate: ~5-10 Hz (typical for cortical pyramidal neurons)
- E/I balance: Stable recurrent activity
- Raster plot: Sparse, asynchronous firing

**Stage 1 (Early AD)**:
- Population firing rate: **↑ 10-20%** (hyperexcitability)
- E/I balance: **Shifted toward excitation** (80 hyperexcitable E cells, 20 normal I cells)
- Raster plot: **More synchronous bursts** (reduced adaptation → sustained E activity)
- **Biological correlate**: Aberrant network activity, increased seizure susceptibility

**Stage 3 (Late AD)**:
- Population firing rate: **↓ 50-90%** (catastrophic hypoexcitability)
- E/I balance: **Network failure** (E cells cannot sustain firing)
- Raster plot: **Very sparse**, isolated spikes
- **Biological correlate**: "Silent" pyramidal neurons, network hypoactivity, cognitive decline

---

## Analysis Workflow

### 1. Run All Three Conditions

```bash
# Healthy
# (cfg.ADmodel = False)
python init.py

# Stage 1
# (cfg.ADmodel = True, cfg.ADstage = 1, cfg.simLabel = '..._AD_Stage1')
python init.py

# Stage 3
# (cfg.ADmodel = True, cfg.ADstage = 3, cfg.simLabel = '..._AD_Stage3')
python init.py
```

### 2. Compare Outputs

NetPyNE automatically generates:
- **Raster plots**: `output/*_raster.png`
- **Voltage traces**: `output/*_traces_*.png`
- **Network 2D visualization**: `output/*_2Dnet.png`
- **Connectivity matrix**: `output/*_conn.png`

### 3. Quantitative Analysis

Extract from JSON outputs (`output/*_data.json`):

**Population firing rates**:
```python
import json
with open('output/Yao_L23_100cell_data.json') as f:
    data = json.load(f)

# Get spike times for HL23PYR population
pyr_spikes = data['simData']['spkt']  # All spike times
pyr_gids = data['simData']['spkid']   # Corresponding cell GIDs

# Calculate population rate
pyr_indices = [i for i, gid in enumerate(pyr_gids) if gid < 80]  # First 80 cells are PYR
pyr_spike_times = [pyr_spikes[i] for i in pyr_indices]
duration = data['simConfig']['duration'] / 1000.0  # Convert to seconds
pyr_rate = len(pyr_spike_times) / (80 * duration)  # Hz per cell
```

**Synchrony measures**:
- Coefficient of variation (CV) of inter-spike intervals
- Cross-correlation between cells
- Spectral analysis (gamma power, etc.)

---

## Scientific Predictions

### "Storm Before the Quiet" at Network Level

**Hypothesis**: Network activity progression mirrors single-cell phenotype

| Stage | Single-Cell Firing | Network Firing Rate | Network Synchrony | E/I Ratio |
|-------|-------------------|---------------------|-------------------|-----------|
| **Healthy** | 21 Hz | ~5-10 Hz | Low (asynchronous) | 1.0 (balanced) |
| **Stage 1 (Early)** | 23 Hz (+9.5%) | **↑ 6-12 Hz** | **↑ Higher** (bursts) | **↑ 1.1-1.2** (E-dominant) |
| **Stage 3 (Late)** | 2 Hz (-90.5%) | **↓ 0.5-1 Hz** | Low (sparse) | **↓ 0.1-0.2** (E failure) |

### Key Questions to Address

1. **Does single-cell hyperexcitability translate to network hyperactivity?**
   - Prediction: **Yes**, but may be moderated by intact inhibitory population

2. **Will Stage 1 show aberrant synchrony?**
   - Prediction: **Yes**, reduced adaptation → prolonged E bursts → synchronous recruitment

3. **At what point does network activity collapse?**
   - Prediction: Stage 3 (-90.5% E cell firing) → network hypoactivity

4. **Does E/I imbalance worsen across stages?**
   - Prediction: Stage 1 (mild E↑) → Stage 3 (severe E↓ → relative I dominance)

---

## Future Extensions

### 1. Interneuron-Specific AD Changes

**PV interneurons** (currently healthy):
- Kv3.1 ↓30-40% (impairs fast-spiking)
- **Effect**: Reduced gamma oscillations, impaired E/I balance

**SST interneurons** (currently healthy):
- Earlier vulnerability than PV in AD
- **Effect**: Reduced dendritic inhibition → E hyperactivity

### 2. Synaptic Loss

Modify connectivity in cfg.py:
```python
if cfg.ADmodel and cfg.ADstage == 3:
    cfg.EEGain = 0.5  # 50% synaptic loss (E→E)
    cfg.IEGain = 0.7  # 30% synaptic loss (I→E)
```

### 3. Network Stimulation Protocols

Add external inputs to test:
- **TMS-like pulses**: Brief depolarizing current to subset of cells
- **Optogenetic-like stimulation**: Activate PV or SST populations selectively
- **Oscillatory drive**: Test gamma (40 Hz) or theta (8 Hz) entrainment

### 4. Dose-Response Analysis

Test graded AD severity:
```python
cfg.ADstage = 1      # Stage 1: +9.5% firing
cfg.ADstage = 1.5    # Intermediate (need to implement)
cfg.ADstage = 2      # Mixed (need to implement)
cfg.ADstage = 3      # Stage 3: -90.5% firing
```

---

## Technical Notes

### Mechanisms Already Compiled

The network repository already contains compiled mechanisms (`x86_64/` directory), including:
- All Allen Institute ion channels (NaTg, Kv3.1, SK, Im, Ih, Ca_HVA, Ca_LVA, etc.)
- Synaptic mechanisms (Exp2Syn)

**No recompilation needed** unless mechanisms are modified.

### Performance

**Expected simulation time** (MacBook Pro, single core):
- 100 cells, 2000 ms simulation: ~30-60 seconds
- Memory usage: <1 GB

**Scaling**:
- Can increase to 1000 cells (10× larger) with proportional time increase
- Parallel computing (MPI) available for larger networks

---

## Summary

✓ **AD integration complete**
✓ **Three conditions ready**: Healthy, Stage 1 (hyperexcitability), Stage 3 (hypoexcitability)
✓ **80 pyramidal neurons** with staged AD biophysics
✓ **20 interneurons** (healthy, for now)
✓ **Network-level predictions**: Stage 1 → increased synchrony, Stage 3 → network failure

**Next steps**: Run simulations and analyze population-level activity to validate "storm before quiet" hypothesis at the network scale.
