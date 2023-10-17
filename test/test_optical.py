from tempfile import TemporaryDirectory
from pathlib import Path

from src.file_handler.data_parser import DataParser


def test_optical_reader():
    dp = DataParser()
    data_path = Path('test')/'data'/'RichModOptical.dat'
    optical_data = dp.read_file(data_path)

    assert optical_data['aerogel_b1_ref_index'] == 1.05
    assert optical_data['aerogel_b2_Npe'] == 12
    assert optical_data['aerogel_b3_smearing'] == 0.0045
    assert optical_data['aerogel_b3_efficiency'] == 0.9
    assert 'frontal_mirror_b1_ref_index' not in optical_data
    assert 'frontal_mirror_b2_Npe' not in optical_data
    assert optical_data['planar_mirror_a2l_smearing'] == 0
    assert optical_data['planar_mirror_a2r_efficiency'] == 0.9
    assert optical_data['planar_mirror_a3_efficiency'] == 0.9
    assert optical_data['spherical_mirror_s5c_efficiency'] == 0.9
    assert optical_data['mapmt_efficiency'] == 1.
    assert optical_data['mapmt_avg_hits'] == 1.
    assert 'mapmt_smearing' not in optical_data


def test_optical_writer():
    with TemporaryDirectory() as dir_name:
        out_path = Path(dir_name) / 'test_RichModOptical.dat'
        
        evt_dict = {
            'aerogel_b3_smearing': 1.2,
            'planar_mirror_a1l_smearing': 3.5,
            'spherical_mirror_s5c_efficiency': 1.2,
            'planar_mirror_a1r_efficiency': 0.8,
            'mapmt_avg_hits': 2.3
        }

        dp = DataParser()
        data_path = Path('test')/'data'/'RichModOptical.dat'
        dp.create_file(out_path, data_path, evt_dict)

        data_old = dp.read_file(data_path)
        data_new = dp.read_file(out_path)
        for key,value in evt_dict.items():
            assert data_new[key] == value
            assert data_new[key] != data_old[key]
