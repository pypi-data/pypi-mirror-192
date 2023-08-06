from ..utils.builder import DataFrame, FUNCTIONAL_TRANSFORMERS
from ..utils.base import Base
from ..utils.timer import timeit


@FUNCTIONAL_TRANSFORMERS.add()
class passDataFrame(Base):
    """do nothing
    {"type":"passDataFrame", "data_container_type":"functional"}
    """
    def __init__(self):
        super().__init__()
        pass

    @timeit
    def transform(self, input_data):
        return input_data


@FUNCTIONAL_TRANSFORMERS.add()
class dummyStart(Base):
    """do nothing
    {"type":"dummyStart", "data_container_type":"functional"}
    """
    def __init__(self):
        super().__init__()
        pass

    @timeit
    def transform(self, input):
        return ""
