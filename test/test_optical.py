from tempfile import TemporaryDirectory
from pathlib import Path

from src.file_handler.data_parser import DataParser


def test_optical_reader():
    dp = DataParser()
    optical_data = dp.read_file('test/data/RichModOptical.dat')

    assert optical_data['aerogel_b1_ref_index'] == 1.05
    assert optical_data['aerogel_b2_Npe'] == 12
    assert optical_data['aerogel_b3_smearing'] == 0.0045
    assert optical_data['aerogel_b3_efficiency'] == 0.9
    assert 'frontal_mirror_b1_ref_index' not in optical_data
    assert 'frontal_mirror_b2_Npe' not in optical_data
    assert optical_data['planar_mirror_l_smearing'] == 0
    assert optical_data['planar_mirror_r_efficiency'] == 0.9
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
            'planar_mirror_l_smearing': 3.5,
            'spherical_mirror_s5c_efficiency': 1.2,
            'planar_mirror_r_efficiency': 0.8,
            'mapmt_avg_hits': 2.3
        }

        dp = DataParser()
        dp.create_file(str(out_path), 'test/data/RichModOptical.dat', evt_dict)

        data_old = dp.read_file('test/data/RichModOptical.dat')
        data_new = dp.read_file(str(out_path))
        for key,value in evt_dict.items():
            assert data_new[key] == value
            assert data_new[key] != data_old[key]
