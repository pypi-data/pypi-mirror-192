from sklearn.base import BaseEstimator, TransformerMixin

class Base(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.node_id = ""
        self.node_name = ""
        self.description = ""
        self.isParallel = "false"
        self.total_time = 0
        self.total_input = 0
        self.total_output = 0
        self.data_container_type="pandas"


    def fit(self):
        pass
    