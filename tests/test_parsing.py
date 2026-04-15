import sys
import os
import pytest

# Add python directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python'))

from pcb_processing import parse_mnt_file, parse_pcb_config, parse_pcb_pads_file

def test_parse_mnt_file():
    mnt_path = "test_images/pcb.mnt"
    components = parse_mnt_file(mnt_path)
    assert len(components) > 0
    # Check a specific component
    c3 = next((c for c in components if c['designator'] == 'C3'), None)
    assert c3 is not None
    assert c3['x'] == 43.18
    assert c3['y'] == 20.00
    assert c3['package'] == '0402-B'

def test_parse_pcb_config():
    cfg_path = "test_images/pcb.cfg"
    cfg = parse_pcb_config(cfg_path)
    assert cfg['pcb_width'] == 101.60
    assert cfg['pcb_height'] == 57.15

def test_parse_pcb_pads_file():
    csv_path = "test_images/pcb.csv"
    pads = parse_pcb_pads_file(csv_path)
    assert len(pads) > 0
    # Check a specific pad
    pad1 = next((p for p in pads if p['component'] == 'BETA' and p['pin'] == 1), None)
    assert pad1 is not None
    assert pad1['x'] == 19.6000
    assert pad1['y'] == 24.4250
