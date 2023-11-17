from pathlib import Path
import tempfile

from src.rich_alignment import RICHAlignment

jsons_path = Path('test')/'jsons'

def test_mixed_data():
    geo_path = Path('test')/'data'/'RichModGeometry.dat'
    opt_path = Path('test')/'data'/'RichModOptical.dat'
        
    output_path = Path(tempfile.TemporaryDirectory().name)
    rich_align = RICHAlignment(jsons_path)
    rich_align.create_data(output_path, 10, geo_path, opt_path)
    assert len(list(output_path.glob('opt/*.dat'))) == 10
    assert len(list(output_path.glob('geo/*.dat'))) == 10
    assert len(list(output_path.glob('*.root'))) == 1

    
def test_only_opt_data():
    opt_path = Path('test')/'data'/'RichModOptical.dat'

    output_path = Path(tempfile.TemporaryDirectory().name)
    rich_align = RICHAlignment(jsons_path)
    rich_align.create_data(output_path, 10, None, opt_path)
    assert len(list(output_path.glob('opt/*.dat'))) == 10
    assert len(list(output_path.glob('*.root'))) == 1

def test_only_geo_data():
    geo_path = Path('test')/'data'/'RichModGeometry.dat'

    output_path = Path(tempfile.TemporaryDirectory().name)
    rich_align = RICHAlignment(jsons_path)
    rich_align.create_data(output_path, 10, geo_path, None)
    assert len(list(output_path.glob('geo/*.dat'))) == 10
    assert len(list(output_path.glob('*.root'))) == 1

