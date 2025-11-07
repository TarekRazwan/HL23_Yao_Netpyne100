"""
Generate F-I and V-I curves for Healthy, AD Stage 1, and AD Stage 3 conditions
Systematically inject current steps and measure firing rate and voltage response
"""

from netpyne import specs, sim
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime

# Current injection parameters
I_MIN = 0.0      # nA
I_MAX = 0.5      # nA
I_STEP = 0.05    # nA
I_DUR = 1000     # ms
I_START = 500    # ms
SIM_DUR = 2000   # ms

def run_single_FI_point(current_amp, ad_model=False, ad_stage=None):
    """Run a single simulation with given current injection"""

    # Create new config
    cfg = specs.SimConfig()
    cfg.duration = SIM_DUR
    cfg.dt = 0.025
    cfg.verbose = False
    cfg.recordCells = [0]  # Record from cell 0
    cfg.recordTraces = {'V_soma': {'sec': 'soma_0', 'loc': 0.5, 'var': 'v'}}
    cfg.recordStep = 0.1
    cfg.hParams = {'celsius': 34, 'v_init': -80}
    cfg.printPopAvgRates = False
    cfg.printRunTime = False
    cfg.createNEURONObj = True
    cfg.createPyStruct = True

    # AD configuration
    cfg.ADmodel = ad_model
    cfg.ADstage = ad_stage if ad_stage else 1
    cfg.ADpopulations = ['HL23PYR']

    # Create network params
    netParams = specs.NetParams()

    # Single cell population
    netParams.popParams['HL23PYR'] = {
        'cellType': 'HL23PYR',
        'numCells': 1,
        'cellModel': 'HH_full'
    }

    # Import cell with AD parameters
    cellArgs = {'cellName': 'HL23PYR'}
    if ad_model:
        cellArgs['ad'] = True
        cellArgs['ad_stage'] = ad_stage

    netParams.importCellParams(
        label='HL23PYR',
        somaAtOrigin=False,
        conds={'cellType': 'HL23PYR', 'cellModel': 'HH_full'},
        fileName='cellwrapper.py',
        cellName='loadCell_HL23PYR',
        cellInstance=True,
        cellArgs=cellArgs
    )

    # Current clamp
    netParams.stimSourceParams['IClamp1'] = {
        'type': 'IClamp',
        'delay': I_START,
        'dur': I_DUR,
        'amp': current_amp
    }

    netParams.stimTargetParams['IClamp1->HL23PYR'] = {
        'source': 'IClamp1',
        'conds': {'pop': 'HL23PYR'},
        'sec': 'soma_0',
        'loc': 0.5
    }

    # Create and run simulation
    sim.initialize(netParams, cfg)
    sim.net.createPops()
    sim.net.createCells()
    sim.net.connectCells()
    sim.net.addStims()
    sim.setupRecording()
    sim.runSim()

    # Extract results
    spkt = np.array(sim.simData['spkt']) if 'spkt' in sim.simData else np.array([])

    # Get voltage trace
    if 'V_soma' in sim.simData:
        if isinstance(sim.simData['V_soma'], dict) and 'cell_0' in sim.simData['V_soma']:
            V_soma = np.array(sim.simData['V_soma']['cell_0'])
        else:
            V_soma = np.array(list(sim.simData['V_soma'].values())[0])
    else:
        V_soma = np.array([])

    t = np.arange(0, len(V_soma)) * cfg.recordStep

    # Calculate firing rate during injection
    injection_spikes = spkt[(spkt >= I_START) & (spkt < I_START + I_DUR)]
    firing_rate = len(injection_spikes) / (I_DUR / 1000.0)  # Hz

    # Calculate mean voltage during injection (after 100ms settling)
    settle_time = I_START + 100  # ms
    settle_idx = int(settle_time / cfg.recordStep)
    end_idx = int((I_START + I_DUR) / cfg.recordStep)
    mean_voltage = np.mean(V_soma[settle_idx:end_idx])

    # Get voltage trace
    voltage_trace = V_soma
    time_trace = t

    # Clean up
    sim.clearAll()

    return firing_rate, mean_voltage, voltage_trace, time_trace


