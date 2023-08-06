from cetl import Base, pd, PANDAS_TRANSFORMERS, timeit, DataFrame
from cetl.utils.timer import timeit
import csv
import json

@PANDAS_TRANSFORMERS.add()
class generateDataFrame(Base):
    """
    {"type":"generateDataFrame"}
    """
    def __init__(self, data=None):
        super().__init__()
        self.data = data
    
    @timeit
    def transform(self, input) -> DataFrame:
        
        df = None
        if not self.data:
            self.data = [  {"customer_id":111, "first_name":"peter", "last_name":"Hong", "title":"Mr."},
                                {"customer_id":222, "first_name":"YuCheung", "last_name":"Wong", "title":"Mr."},
                                {"customer_id":333, "first_name":"Cindy", "last_name":"Wong", "title":"Mrs."},
                            ]
            df = pd.DataFrame(self.data)

        return df

