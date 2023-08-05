from .registry import Registry
import pandas as pd
DataFrame = pd.DataFrame
# pd.set_option('display.max_columns', None)
FUNCTIONAL_TRANSFORMERS = Registry("functional_modules")
PANDAS_TRANSFORMERS = Registry("pandas_modules")
JSON_TRANSFORMERS = Registry("json_modules")
SPARK_TRANSFORMERS = Registry("spark_modules")
TEST_TRANSFORMERS = Registry("test_modules")


DB_MAPPERS = Registry("src_db_mappers")
# tenant388_transaction_models =Registry("tenant388_transaction models")
# TB_MODELS = {"tenant388_transaction":tenant388_transaction_models}
DB_MODELS = Registry("db models")




def get_register(data_container_type):
    # print("data_container_type:", data_container_type)
    TRANSFORMERS=None
    # data_container_type is like "pandas", "json" or "spark"
    if data_container_type=="functional":
        TRANSFORMERS = FUNCTIONAL_TRANSFORMERS
    elif data_container_type=="pandas":
        TRANSFORMERS = PANDAS_TRANSFORMERS
    elif data_container_type=="json":
        TRANSFORMERS = JSON_TRANSFORMERS
    elif data_container_type=="spark":
        TRANSFORMERS = SPARK_TRANSFORMERS
    elif data_container_type=="":
        TRANSFORMERS = PANDAS_TRANSFORMERS
        # print(TRANSFORMERS)
    else:
        raise ValueError(f"data_container_type, {data_container_type} is not recognized by cetl")

    # print(TRANSFORMERS)

    return TRANSFORMERS



def build_transformer_from_cfg(cfg, registry, parallel_transformers=None):
    args = cfg.copy()
    transformer_type = args.pop("type")
    
    cls_obj = registry.module_dict[transformer_type]
    
    transformer=None
    if transformer_type=="parallelTransformer":
        transformer = cls_obj(parallel_transformers)
        
    else:
        transformer = cls_obj(**args)

    return transformer