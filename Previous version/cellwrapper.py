"""
Cell Wrapper - Fernando Borges Style
Functions to load Yao et al. 2022 cell models with full biophysics
Based on Human_L23_NetPyNE/cellwrapper.py
Uses GENERIC NeuronTemplate.hoc for all cell types
"""

from neuron import h

def loadCell_HL23PYR(cellName='HL23PYR'):
    """Load HL23 Pyramidal cell"""
    
    templatepath = 'models/NeuronTemplate.hoc'  # Generic template
    biophysics = f'models/biophys_{cellName}.hoc'
    morphpath = f'morphologies/{cellName}.swc'

    h.load_file("stdrun.hoc")
    h.load_file('import3d.hoc')
    h.xopen(biophysics)
    
    try:
        h.xopen(templatepath)
    except:
        pass

    cell = h.NeuronTemplate(morphpath)  # Generic class, pass morphology
    h.biophys_HL23PYR(cell)

    print(f"Loaded {cellName}")
    return cell


def loadCell_HL23SST(cellName='HL23SST'):
    """Load HL23 SST interneuron"""
    
    templatepath = 'models/NeuronTemplate.hoc'  # Generic template
    biophysics = f'models/biophys_{cellName}.hoc'
    morphpath = f'morphologies/{cellName}.swc'

    h.load_file("stdrun.hoc")
    h.load_file('import3d.hoc')
    h.xopen(biophysics)
    
    try:
        h.xopen(templatepath)
    except:
        pass

    cell = h.NeuronTemplate(morphpath)  # Generic class, pass morphology
    h.biophys_HL23SST(cell)

    print(f"Loaded {cellName}")
    return cell


def loadCell_HL23PV(cellName='HL23PV'):
    """Load HL23 PV interneuron"""
    
    templatepath = 'models/NeuronTemplate.hoc'  # Generic template
    biophysics = f'models/biophys_{cellName}.hoc'
    morphpath = f'morphologies/{cellName}.swc'

    h.load_file("stdrun.hoc")
    h.load_file('import3d.hoc')
    h.xopen(biophysics)
    
    try:
        h.xopen(templatepath)
    except:
        pass

    cell = h.NeuronTemplate(morphpath)  # Generic class, pass morphology
    h.biophys_HL23PV(cell)

    print(f"Loaded {cellName}")
    return cell


def loadCell_HL23VIP(cellName='HL23VIP'):
    """Load HL23 VIP interneuron"""
    
    templatepath = 'models/NeuronTemplate.hoc'  # Generic template
    biophysics = f'models/biophys_{cellName}.hoc'
    morphpath = f'morphologies/{cellName}.swc'

    h.load_file("stdrun.hoc")
    h.load_file('import3d.hoc')
    h.xopen(biophysics)
    
    try:
        h.xopen(templatepath)
    except:
        pass

    cell = h.NeuronTemplate(morphpath)  # Generic class, pass morphology
    h.biophys_HL23VIP(cell)

    print(f"Loaded {cellName}")
    return cell


def test_all_cells():
    """Test loading all cell types"""
    print("="*60)
    print("Testing Cell Loading")
    print("="*60)
    
    cells = {}
    
    try:
        print("\nLoading PYR...")
        cells['PYR'] = loadCell_HL23PYR()
        print("✓ PYR loaded successfully")
    except Exception as e:
        print(f"✗ PYR failed: {e}")
    
    try:
        print("\nLoading SST...")
        cells['SST'] = loadCell_HL23SST()
        print("✓ SST loaded successfully")
    except Exception as e:
        print(f"✗ SST failed: {e}")
    
    try:
        print("\nLoading PV...")
        cells['PV'] = loadCell_HL23PV()
        print("✓ PV loaded successfully")
    except Exception as e:
        print(f"✗ PV failed: {e}")
    
    try:
        print("\nLoading VIP...")
        cells['VIP'] = loadCell_HL23VIP()
        print("✓ VIP loaded successfully")
    except Exception as e:
        print(f"✗ VIP failed: {e}")
    
    print("\n" + "="*60)
    print(f"Successfully loaded {len(cells)}/4 cell types")
    print("="*60)
    
    return cells


if __name__ == '__main__':
    test_all_cells()