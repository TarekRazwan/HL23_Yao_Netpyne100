# Network Simulation Results: AD Integration

**Date**: 2025-11-02
**Model**: Yao et al. L2/3 Human Cortical Microcircuit (100 cells)
**Conditions**: Healthy Baseline, AD Stage 1 (Early Hyperexcitability), AD Stage 3 (Late Hypoexcitability)

---

## Simulation Parameters

- **Duration**: 2000 ms (2 seconds)
- **Time step**: 0.025 ms
- **Temperature**: 34°C
- **Background drive**: NetStim @ 100 Hz to all populations

### Network Composition

| Population | Count | Type | AD Modification |
|-----------|-------|------|-----------------|
| HL23PYR | 80 | Excitatory pyramidal | **✓ Yes** (Stages 1 & 3) |
| HL23SST | 8 | Somatostatin interneurons | No (healthy) |
| HL23PV | 6 | Parvalbumin interneurons | No (healthy) |
| HL23VIP | 6 | VIP interneurons | No (healthy) |

---

## Results Summary

### Healthy Baseline ✓ Complete

**Simulation time**: ~5646 seconds (~94 minutes)
**Total spikes**: 709
**Average network firing rate**: 3.54 Hz

#### Population-Specific Firing Rates

| Population | Firing Rate | Count | Notes |
|-----------|-------------|-------|-------|
| **HL23PYR** | **2.619 Hz** | 80 cells | Excitatory baseline |
| HL23SST | 7.125 Hz | 8 cells | Higher than PYR (typical for interneurons) |
| HL23PV | 10.750 Hz | 6 cells | Highest firing (fast-spiking) |
| HL23VIP | 3.917 Hz | 6 cells | Similar to PYR |

**Key Observations**:
- HL23PYR firing rate (2.6 Hz) is **reasonable** for cortical pyramidal neurons at rest
- Interneurons fire at higher rates (3.9-10.8 Hz), consistent with their inhibitory role
- Network shows sparse, asynchronous activity (healthy baseline)

---

### AD Stage 1 (Early Hyperexcitability) 🔄 Running

**Status**: Simulation in progress
**Expected changes** (based on single-cell results):
- HL23PYR firing rate: **+9.5% increase** (predicted: ~2.9 Hz)
- Mechanism: SK↓25%, M-current↓25%, Kv3.1↓10%, Nav unchanged
- Network prediction: Increased synchrony, more bursting activity

---

### AD Stage 3 (Late Hypoexcitability) ⏳ Pending

**Status**: Awaiting completion of Stage 1
**Expected changes** (based on single-cell results):
- HL23PYR firing rate: **-90.5% decrease** (predicted: ~0.25 Hz)
- Mechanism: Nav↓30%, Kv3.1↓30%, SK↓25%
- Network prediction: Sparse activity, network hypoactivity, "silent" neurons

---

## Single-Cell vs Network Comparison

### Single-Cell Results (@ 310 pA current injection)

| Condition | Firing Rate | Change from Healthy |
|-----------|-------------|---------------------|
| Healthy | 21 Hz | — |
| Stage 1 | 23 Hz | **+9.5%** ↑ |
| Stage 3 | 2 Hz | **-90.5%** ↓ |

### Network Results (spontaneous activity with background drive)

| Condition | HL23PYR Population Rate | Change from Healthy |
|-----------|-------------------------|---------------------|
| Healthy | **2.619 Hz** | — |
| Stage 1 | *Running...* | **Predicted: +9.5% → ~2.9 Hz** |
| Stage 3 | *Pending* | **Predicted: -90.5% → ~0.25 Hz** |

---

## Interpretation

### Healthy Baseline Validation

✓ **HL23PYR firing rate (2.6 Hz) is biologically realistic**
- Cortical pyramidal neurons in vivo: 0.5-5 Hz at rest
- Our network: 2.6 Hz falls within this range

✓ **E/I balance appears reasonable**
- Excitatory (PYR): 2.6 Hz
- Inhibitory (SST/PV/VIP): 3.9-10.8 Hz
- I > E firing rates → inhibitory control intact

✓ **Network shows sparse activity**
- 709 spikes across 100 cells over 2 seconds
- Average: 3.54 spikes/cell/2sec → ~1.8 Hz overall
- Consistent with asynchronous irregular (AI) state in cortex

### Predictions for AD Stages

