<span style="float:right;">[[source]](https://github.com/thepetabyteproject/your/blob/master/your/utils/gpu.py#L11)</span>

### gpu_dedisperse


```python
your.utils.gpu.gpu_dedisperse(cand, device=0)
```


GPU dedispersion (by rolling the array)

Args:

    cand: Candidate instance

    device (int): GPU ID

Returns:

    candidate object


----

<span style="float:right;">[[source]](https://github.com/thepetabyteproject/your/blob/master/your/utils/gpu.py#L55)</span>

### gpu_dmt


```python
your.utils.gpu.gpu_dmt(cand, device=0)
```


GPU DM-Time bow-tie (by rolling the array)

Args:

    cand: Candidate instance

    device (int): GPU ID

Returns:

    candidate object


----

<span style="float:right;">[[source]](https://github.com/thepetabyteproject/your/blob/master/your/utils/gpu.py#L102)</span>

### gpu_dedisp_and_dmt_crop


```python
your.utils.gpu.gpu_dedisp_and_dmt_crop(cand, device=0)
```


GPU based dedispersion, DM time bow-time plot and crop it to 256x256 shaped arrays (by rolling the array)

Args:

    cand: Candidate instance

    device (int): GPU ID

Returns:

    candidate object


----

<span style="float:right;">[[source]](https://github.com/thepetabyteproject/your/blob/master/your/utils/gpu.py#L224)</span>

### get_gpu_memory_map


```python
your.utils.gpu.get_gpu_memory_map(gpu_id)
```


Get the current gpu free memory

Args:

    gpu_id (int): GPU id

Returns:

    int: amount of free GPU RAM


----
