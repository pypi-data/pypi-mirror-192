import sys 
sys.path.append('.')
from cetl import DataPipeline




from cetl import build_pipeline
from cetl.pandas_modules import generateDataFrame, unionAll
from cetl.functional_modules import dummyStart, parallelTransformer

pipe = build_pipeline(   dummyStart(),
                        parallelTransformer([generateDataFrame(), generateDataFrame()]), 
                        unionAll())
df = pipe.transform("")
print(df)


pipe = pipe.create_dot_graph()
pipe.save_png("./sample6.png")


# python3.6 cetl/dev_tests/sample6_build_pipeline.py