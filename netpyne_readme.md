# Yao et al. 2022 - NetPyNE Conversion

NetPyNE implementation of the human L2/3 microcircuit model from:
> Yao et al. (2022). "Reduced inhibition in depression impairs stimulus processing in human cortical microcircuits." *Cell Reports*.

## Quick Start

### 1. Setup Directory Structure

```bash
cd ~/Downloads/L23Net
mkdir netpyne_conversion
cd netpyne_conversion
```

### 2. Copy Required Files

Copy the three Python files I provided:
- `netParams.py` - Network parameters
- `simConfig.py` - Simulation configuration  
- `init.py` - Main script

### 3. Link to Original Files

The NetPyNE version needs access to:
- Morphology files (`.swc`)
- MOD files (ion channels)

Create symbolic links:

```bash
# Link morphologies
ln -s ../morphologies ./morphologies

# Link compiled mechanisms
ln -s ../x86_64 ./x86_64
```

### 4. Run Initial Test

```bash
python init.py
```

This will:
- Create a small network (11 cells total)
- Run 1 second simulation
- Generate raster plots and connectivity diagrams
- Save results to `data/` folder

## Current Implementation Status

### ✅ Implemented (Hour 1)

- [x] Basic cell type definitions (4 types)
- [x] Morphology imports
- [x] Core biophysics (soma compartments)
- [x] Population definitions
- [x] Basic connectivity matrix
- [x] Synaptic mechanisms (AMPA/NMDA, GABA)
- [x] Simple background stimulation
- [x] Recording and analysis setup

### 🚧 To Implement Tonight

**Hour 2-3: Enhanced Biophysics**
- [ ] Dendritic ion channel distributions
- [ ] Axonal properties
- [ ] Complete VIP interneuron parameters

**Hour 4-5: Synaptic Dynamics**
- [ ] Short-term plasticity (depression/facilitation)
- [ ] Conductance-based weights from Excel
- [ ] Multiple contacts per connection

**Hour 6-7: Background Input**
- [ ] Tonic inhibition (GABA conductance)
- [ ] OU process (fluctuating background)
- [ ] Proper noise implementation

**Hour 8: Depression Model**
- [ ] 40% SST inhibition reduction
- [ ] Comparison simulations

**Hour 9-10: Validation & Scaling**
- [ ] Compare to LFPy results
- [ ] Scale to 100 cells
- [ ] Document differences

## File Structure

```
netpyne_conversion/
├── init.py              # Main script
├── netParams.py         # Network parameters
├── simConfig.py         # Simulation config
├── morphologies/        # Symlink to ../morphologies/
├── x86_64/             # Symlink to ../x86_64/
├── data/               # Output directory
└── README.md           # This file
```

## Key Differences from Original LFPy Model

1. **Spatial layout**: NetPyNE uses simpler cylindrical distribution
2. **Synapse placement**: Currently simplified to soma (will enhance)
3. **Background input**: Using NetStim instead of OU process (temporary)
4. **No LFP recording**: Focus on spiking activity first

## Next Steps

After running the initial test:

1. **Check output**: Look at `data/yao_netpyne_test_raster.png`
2. **Verify cells fire**: Examine voltage traces
3. **Check connectivity**: Review connection matrix
4. **Compare to LFPy**: Match firing rates

## Troubleshooting

### If morphologies not found:
```bash
# Check symlink
ls -la morphologies/
# Should show: morphologies -> ../morphologies
```

### If mechanisms not found:
```bash
# Check symlink
ls -la x86_64/
# Should show compiled .o files
```

### If simulation fails:
- Check that original LFPy simulation completed successfully
- Verify all `.mod` files are compiled
- Check NetPyNE installation: `python -c "import netpyne; print(netpyne.__version__)"`

## Contact & Notes

This is a rapid conversion focusing on core functionality. Many features simplified for initial testing. Will progressively add complexity over the next 9 hours.

**Goal**: Working 100-cell model that reproduces key findings by end of tonight.