def generate_FI_VI_curves(condition_name, ad_model=False, ad_stage=None):
    """Generate complete F-I and V-I curves for a condition"""

    print(f"\n{'='*70}")
    print(f"Generating F-I and V-I curves for: {condition_name}")
    print(f"{'='*70}")

    currents = np.arange(I_MIN, I_MAX + I_STEP, I_STEP)
    firing_rates = []
    mean_voltages = []
    voltage_traces = []

    for i, current in enumerate(currents):
        print(f"[{i+1}/{len(currents)}] Running I = {current:.3f} nA...", end=' ')

        f_rate, v_mean, v_trace, t_trace = run_single_FI_point(
            current, ad_model=ad_model, ad_stage=ad_stage
        )

        firing_rates.append(f_rate)
        mean_voltages.append(v_mean)
        voltage_traces.append(v_trace)

        print(f"F = {f_rate:.1f} Hz, V = {v_mean:.1f} mV")

    results = {
        'condition': condition_name,
        'currents': currents.tolist(),
        'firing_rates': firing_rates,
        'mean_voltages': mean_voltages,
        'time_trace': t_trace.tolist(),
        'voltage_traces': [vt.tolist() for vt in voltage_traces],
        'ad_model': ad_model,
        'ad_stage': ad_stage
    }

    return results


