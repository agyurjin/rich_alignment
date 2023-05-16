#from __future__ import absolute_import
from pathlib import Path

from src.file_handler.data_parser import DataParser

def test_aerogel_reader():
    dp = DataParser()
    data_path = Path('test') /'data'/'RichReco_FastMC.root_hist.root_hm_Aerogel.out'
    aerogel_data = dp.read_file(data_path)
    
    assert aerogel_data['aerogel_b2_dp_chi2'] == 1.2583
    assert aerogel_data['aerogel_b2_a2l_chi2'] == 1.1658
    assert aerogel_data['aerogel_b2_a2r_chi2'] == 1.3175
    assert aerogel_data['aerogel_b2_s5c_b1_chi2'] == 1.2397
    assert aerogel_data['aerogel_b2_s5c_b2_chi2'] == 7.8386    
    assert aerogel_data['aerogel_b2_dp_mean'] == (-0.881)
    assert aerogel_data['aerogel_b2_a2l_mean_err'] == 0.446
    assert aerogel_data['aerogel_b2_a2r_std'] == 5.033
    assert aerogel_data['aerogel_b2_s5c_b1_std_err'] == 0.448
    assert aerogel_data['aerogel_b2_s5c_b2_entries'] == 18
    assert aerogel_data['aerogel_b1_dp_chi2'] == 2.025
    assert aerogel_data['aerogel_b1_a2l_mean'] == 3.756
    assert aerogel_data['aerogel_b1_a2r_std'] == 5.123
    assert aerogel_data['aerogel_b1_s3_b2_entries'] == 22
    assert aerogel_data['aerogel_b1_s4c_b1_chi2'] == 2.7236
    assert aerogel_data['aerogel_b3_a3_mean'] == (-1.243)
    assert aerogel_data['aerogel_b3_other_mean_err'] == 0.325
    assert aerogel_data['aerogel_b3_s2c_b2_std'] == 3.017
    assert aerogel_data['aerogel_b3_s6_b2_std_err'] == 0.022
    assert aerogel_data['aerogel_b3_s3c_b2_entries'] == 10



def test_aerogel_writer():
    dp = DataParser()
    try:
        aerogel_data = dp.create_file(Path('Aerogel.out'), Path('Aerogel.out'), {})
    except Exception as error:
        assert str(error) == 'Aerogel file creation method not implemented as it should be generated from simulations!'