**Stage 1 (Early AD - Hyperexcitability)**:
- **Expected**: Modest increase in HL23PYR firing (+9.5% from single-cell)
- **Network effect**: May be dampened by intact inhibitory neurons (SST/PV/VIP)
- **Hypothesis**: Still expect increased firing, but possibly less than +9.5% due to network compensation

**Stage 3 (Late AD - Severe Hypoexcitability)**:
- **Expected**: Catastrophic reduction in HL23PYR firing (-90.5% from single-cell)
- **Network effect**: E/I imbalance (E ↓↓, I unchanged) → relative I dominance
- **Hypothesis**: Network may show near-complete failure of excitatory activity

---

## "Storm Before the Quiet" at Network Level

### Hypothesis

The biphasic AD progression observed at the single-cell level should manifest as:

1. **Healthy**: Balanced, sparse network activity
2. **Stage 1 (Early)**: **Increased E activity** → aberrant synchrony, bursting
3. **Stage 3 (Late)**: **E network failure** → hypoactivity, "silent" PYR neurons

### Validation Criteria

**Stage 1 vs Healthy**:
- ✓ Increased HL23PYR firing rate (predicted: +5-10%)
- ✓ Increased network synchrony (higher CV, cross-correlation)
- ✓ Possible emergence of burst events

**Stage 3 vs Healthy**:
- ✓ Drastically reduced HL23PYR firing rate (predicted: -80-95%)
- ✓ Network hypoactivity (total spike count ↓)
- ✓ E/I imbalance (relative I dominance)

---

## Files Generated

### Healthy Baseline
- `output/Yao_L23_100cell_data.json` ✓
- `output/Yao_L23_100cell_raster.png` ✓
- `output/Yao_L23_100cell_traces_*.png` ✓
- `output/Yao_L23_100cell_2Dnet.png` ✓
- `output/Yao_L23_100cell_conn.png` ✓

### AD Stage 1 (when complete)
- `output/Yao_L23_100cell_AD_Stage1_data.json` 🔄
- `output/Yao_L23_100cell_AD_Stage1_raster.png` 🔄
- (+ traces, net, conn plots)

### AD Stage 3 (when complete)
- `output/Yao_L23_100cell_AD_Stage3_data.json` ⏳
- (+ all associated plots)

---

## Technical Notes

### Simulation Performance

**Healthy Baseline**:
- Simulation time: 5646 seconds (~94 minutes)
- Biological time: 2 seconds
- Real-time ratio: ~2823× slower than real-time
- Hardware: MacBook Pro (single core, no MPI)

**Bottlenecks**:
- 100 detailed morphological neurons with full biophysics
- 80 HL23PYR cells each have ~800-1000 compartments
- No CVODE (fixed time-step integration)

**Optimization opportunities**:
- Use CVODE (adaptive time-step)
- Parallel computing (MPI) for multi-core
- Reduce morphological detail (ball-and-stick models)

### Template Redefinition Warnings

**Issue**: NEURON shows warnings about template redefinition during cell loading
**Impact**: None - warnings are cosmetic, simulations complete successfully
**Cause**: Duplicate code sections in netParams.py (from earlier file duplication)
**Resolution**: Does not affect results, can be ignored or fixed by cleaning netParams.py

---

## Next Steps

1. ✓ **Wait for AD Stage 1 to complete** (currently running)
2. **Run AD Stage 3 simulation**
3. **Compare all three conditions**:
   - Population firing rates
   - Raster plots (visual synchrony comparison)
   - Quantitative synchrony measures (CV, cross-correlation)
4. **Validate "storm before quiet" hypothesis**

---

## Summary

✓ **Healthy baseline successfully simulated**
- HL23PYR: 2.6 Hz (realistic cortical pyramidal neuron firing)
- Network shows sparse, asynchronous activity
- E/I balance appears reasonable (I > E firing rates)

🔄 **AD Stage 1 (Early Hyperexcitability) running**
- Predicting +9.5% increase in HL23PYR firing
- May see increased synchrony/bursting

⏳ **AD Stage 3 (Late Hypoexcitability) pending**
- Predicting -90.5% reduction in HL23PYR firing
- Expect catastrophic network hypoactivity

**Hypothesis under test**: Single-cell AD phenotypes (hyperexcitability → hypoexcitability) translate to network-level activity changes, demonstrating the "storm before the quiet" progression of Alzheimer's Disease.

---

**Last updated**: 2025-11-02 (Healthy complete, Stage 1 running, Stage 3 pending)
