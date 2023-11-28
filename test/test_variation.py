from pathlib import Path

from src.file_handler.data_parser import DataParser


def test_variation_reader():
    dp = DataParser()
    data_path = Path('test') /'data'/'testVariation.dat'
    variation_data = dp.read_file(data_path)

    assert variation_data['total_rich_x'] == 1.8
    assert variation_data['aerogel_1_z'] == 1.18
    assert variation_data['aerogel_0_tile_13_theta_z'] == 3.0
    assert variation_data['aerogel_2_1_theta_x'] == 7.92
    assert variation_data['aerogel_2_2_theta_x'] == variation_data['aerogel_2_1_theta_x']