def plot_FI_VI_curves(all_results):
    """Plot F-I and V-I curves for all conditions"""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    colors = {
        'Healthy': '#2E86AB',
        'AD Stage 1': '#A23B72',
        'AD Stage 2': '#E07A5F',
        'AD Stage 3': '#F18F01'
    }

    markers = {
        'Healthy': 'o',
        'AD Stage 1': 's',
        'AD Stage 2': 'D',
        'AD Stage 3': '^'
    }

    # F-I Curve
    ax = axes[0, 0]
    for result in all_results:
        condition = result['condition']
        ax.plot(result['currents'], result['firing_rates'],
                marker=markers[condition], linewidth=2, markersize=8,
                label=condition, color=colors[condition])

    ax.set_xlabel('Injected Current (nA)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Firing Rate (Hz)', fontsize=12, fontweight='bold')
    ax.set_title('F-I Curve: Firing Rate vs Current', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # V-I Curve
    ax = axes[0, 1]
    for result in all_results:
        condition = result['condition']
        ax.plot(result['currents'], result['mean_voltages'],
                marker=markers[condition], linewidth=2, markersize=8,
                label=condition, color=colors[condition])

    ax.set_xlabel('Injected Current (nA)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Mean Voltage (mV)', fontsize=12, fontweight='bold')
    ax.set_title('V-I Curve: Voltage vs Current', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Example voltage traces (I = 0.2 nA)
    ax = axes[1, 0]
    target_current = 0.2
    for result in all_results:
        condition = result['condition']
        idx = np.argmin(np.abs(np.array(result['currents']) - target_current))
        t = np.array(result['time_trace'])
        v = np.array(result['voltage_traces'][idx])
        ax.plot(t, v, label=condition, color=colors[condition], linewidth=1.5)

    ax.set_xlabel('Time (ms)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Voltage (mV)', fontsize=12, fontweight='bold')
    ax.set_title(f'Example Traces (I = {target_current} nA)', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.set_xlim([400, 1600])
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Excitability comparison (slope of F-I curve at threshold)
    ax = axes[1, 1]

    conditions = []
    gains = []
    rheobase_currents = []

    for result in all_results:
        condition = result['condition']
        currents = np.array(result['currents'])
        f_rates = np.array(result['firing_rates'])

        # Find rheobase (first current that elicits spiking)
        rheobase_idx = np.where(f_rates > 0)[0]
        if len(rheobase_idx) > 0:
            rheobase_idx = rheobase_idx[0]
            rheobase = currents[rheobase_idx]
        else:
            rheobase = np.nan

        # Calculate gain (slope near threshold, between 5-30 Hz)
        valid_idx = (f_rates >= 5) & (f_rates <= 30)
        if np.sum(valid_idx) >= 2:
            gain = np.polyfit(currents[valid_idx], f_rates[valid_idx], 1)[0]
        else:
            gain = np.nan

        conditions.append(condition)
        gains.append(gain)
        rheobase_currents.append(rheobase)

    x_pos = np.arange(len(conditions))
    bars = ax.bar(x_pos, gains, color=[colors[c] for c in conditions],
                   edgecolor='black', linewidth=1.5, alpha=0.8)

    ax.set_xticks(x_pos)
    ax.set_xticklabels(conditions, fontsize=10, rotation=15, ha='right')
    ax.set_ylabel('F-I Gain (Hz/nA)', fontsize=12, fontweight='bold')
    ax.set_title('Excitability: F-I Gain', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Add values on bars
    for i, (bar, gain) in enumerate(zip(bars, gains)):
        if not np.isnan(gain):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                   f'{gain:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig('output/FI_VI_curves_comparison.png', dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved plot: output/FI_VI_curves_comparison.png")

    # Print summary statistics
    print(f"\n{'='*70}")
    print("EXCITABILITY SUMMARY")
    print(f"{'='*70}")
    for condition, gain, rheobase in zip(conditions, gains, rheobase_currents):
        print(f"{condition:15s}: Gain = {gain:6.1f} Hz/nA, Rheobase = {rheobase:.3f} nA")
    print(f"{'='*70}\n")

    return fig


def main():
    print("\n" + "="*70)
    print("F-I AND V-I CURVE GENERATION")
    print("Systematic Current Injection Analysis")
    print("="*70)

    # Generate curves for all four conditions
    all_results = []

    # Healthy
    print("\n[1/4] Healthy Baseline")
    healthy_results = generate_FI_VI_curves('Healthy', ad_model=False)
    all_results.append(healthy_results)

    # Save intermediate
    with open('output/FI_VI_Healthy.json', 'w') as f:
        json.dump(healthy_results, f, indent=2)

    # AD Stage 1
    print("\n[2/4] AD Stage 1 (Early Hyperexcitability)")
    stage1_results = generate_FI_VI_curves('AD Stage 1', ad_model=True, ad_stage=1)
    all_results.append(stage1_results)

    # Save intermediate
    with open('output/FI_VI_AD_Stage1.json', 'w') as f:
        json.dump(stage1_results, f, indent=2)

    # AD Stage 2
    print("\n[3/4] AD Stage 2 (Intermediate Transition)")
    stage2_results = generate_FI_VI_curves('AD Stage 2', ad_model=True, ad_stage=2)
    all_results.append(stage2_results)

    # Save intermediate
    with open('output/FI_VI_AD_Stage2.json', 'w') as f:
        json.dump(stage2_results, f, indent=2)

    # AD Stage 3
    print("\n[4/4] AD Stage 3 (Late Hypoexcitability)")
    stage3_results = generate_FI_VI_curves('AD Stage 3', ad_model=True, ad_stage=3)
    all_results.append(stage3_results)

    # Save intermediate
    with open('output/FI_VI_AD_Stage3.json', 'w') as f:
        json.dump(stage3_results, f, indent=2)

    # Save combined results
    with open('output/FI_VI_all_conditions.json', 'w') as f:
        json.dump(all_results, f, indent=2)

    # Generate comparison plots
    print("\nGenerating comparison plots...")
    plot_FI_VI_curves(all_results)

    print("\n" + "="*70)
    print("✅ F-I AND V-I CURVE GENERATION COMPLETE!")
    print("="*70)
    print("\nGenerated files:")
    print("  - output/FI_VI_curves_comparison.png")
    print("  - output/FI_VI_Healthy.json")
    print("  - output/FI_VI_AD_Stage1.json")
    print("  - output/FI_VI_AD_Stage2.json")
    print("  - output/FI_VI_AD_Stage3.json")
    print("  - output/FI_VI_all_conditions.json")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
