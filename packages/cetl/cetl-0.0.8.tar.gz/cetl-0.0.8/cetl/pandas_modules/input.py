from cetl import Base, pd, PANDAS_TRANSFORMERS
from cetl.utils.timer import timeit
from cetl import DataFrame
import csv
import json

@PANDAS_TRANSFORMERS.add()
class readCSV(Base):
    def __init__(self,
                filepath=None , 
                delimiter=","):
        """
        the value of "keep" can be "last", False, "first"
        {"type":"readCSVAsJson", "filepath":"/home/clement/data/data_warehouse/Orders.csv", 
            "delimiter":","}
        """
        self.filepath = filepath
        self.delimiter=delimiter

    @timeit
    def transform(self, input_data):

        data = []
        with open(self.filepath, encoding='utf-8') as f:
            csvReader = csv.DictReader(f, delimiter=self.delimiter)
            # csvReader = csv.reader(f, delimiter=self.delimiter)
        
            # data = list(csvReader)
            for row in csvReader:
                data.append(row)

        json_str = json.dumps({"json_data":data}, indent=4)

        json_obj = json.loads(json_str)

        return json_obj

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

