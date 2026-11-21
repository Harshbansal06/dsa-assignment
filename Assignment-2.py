import random
from math import log2
from time import perf_counter
import matplotlib.pyplot as plt
TRIALS=7
SEED = 2026

def list_indexing(data):
    return data[len(data)//2]

def binary_search(data,target):
    lo,hi=0,len(data)-1
    while lo<=hi:
        mid=(lo+hi)//2
        if data[mid]==target: return mid
        elif data[mid]<target: lo=mid+1
        else: hi=mid-1
    return -1

def linear_search(data, target):
    for i in range(len(data)):
        if data[i] == target: return i
    return -1

def merge_sort(data):
    if len(data)<=1: return list(data)
    mid=len(data)//2
    left=merge_sort(data[:mid])
    right=merge_sort(data[mid:])
    res=[]; i=j=0
    while i<len(left) and j<len(right):
        if left[i]<=right[j]:
            res.append(left[i]); i+=1
        else:
            res.append(right[j]); j+=1
    res.extend(left[i:]); res.extend(right[j:])
    return res

def pair_counter(n):
    count=0
    for i in range(n):
        for j in range(n): count+=1
    return count

def subset_masks(n):
    for m in range(1<<n): yield m

def enumerate_subsets(n):
    count=0
    for m in subset_masks(n): count+=1
    return count

def prefix_average1(data):
    avgs=[]
    for j in range(len(data)):
        s=0
        for i in range(j+1): s+=data[i]
        avgs.append(s/(j+1))
    return avgs

def prefix_average2(data):
    avgs=[]; s=0
    for j, value in enumerate(data):
        s+=value; avgs.append(s/(j+1))
    return avgs

def validate():
    cases=[([],[]),([7],[7.0]),([2,4,6],[2.0,3.0,4.0]),([-2,-4,-6],[-2.0,-3.0,-4.0]),([3,-3,9,-1],[3.0,0.0,3.0,2.0]),([0.5,1.5,-2.0],[0.5,1.0,0.0])]
    for data,expected in cases:
        assert prefix_average1(data)==expected
        assert prefix_average2(data)==expected
    for data in ([],[1],[4,-1,4,0],[5,4,3,2,1]):
        assert merge_sort(data)==sorted(data)
        ordered=sorted(data)
        for target in (-10,-1,0,1,4,10):
            for search in (binary_search,linear_search):
                ix=search(ordered,target)
                assert (ix==-1)==(target not in ordered)
                if ix!=-1: assert ordered[ix]==target
    assert list_indexing([10,20,30])==20
    for n in range(8):
        assert pair_counter(n)==n*n
        assert list(subset_masks(n))==list(range(2**n))
        assert enumerate_subsets(n)==2**n
    return "Passed: empty, singleton, positive, negative, mixed and float prefix cases; searches, sorting, indexing, pairs and subsets."

def measure(func,args,batch=1):
    func(*args)
    samples=[]
    for k in range(TRIALS):
        t0=perf_counter()
        for _ in range(batch): func(*args)
        samples.append((perf_counter()-t0)/batch)
    med=sorted(samples)[TRIALS//2]
    return med,samples

def growth_value(name,n):
    if name=='list_indexing': return 1
    if name=='binary_search': return n.bit_length()-1
    if name=='linear_search': return n
    if name=='merge_sort': return n*(n.bit_length()-1)
    if name=='pair_counter': return n*n
    return 2**n

def lab_work1():
    print("\nLAB WORK 1: BENCHMARKING ALGORITHMIC GROWTH RATES")
    print("Task 1: indexing, binary search, linear search, merge sort,")
    print("double-loop pair counting, and subset enumeration are implemented.")
    experiments=[(list_indexing,"Theta(1)",[128,512,2048,8192,32768],10000),
                 (binary_search,"Theta(log n) for misses",[128,512,2048,8192,32768],500),
                 (linear_search,"Theta(n) for misses",[128,512,2048,8192,32768],20),
                 (merge_sort,"Theta(n log n)",[128,256,512,1024,2048,4096],1),
                 (pair_counter,"Theta(n^2)",[50,100,200,400,800],1),
                 (enumerate_subsets,"Theta(2^n), small masks",[8,10,12,14,16,18],1)]
    print("\nTask 2: safe input ranges")
    for func,bound,sizes,batch in experiments:
        print(f"{func.__name__:20} {bound:26} n = {sizes}")
    print("Exponential enumeration stops at n=18 (262144 subsets).")
    print("Quadratic work stops at n=800; larger sizes are safe for faster algorithms.")
    print("\nTask 3: repeated measurements and input characteristics")
    print("Search/index input: sorted distinct integers 0..n-1; target -1 is absent.")
    print(f"Merge-sort input: random integers [-10*n, 10*n], seed={SEED}.")
    print("Pairs: all ordered pairs including self-pairs. Subsets: streamed bit masks.")
    print("Seven trials; median seconds per call. Fast operations use batches.")
    print("Data generation, expected outputs and validation are outside timed sections.")
    rng=random.Random(SEED)
    results=[]
    for func,bound,sizes,batch in experiments:
        times=[]
        print(f"\n{func.__name__} (batch={batch})")
        print("n median seconds    seven trial times (seconds per call)")
        for n in sizes:
            if func in (list_indexing,binary_search,linear_search):
                data=list(range(n))
                args=(data,) if func is list_indexing else (data,-1)
                expected=n//2 if func is list_indexing else -1
            elif func is merge_sort:
                data=[rng.randint(-10*n,10*n) for _ in range(n)]
                args,expected=(data,),sorted(data)
            else:
                args=(n,)
                expected=n*n if func is pair_counter else 2**n
            assert func(*args)==expected
            med,samples=measure(func,args,batch)
            times.append(med)
            trials=", ".join(f"{t:.8g}" for t in samples)
            print(f"{n:<7} {med:<17.8g} {trials}")
        results.append((func.__name__,bound,sizes,times))
    print("\nTask 4: Matplotlib time and normalized-growth plots")
    fig,axes=plt.subplots(2,3,figsize=(15,8),constrained_layout=True)
    norm_fig,norm_axes=plt.subplots(6,3,figsize=(15,22),constrained_layout=True)
    for index,(name,bound,sizes,times) in enumerate(results):
        ax=axes.flat[index]
        model=[times[0]*growth_value(name,n)/growth_value(name,sizes[0]) for n in sizes]
        ax.plot(sizes,times,"o-",label="Measured median")
        ax.plot(sizes,model,"--",label="Scaled growth model")
        ax.set(title=name,xlabel="Input size n",ylabel="Seconds per call")
        ax.grid(True,alpha=0.3)
        ax.legend(fontsize=8)
        per_n=[t/n for n,t in zip(sizes,times)]
        per_n_squared=[t/(n*n) for n,t in zip(sizes,times)]
        per_n_log_n=[t/(n*log2(n)) for n,t in zip(sizes,times)]
        print(f"\n{name}: Task 4 normalized timing table")
        print("n       T(n)/n          T(n)/n^2        T(n)/(n log2 n)")
        for n,a,b,c in zip(sizes,per_n,per_n_squared,per_n_log_n):
            print(f"{n:<7} {a:<15.6g} {b:<15.6g} {c:.6g}")
        for column,(label,values) in enumerate([("T(n)/n",per_n),("T(n)/n^2",per_n_squared),("T(n)/(n log2 n)",per_n_log_n)]):
            ax=norm_axes[index,column]
            ax.plot(sizes,values,"o-")
            ax.set(title=f"{name}: {label}",xlabel="Input size n",ylabel="Normalized seconds")
            ax.grid(True,alpha=0.3)
    fig.suptitle("Lab 1 Task 4: execution time versus input size")
    norm_fig.suptitle("Lab 1 Task 4: T(n)/n, T(n)/n^2 and T(n)/(n log2 n)")
    fig.savefig("lab1_execution_times.png",dpi=160)
    norm_fig.savefig("lab1_normalized_times.png",dpi=160)
    plt.close(fig)
    plt.close(norm_fig)
    print("Saved lab1_execution_times.png and lab1_normalized_times.png.")
    print("A roughly flat T(n)/n supports linear growth; flat T(n)/n^2 supports")
    print("quadratic growth; flat T(n)/(n log2 n) supports n log n growth.")
    print("These are finite-range comparisons and do not prove asymptotic bounds.")

def lab_work2():
    print("\nLAB WORK 2: PREFIX AVERAGES")
    print("Tasks 1-2: prefix_average1 uses nested loops; prefix_average2 uses a running sum.")
    print("Task 3: validation covers empty, singleton, positive, negative, mixed and float inputs.")
    print("Empty input returns [] in both implementations.")
    print("\nTask 4: seven repeated trials for identical reproducible inputs")
    print(f"Random integer sequences in [-100, 100], seed={SEED+1}.")
    rng=random.Random(SEED+1)
    sizes=[1,10,100,200,400,800,1600,3200]
    quadratic,linear,clearly_faster=[],[],[]
    print("n       nested seconds    running seconds   speedup   T1/n^2       T2/n")
    for index,n in enumerate(sizes):
        data=[rng.randint(-100,100) for _ in range(n)]
        assert prefix_average1(data)==prefix_average2(data)
        functions=[prefix_average1,prefix_average2]
        if index%2: functions.reverse()
        timings={}; samples={}
        for func in functions:
            batch=100 if n<=10 else (10 if func is prefix_average2 else 1)
            timings[func],samples[func]=measure(func,(data,),batch)
        t1,t2=timings[prefix_average1],timings[prefix_average2]
        quadratic.append(t1); linear.append(t2)
        if max(samples[prefix_average2])<min(samples[prefix_average1]): clearly_faster.append(n)
        print(f"{n:<7} {t1:<17.8g} {t2:<17.8g} {t1/t2:<9.2f} {t1/n**2:<12.5g} {t2/n:.5g}")
        for func in (prefix_average1,prefix_average2):
            print(f"  {func.__name__} trials: {samples[func]}")
    fig,axes=plt.subplots(1,3,figsize=(16,5),constrained_layout=True)
    axes[0].plot(sizes,quadratic,"o-",label="prefix_average1")
    axes[0].plot(sizes,linear,"o-",label="prefix_average2")
    axes[0].set_title("Both implementations")
    for ax,times,power,title in [(axes[1],quadratic,2,"Quadratic: O(n^2)"),(axes[2],linear,1,"Linear: O(n)")]:
        ax.plot(sizes,times,"o-",label="Measured median")
        ax.plot(sizes,[times[-1]*(n/sizes[-1])**power for n in sizes],"--",label="Scaled model")
        ax.set_title(title)
    for ax in axes:
        ax.set_xlabel("Sequence length n")
        ax.set_ylabel("Seconds per call")
        ax.grid(True,alpha=0.3)
        ax.legend()
    fig.suptitle("Lab 2 Task 5: quadratic versus linear prefix averages")
    fig.savefig("lab2_prefix_averages.png",dpi=160)
    plt.close(fig)
    print("\nTask 5: saved lab2_prefix_averages.png.")

def main():
    lab_work1()
    lab_work2()
    print("\nSaved three Matplotlib PNG figures.")

if __name__=="__main__":
    main()
