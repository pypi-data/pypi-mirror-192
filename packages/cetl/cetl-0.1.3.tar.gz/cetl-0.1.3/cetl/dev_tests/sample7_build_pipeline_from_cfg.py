import sys 
sys.path.append('.')
from cetl import DataPipeline

cfg = {"pipeline":[ {"type":"dummyStart", "module_type":"functional"},
                    {"type":"parallelTransformer", "transformers":[
                        {"type":"generateDataFrame"},
                        {"type":"generateDataFrame"}
                    ]},
                    {"type":"unionAll"}
]}

pipe = DataPipeline(cfg)
df = pipe.transform("")
# print(df)


pipe = pipe.create_dot_graph()
pipe.save_png("./sample7.png")


# python3.6 cetl/dev_tests/sample7_build_pipeline_from_cfg.py