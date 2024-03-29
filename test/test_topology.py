from pathlib import Path

from src.file_handler.data_parser import DataParser

def test_topology_reader():
    dp = DataParser()
    data_path = Path('test') /'data'/'RichReco_FastMC.root_hist.root_hp_dir.out'
    topology_data = dp.read_file(data_path)

    assert topology_data['dir_aerogel_b1_tile_1_mean_err'] == 2.2
    assert topology_data['dir_aerogel_b1_tile_3_entries'] == 100
    assert topology_data['dir_aerogel_b1_tile_3_chi2'] == 2.0
    assert topology_data['dir_aerogel_b1_tile_10_chi2'] == 2.4214
    assert topology_data['dir_aerogel_b1_tile_14_mean'] == -0.124
    assert topology_data['dir_aerogel_b1_tile_21_std'] == -2.354
    assert topology_data['dir_aerogel_b1_tile_22_std_err'] == 3.810
    assert 'dir_aerogel_b1_tile_24_std' not in topology_data
    assert topology_data['dir_aerogel_b2_tile_13_entries'] == 200
    assert topology_data['dir_aerogel_b2_tile_15_mean'] == 2.245
    assert topology_data['dir_aerogel_b2_tile_19_mean_err'] == 0.025
    assert topology_data['dir_aerogel_b2_tile_24_std'] == -2.146
    assert topology_data['dir_aerogel_b2_tile_29_std_err'] == 8.624
    assert 'dir_aerogel_b2_tile_30_mean' not in topology_data
    assert topology_data['dir_aerogel_b3_tile_2_chi2'] == -8.4213
    assert topology_data['dir_aerogel_b3_tile_7_entries'] == 500
    assert topology_data['dir_aerogel_b3_tile_10_mean'] == -10.21
    assert topology_data['dir_aerogel_b3_tile_13_mean_err'] == 23.25
    assert topology_data['dir_aerogel_b3_tile_19_std'] == 0.001
    assert topology_data['dir_aerogel_b3_tile_24_std_err'] == 12.23
    assert topology_data['dir_aerogel_b3_tile_30_chi2'] == 21.281
    assert topology_data['dir_aerogel_b3_tile_35_std'] == 2.223
    assert 'dir_aeorgel_b3_tile_35_chi2' not in topology_data
    assert 'dir_aerogel_b4_tile_1_chi2' not in topology_data
    assert 'planaA1L_aerogel_b2_tile_19_mean_err' not in topology_data


def test_topology_writer():
    dp = DataParser()
    try:
        topology_data = dp.create_file(Path('dir.out'), Path('dir.out'), {})
    except Exception as error:
        assert str(error) == 'Topology file creation method not implemented as it should be created during the simulation!'
