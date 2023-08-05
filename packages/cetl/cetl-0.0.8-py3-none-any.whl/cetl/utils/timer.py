from functools import wraps
import time

def timeit(func):
    """
    Usage
    ----------------------------
    class Calculator:
        @timeit
        def calculate_something(self, num):
            total = sum((x for x in range(0, num**2)))
            return total

        def __repr__(self):
            return f'calc_object:{id(self)}'
    Reference
    ---------------------------
    https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk
    """

    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        
        # Calculate the execution time
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')

        # Adding the execution time to the transformer
        self = args[0]
        #output data of the func: args[1]
        self.total_time = total_time
        # print(self)
        # parallelTransformer will make it run double times, not solved yet
        if self.node_name:
            print(f"{self.node_name}: take time {total_time:.4f} seconds")

        return result

    return timeit_wrapper


