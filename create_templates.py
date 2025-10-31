"""
create_templates.py
Automatically create cell-specific template files from generic NeuronTemplate.hoc
RUN THIS FIRST before init.py!
"""

import os
import sys

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Cell types
cell_types = ['HL23PYR', 'HL23SST', 'HL23PV', 'HL23VIP']

print("="*70)
print("CREATING CELL-SPECIFIC TEMPLATE FILES")
print("="*70)
print(f"Working directory: {BASE_DIR}")
print(f"Models directory: {MODELS_DIR}")

# Read generic template
generic_template = os.path.join(MODELS_DIR, 'NeuronTemplate.hoc')

if not os.path.exists(generic_template):
    print(f"\n✗ ERROR: Generic template not found: {generic_template}")
    print("\nMake sure you have models/NeuronTemplate.hoc in your directory!")
    sys.exit(1)

print(f"\n✓ Found generic template: {generic_template}")

with open(generic_template, 'r') as f:
    content = f.read()

print(f"✓ Template size: {len(content)} characters\n")

# Create cell-specific templates
created_files = []
for cell_type in cell_types:
    output_file = os.path.join(MODELS_DIR, f'NeuronTemplate_{cell_type}.hoc')
    
    print(f"Creating {os.path.basename(output_file)}...")
    
    # Replace template name
    new_content = content.replace(
        'begintemplate NeuronTemplate',
        f'begintemplate NeuronTemplate_{cell_type}'
    )
    new_content = new_content.replace(
        'endtemplate NeuronTemplate',
        f'endtemplate NeuronTemplate_{cell_type}'
    )
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write(new_content)
    
    created_files.append(output_file)
    print(f"  ✓ Created: {output_file}")

print("\n" + "="*70)
print("VERIFICATION")
print("="*70 + "\n")

# Verify files were created
all_correct = True
for cell_type in cell_types:
    template_file = os.path.join(MODELS_DIR, f'NeuronTemplate_{cell_type}.hoc')
    
    if os.path.exists(template_file):
        # Check content
        with open(template_file, 'r') as f:
            first_line = f.readline().strip()
            f.seek(0)
            lines = f.readlines()
            last_line = lines[-1].strip() if lines else ''
        
        print(f"✓ {os.path.basename(template_file)}")
        
        # Verify template name
        if f'begintemplate NeuronTemplate_{cell_type}' in first_line:
            print(f"  ✓ First line correct: {first_line}")
        else:
            print(f"  ✗ WARNING: First line incorrect: {first_line}")
            all_correct = False
            
        if f'endtemplate NeuronTemplate_{cell_type}' in last_line:
            print(f"  ✓ Last line correct: {last_line}")
        else:
            print(f"  ✗ WARNING: Last line incorrect: {last_line}")
            all_correct = False
    else:
        print(f"✗ MISSING: {template_file}")
        all_correct = False
    
    print()

print("="*70)
if all_correct:
    print("✅ SUCCESS! ALL TEMPLATE FILES CREATED CORRECTLY!")
    print("\nYou can now run: python init.py")
else:
    print("❌ ERRORS DETECTED - Please check the files manually")
    sys.exit(1)
print("="*70 + "\n")
"""
create_templates.py
Automatically create cell-specific template files from generic NeuronTemplate.hoc
"""

import os

BASE_DIR = '/Users/tarek/Desktop/Yao_NetPyNE_100'
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Cell types
cell_types = ['HL23PYR', 'HL23SST', 'HL23PV', 'HL23VIP']

# Read generic template
generic_template = os.path.join(MODELS_DIR, 'NeuronTemplate.hoc')

print("="*70)
print("CREATING CELL-SPECIFIC TEMPLATE FILES")
print("="*70)

if not os.path.exists(generic_template):
    print(f"\nERROR: Generic template not found: {generic_template}")
    exit(1)

print(f"\nReading generic template: {generic_template}")

with open(generic_template, 'r') as f:
    content = f.read()

print(f"Template size: {len(content)} characters")

# Create cell-specific templates
for cell_type in cell_types:
    output_file = os.path.join(MODELS_DIR, f'NeuronTemplate_{cell_type}.hoc')
    
    print(f"\nCreating {os.path.basename(output_file)}...")
    
    # Replace template name
    new_content = content.replace(
        'begintemplate NeuronTemplate',
        f'begintemplate NeuronTemplate_{cell_type}'
    )
    new_content = new_content.replace(
        'endtemplate NeuronTemplate',
        f'endtemplate NeuronTemplate_{cell_type}'
    )
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write(new_content)
    
    print(f"  ✓ Created: {output_file}")
    print(f"  ✓ Size: {len(new_content)} characters")

print("\n" + "="*70)
print("VERIFICATION")
print("="*70)

# Verify files were created
all_exist = True
for cell_type in cell_types:
    template_file = os.path.join(MODELS_DIR, f'NeuronTemplate_{cell_type}.hoc')
    
    if os.path.exists(template_file):
        # Check content
        with open(template_file, 'r') as f:
            first_line = f.readline().strip()
            f.seek(0)
            lines = f.readlines()
            last_line = lines[-1].strip() if lines else ''
        
        print(f"\n✓ {os.path.basename(template_file)}")
        print(f"  First line: {first_line[:60]}...")
        print(f"  Last line:  {last_line[:60]}...")
        
        # Verify template name
        if f'NeuronTemplate_{cell_type}' in first_line:
            print(f"  ✓ Template name correct")
        else:
            print(f"  ✗ WARNING: Template name not found in first line")
            all_exist = False
    else:
        print(f"✗ MISSING: {template_file}")
        all_exist = False

print("\n" + "="*70)
if all_exist:
    print("✓ ALL TEMPLATE FILES CREATED SUCCESSFULLY!")
    print("\nNext step: python init.py")
else:
    print("✗ SOME FILES MISSING OR INCORRECT")
print("="*70)
