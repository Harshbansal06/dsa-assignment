# DSA Assignments - IIITDM Jabalpur

Python coursework covering programming basics, algorithm analysis, recursion, and data structures.

**Name** : Harsh Bansal
**Roll No.:**25BEC039


## Assignments

|File| Topics |
|----|---|
| [Assignment1.ipynb](Assignment1.ipynb) | Python basics, collections, strings, functions, file handling, exception handling, GPA calculator, and student records |
|[Assignment-2.py](Assignment-2.py)| Algorithm growth rates, execution-time benchmarks, and quadratic versus linear prefix averages |
| [Assignment-3.py](Assignment-3.py) | Recursive factorial, natural-number sum, power, sorted-order checking, stack, circular queue, and circular deque |

reference PDFs for the assignments are included in the repo.

## Running the code

Use Python 3. Assignment 2 needs matplotlib, for Assignment 1 you need Jupyter Notebook (or some editor with notebook support).

install dependencies:

```sh
python -m pip install matplotlib notebook
```

run the scripts from repo folder:

```bash
python Assignment-2.py
python Assignment-3.py
```

to open Assignment 1 :

```
python -m notebook Assignment1.ipynb
```

Run cells in order, enter input when asked. type `6` to quit the student-record menu.

### Benchmark plots

Assignment 2 prints timing results and saves plots in current working directory :

* [lab1_execution_times.png](lab1_execution_times.png) : execution times for six algorithm growth classes
- [lab1_normalized_times.png](lab1_normalized_times.png): timings divided by `n`, `n^2`, `n log2(n)`.
+ [lab2_prefix_averages.png](lab2_prefix_averages.png) : comparison of two prefix-average implementations.

Benchmarks use seven trials, reports median execution times. results vary from machine to machine and with system load.
