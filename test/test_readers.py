from ..readers.data_parser import DataParser
from ..readers.readers import GeometryReader, AerogelReader

def test_geometry_reader():
    dp = DataParser()
    dp.set_strategy(GeometryReader())
    geometry_data = dp.run_strategy('data/RichModGeometry.dat')
    assert geometry_data['aerogel_b2_z'] == 1.0
    assert geometry_data['aerogel_b2_theta_x'] == 0.004
    assert geometry_data['aerogel_b2_theta_y'] == 0.0

def test_aerogel_reader():
    dp = DataParser()
    dp.set_strategy(AerogelReader())
    aerogel_data = dp.run_strategy('data/RichReco_FastMC.root_hist.root_Aerogel.out')
    assert aerogel_data['aerogel_b2_dp_chi2'] == 144.1
    assert aerogel_data['aerogel_b2_s5c_b2_chi2'] == 16.6


