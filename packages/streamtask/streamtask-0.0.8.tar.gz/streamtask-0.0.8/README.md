# Streamtask
**Streamtask** is a lightweight python parallel framework for parallelizing the computationally intensive pipelines. It is similar to Map/Reduce, while it is more lightweight. It parallelizes each module in the pipeline with a given processing number to make it possible to leverage the different speeds in different modules. It improves the performance especially there are some heavy I/O operations in the pipeline.

### Example
Suppose we want to process the data in a pipline with 3 blocks, f1, f2 and f3. We can use the following code to  parallelize the processing.

``` python
def f1(total):
    import time
    for i in range(total):
        time.sleep(0.002)
        yield i * 2

def f2(n, add, third = 0.01):
    time.sleep(0.02)
    return n + add + third

def f3_the_final(n):
    time.sleep(0.03)
    return n + 1

if __name__ == "__main__":
    total = 10000
    sl = StreamTask(parallel = False, total = total)
    sl.add_module(f1, 1, total = total)
    sl.add_module(f2, 2, args = [0.5], third = 0.02)
    sl.add_module(f3_the_final, 2)
    sl.run(parallel = True)
    sl.join()
    print(sl.get_results())
```

```
f1 (1):  17%|███████▎                                   | 1692/10000 [00:04<00:19, 419.46it/s]
f2 (2):  23%|██████████▋                                   | 394/1690 [00:04<00:13, 97.68it/s]
f3_the_final (2):  67%|████████████████████████▋            | 262/392 [00:04<00:02, 64.96it/s]
```