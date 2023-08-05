from cetl import FUNCTIONAL_TRANSFORMERS, Base, timeit, pd
import copy

@FUNCTIONAL_TRANSFORMERS.add()
class parallelTransformer(Base):
    def __init__(self, transformers: list):
        # super().__init()
        self.transformers = transformers

    # @timeit
    def transform(self, X)-> list:
        if isinstance(X, list):
            X=X
        elif X is None:
            X = ""
            X = [X for i in range(len(self.transformers))]
        else:
            X = [copy.deepcopy(X) for i in range(len(self.transformers))]

        # print(X)
        # assert len(X)>0
        outputs = []
        for i, transformer in enumerate(self.transformers):
            outputs.append(transformer.transform(X[i]))

        return outputs

