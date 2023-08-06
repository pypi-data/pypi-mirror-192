import sys
import os
from cetl import DataFrame
from cetl import PANDAS_TRANSFORMERS, Base, timeit

@PANDAS_TRANSFORMERS.add()
class addHeaders2Dataframe(Base):
    def __init__(self, headers=None):
        self.headers=headers



    @timeit
    def transform(self, dataframe: DataFrame):
        #skip transformation if dataframe is an empty dataframe
        if dataframe.empty:
            return dataframe
            
        df = dataframe
        # df = df.rename(columns={'oldName1': 'newName1', 'oldName2': 'newName2'})
        df.columns = self.headers
        # print(df)

        return df


@PANDAS_TRANSFORMERS.add()
class renameDataframeHeaders(Base):
    """
    {"type":"renameDataframeHeaders", "headers_dict":{}}
    """
    def __init__(self, headers_dict=None):
        self.headers_dict = headers_dict



    @timeit
    def transform(self, dataframe:DataFrame):
        if dataframe.empty:
            return dataframe

        df = dataframe
        df = df.rename(self.headers_dict, axis=1)

        return df



@PANDAS_TRANSFORMERS.add()
class selectOneDataFrameFromMultiple(Base):
    """
    {"type":"selectOneDataFrameFromMultiple", "position":1}
    """
    def __init__(self, position=None):
        self.position = position



    @timeit
    def transform(self, dataframes:list):

        df = dataframes[self.position]

        return df


@PANDAS_TRANSFORMERS.add()
class addOneMoreDataFrameFromExistingDataframe(Base):
    """
    {"type":"addOneMoreDataFrameFromExistingDataframe", "subset":[]}
    """
    def __init__(self, subset=None):
        self.subset = subset



    @timeit
    def transform(self, dataframe):

        df = dataframe[self.subset]

        return [dataframe, df]