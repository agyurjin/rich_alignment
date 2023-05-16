from tempfile import TemporaryDirectory
from pathlib import Path

from src.file_handler.data_parser import DataParser

def test_geometry_v1_reader():
    dp = DataParser()
    data_path = Path('test')/'data'/'RichModGeometry_v1.dat'
    geometry_data = dp.read_file(data_path)

    assert geometry_data['aerogel_b1_x'] == 2.1 
    assert geometry_data['aerogel_b1_theta_y'] == -0.003 
    assert geometry_data['aerogel_b2_z'] == 2.4
    assert geometry_data['aerogel_b2_theta_x'] == 0.1
    assert geometry_data['aerogel_b3_y'] == 0.1 
    assert geometry_data['aerogel_b3_theta_z'] == 0.02
    assert geometry_data['frontal_mirror_b1_x'] == -2.1
    assert geometry_data['frontal_mirror_b1_theta_y'] == 2.0 
    assert geometry_data['frontal_mirror_b2_z'] == 5.0
    assert geometry_data['frontal_mirror_b2_theta_x'] == -4.2  
    assert geometry_data['planar_mirror_l_z'] == -1.3 
    assert geometry_data['planar_mirror_l_theta_y'] == -2.3
    assert geometry_data['planar_mirror_r_y'] == -1.3
    assert geometry_data['planar_mirror_r_theta_x'] == -2.3
    assert geometry_data['planar_mirror_a3_x'] == 1.0
    assert geometry_data['planar_mirror_a3_theta_y'] == 2.0
    assert geometry_data['spherical_mirror_s5c_x'] == 2.0
    assert geometry_data['spherical_mirror_s5c_theta_z'] == 0.0 
    assert geometry_data['mapmt_z'] == 3.0
    assert geometry_data['mapmt_theta_y'] == -2.3

    assert 'spherical_mirror_s5c_b1_x' not in geometry_data
    assert 'planar_mirror_a1r_y' not in geometry_data

def test_geometry_v2_reader():
    dp = DataParser()
    data_path = Path('test')/'data'/'RichModGeometry_v2.dat'
    geometry_data = dp.read_file(data_path)
    
    assert geometry_data['aerogel_b1_x'] == 1.8 
    assert geometry_data['aerogel_b1_theta_y'] == -0.003 
    assert geometry_data['aerogel_b2_z'] == 6.0
    assert geometry_data['aerogel_b2_theta_x'] == -0.06
    assert geometry_data['aerogel_b3_y'] == 0.
    assert geometry_data['aerogel_b3_theta_z'] == 0.0
    assert geometry_data['frontal_mirror_b1_x'] == 0.3
    assert geometry_data['frontal_mirror_b1_theta_y'] == -0.04 
    assert geometry_data['frontal_mirror_b2_z'] == 6.0
    assert geometry_data['frontal_mirror_b2_theta_x'] == 0.006  
    assert geometry_data['planar_mirror_a2l_z'] == 1.5
    assert geometry_data['planar_mirror_a2l_theta_x'] == -0.02
    assert geometry_data['planar_mirror_a3_y'] == 2.0
    assert geometry_data['planar_mirror_a3_theta_x'] == 1.0
    assert geometry_data['planar_mirror_a1r_y'] == -1.3
    assert geometry_data['planar_mirror_a1r_theta_x'] == -2.3
    assert geometry_data['spherical_mirror_s2_x'] == 8.5
    assert geometry_data['spherical_mirror_s2_theta_y'] == -2.4
    assert geometry_data['spherical_mirror_s2c_x'] == -1.2
    assert geometry_data['spherical_mirror_s2c_theta_y'] == 2.0
    assert geometry_data['spherical_mirror_s5c_x'] == 2.0
    assert geometry_data['spherical_mirror_s5c_theta_z'] == 0.0 
    assert geometry_data['mapmt_y'] == 3.2
    assert geometry_data['mapmt_theta_y'] == -1.0

    assert 'planar_mirror_l_z' not in geometry_data
    assert 'planar_mirror_r_theta_x' not in geometry_data


def test_geometry_v1_writer():
    out_path = None
    with TemporaryDirectory() as dir_name:
        out_path = Path(dir_name) / 'test_RichModGeometry_v1.dat'

        evt_dict = {
            'planar_mirror_l_z': 1.5,
            'aerogel_b2_theta_z': 2.56,
            'planar_mirror_a3_z': 3.26,
            'spherical_mirror_s5c_z': -6.25,
            'spherical_mirror_s5c_theta_z': -0.1,
            'aerogel_b3_theta_x': -5.23,
            'planar_mirror_r_theta_x': 2.3
        }
        dp = DataParser()
        data_path = Path('test') /'data'/'RichModGeometry_v1.dat'
        dp.create_file(out_path, data_path, evt_dict)
        
        data_old = dp.read_file(data_path)
        data_new = dp.read_file(out_path)
        for key,value in evt_dict.items():
            assert data_new[key] == value
            assert data_new[key] != data_old[key]
        

def test_geometry_v2_writer():
    out_path = None
    with TemporaryDirectory() as dir_name:
        out_path = Path(dir_name) / 'test_RichModGeometry_v2.dat'
            
        evt_dict = {
            'frontal_mirror_b1_z': 1.3,
            'frontal_mirror_b1_theta_x': 2.35,
            'aerogel_b2_x': -3.0,
            'frontal_mirror_b2_theta_x': 0.007,
            'planar_mirror_a2l_x': -1.5,
            'planar_mirror_a2l_theta_z': -0.08,
            'planar_mirror_a3_x': -2.0,
            'planar_mirror_a3_theta_z': -1.0,
            'spherical_mirror_s5c_z': 2.0
        }
        dp = DataParser()
        data_path = Path('test') / 'data'/'RichModGeometry_v2.dat'
        dp.create_file(out_path, data_path, evt_dict)


        data_old = dp.read_file(data_path)
        data_new = dp.read_file(out_path)
        for key,value in evt_dict.items():
            assert data_new[key] == value
            assert data_new[key] != data_old[key]



