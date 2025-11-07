"""
Analyze and compare network simulation results across all three conditions
"""
import json
import numpy as np
import pandas as pd
import os

def load_simulation(json_file):
    """Load simulation data from JSON file"""
    with open(json_file) as f:
        data = json.load(f)
    return data

def analyze_population_activity(data, duration_ms=2000):
    """Extract population-level firing statistics"""

    # Get spike data
    spike_times = np.array(data['simData']['spkt'])
    spike_gids = np.array(data['simData']['spkid'])

    # Duration in seconds
    duration_s = duration_ms / 1000.0

    # Population GID ranges (from cfg.py)
    pop_ranges = {
        'HL23PYR': (0, 80),
        'HL23SST': (80, 88),
        'HL23PV': (88, 94),
        'HL23VIP': (94, 100)
    }

    results = {}

    for pop_name, (gid_start, gid_end) in pop_ranges.items():
        # Get spikes for this population
        pop_mask = (spike_gids >= gid_start) & (spike_gids < gid_end)
        pop_spikes = spike_times[pop_mask]
        pop_gids = spike_gids[pop_mask]

        # Calculate statistics
        n_cells = gid_end - gid_start
        total_spikes = len(pop_spikes)
        avg_rate = total_spikes / (n_cells * duration_s) if n_cells > 0 else 0

        # Per-cell firing rates
        cell_rates = []
        for gid in range(gid_start, gid_end):
            cell_spikes = np.sum(spike_gids == gid)
            cell_rate = cell_spikes / duration_s
            cell_rates.append(cell_rate)

        # Synchrony measure (coefficient of variation of ISIs)
        if len(pop_spikes) > 1:
            isis = np.diff(np.sort(pop_spikes))
            cv_isi = np.std(isis) / np.mean(isis) if np.mean(isis) > 0 else 0
        else:
            cv_isi = 0

        results[pop_name] = {
            'n_cells': n_cells,
            'total_spikes': total_spikes,
            'avg_rate_hz': avg_rate,
            'rate_std': np.std(cell_rates),
            'cv_isi': cv_isi,
            'active_cells': np.sum(np.array(cell_rates) > 0)
        }

    return results

def main():
    print("="*80)
    print("NETWORK SIMULATION RESULTS: Healthy vs AD Stage 1 vs AD Stage 3")
    print("="*80)

    # File paths
    files = {
        'Healthy': 'output/Yao_L23_100cell_data.json',
        'AD Stage 1': 'output/Yao_L23_100cell_AD_Stage1_data.json',
        'AD Stage 3': 'output/Yao_L23_100cell_AD_Stage3_data.json'
    }

    all_results = {}

    for condition, filepath in files.items():
        if os.path.exists(filepath):
            print(f"\n[Loading] {condition}...")
            data = load_simulation(filepath)
            results = analyze_population_activity(data)
            all_results[condition] = results
            print(f"✓ {condition} loaded successfully")
        else:
            print(f"✗ {condition} file not found: {filepath}")
            all_results[condition] = None

    # Create comparison table for HL23PYR (pyramidal neurons)
    print("\n" + "="*80)
    print("HL23PYR POPULATION COMPARISON (80 pyramidal neurons)")
    print("="*80)

    pyr_data = []
    for condition in ['Healthy', 'AD Stage 1', 'AD Stage 3']:
        if all_results[condition] is not None:
            pyr_stats = all_results[condition]['HL23PYR']
            pyr_data.append({
                'Condition': condition,
                'Total Spikes': pyr_stats['total_spikes'],
                'Avg Rate (Hz)': f"{pyr_stats['avg_rate_hz']:.2f}",
                'Std Dev (Hz)': f"{pyr_stats['rate_std']:.2f}",
                'Active Cells': f"{pyr_stats['active_cells']}/80",
                'CV ISI': f"{pyr_stats['cv_isi']:.3f}"
            })

    pyr_df = pd.DataFrame(pyr_data)
    print(pyr_df.to_string(index=False))

    # Calculate percent changes
    if all_results['Healthy'] and all_results['AD Stage 1']:
        healthy_rate = all_results['Healthy']['HL23PYR']['avg_rate_hz']
        stage1_rate = all_results['AD Stage 1']['HL23PYR']['avg_rate_hz']
        pct_change_s1 = 100 * (stage1_rate - healthy_rate) / healthy_rate if healthy_rate > 0 else 0

        print(f"\n**AD Stage 1 vs Healthy**: {pct_change_s1:+.1f}% change in firing rate")

        if pct_change_s1 > 0:
            print("  → ✓ HYPEREXCITABILITY confirmed!")
        else:
            print("  → ⚠ Expected hyperexcitability, but got reduction")

    if all_results['Healthy'] and all_results['AD Stage 3']:
        healthy_rate = all_results['Healthy']['HL23PYR']['avg_rate_hz']
        stage3_rate = all_results['AD Stage 3']['HL23PYR']['avg_rate_hz']
        pct_change_s3 = 100 * (stage3_rate - healthy_rate) / healthy_rate if healthy_rate > 0 else 0

        print(f"**AD Stage 3 vs Healthy**: {pct_change_s3:+.1f}% change in firing rate")

        if pct_change_s3 < 0:
            print("  → ✓ HYPOEXCITABILITY confirmed!")
        else:
            print("  → ⚠ Expected hypoexcitability, but got increase")

    # Full population summary
    print("\n" + "="*80)
    print("ALL POPULATIONS SUMMARY")
    print("="*80)

    for condition in ['Healthy', 'AD Stage 1', 'AD Stage 3']:
        if all_results[condition] is not None:
            print(f"\n[{condition}]")
            for pop in ['HL23PYR', 'HL23SST', 'HL23PV', 'HL23VIP']:
                stats = all_results[condition][pop]
                print(f"  {pop:10s}: {stats['avg_rate_hz']:6.2f} Hz "
                      f"({stats['active_cells']}/{stats['n_cells']} active)")

    # Save summary
    summary_file = 'output/network_comparison_summary.txt'
    with open(summary_file, 'w') as f:
        f.write("NETWORK SIMULATION COMPARISON\n")
        f.write("="*80 + "\n\n")
        f.write(pyr_df.to_string(index=False))
        f.write("\n\n")
        if all_results['Healthy'] and all_results['AD Stage 1']:
            f.write(f"AD Stage 1 vs Healthy: {pct_change_s1:+.1f}% change\n")
        if all_results['Healthy'] and all_results['AD Stage 3']:
            f.write(f"AD Stage 3 vs Healthy: {pct_change_s3:+.1f}% change\n")

    print(f"\n[SAVED] {summary_file}")
    print("="*80)

if __name__ == '__main__':
    main()
