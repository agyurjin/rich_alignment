'''
Data reader
'''

class DataParser:
    '''
    Data reader
    '''
    def __init__(self):
        '''
        init method
        '''
        self.strategy = None

    def set_strategy(self, strategy):
        '''
        set strategy
        '''
        self.strategy = strategy

    def run_strategy(self, file_path):
        '''
        run strategy
        '''
        return self.strategy.read_txt_file(file_path)
