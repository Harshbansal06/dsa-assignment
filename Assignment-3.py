def check_n(n):
    if type(n)!=int or n<0:
        raise ValueError("n must be a non-negative integer")

def factorial(n):
    check_n(n)
    if n==0: return 1
    return n*factorial(n-1)

def natural_sum(n):
    check_n(n)
    if n==0: return 0
    return n+natural_sum(n-1)

def power(x,n):
    check_n(n)
    if n==0: return 1
    return x*power(x,n-1)

def is_sorted(data,index=0):
    if index>=len(data)-1: return True
    if data[index]>data[index+1]: return False
    return is_sorted(data,index+1)

class Stack:
    def __init__(self):
        self.data=[]

    def __len__(self):
        return len(self.data)

    def is_empty(self):
        return len(self.data)==0

    def push(self,element):
        self.data.append(element)

    def pop(self):
        if self.is_empty(): raise IndexError("stack is empty")
        return self.data.pop()

    def top(self):
        if self.is_empty(): raise IndexError("stack is empty")
        return self.data[-1]

class CircularQueue:
    def __init__(self,capacity=5):
        if type(capacity)!=int or capacity<1:
            raise ValueError("capacity must be a positive integer")
        self.data=[None]*capacity
        self.size=0
        self.front=0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size==0

    def enqueue(self,element):
        if self.size==len(self.data): raise OverflowError("queue is full")
        idx=(self.front+self.size)%len(self.data)
        self.data[idx]=element
        self.size+=1

    def first(self):
        if self.is_empty(): raise IndexError("queue is empty")
        return self.data[self.front]

    def dequeue(self):
        element=self.first()
        self.data[self.front]=None
        self.front=(self.front+1)%len(self.data)
        self.size-=1
        return element

    def display(self):
        out=[]
        for i in range(self.size):
            out.append(self.data[(self.front+i)%len(self.data)])
        return out

class CircularDeque(CircularQueue):
    def add_first(self,element):
        if self.size==len(self.data): raise OverflowError("deque is full")
        self.front=(self.front-1)%len(self.data)
        self.data[self.front]=element
        self.size+=1

    def add_last(self,element):
        self.enqueue(element)

    def delete_first(self):
        return self.dequeue()

    def delete_last(self):
        if self.is_empty(): raise IndexError("deque is empty")
        idx=(self.front+self.size-1)%len(self.data)
        element=self.data[idx]
        self.data[idx]=None
        self.size-=1
        return element

def main():
    print("PART A, Q2: RECURSIVE FUNCTIONS")
    print("Preconditions: n is an integer >= 0; x is numeric for power.")
    print("Base cases: factorial(0)=1, sum(0)=0, power(x,0)=1.")
    print("factorial(5) =",factorial(5))
    print("natural_sum(10) =",natural_sum(10))
    print("power(2, 10) =",power(2,10))

    print("\nPART A, Q4: NON-DECREASING ORDER")
    for data in ([],[5],[1,1,3],[1,3,2]):
        print(data,"->",is_sorted(data))

    print("\nPART C, Q2: STACK")
    st=Stack()
    st.push(10); st.push(20)
    print("After push 10, push 20: top =",st.top(),"length =",len(st))
    print("Pop:",st.pop(),"then",st.pop(),"empty:",st.is_empty())

    print("\nPART C, Q8: CIRCULAR QUEUE")
    print("Insertion index = (front + size) % len(data).")
    print("After dequeue: front = (front + 1) % len(data).")
    q=CircularQueue(3)
    for e in (10,20,30): q.enqueue(e)
    print("Full queue:",q.display(),"storage:",q.data)
    print("Dequeue:",q.dequeue())
    q.enqueue(40)
    print("Wrapped queue:",q.display(),"storage:",q.data,"front:",q.front,"size:",q.size)

    print("\nPART C, Q10: CIRCULAR DEQUE")
    print("add_first: front=(front-1)%capacity; store; size+=1.")
    print("add_last: store at (front+size)%capacity; size+=1.")
    print("delete_first: clear front; front=(front+1)%capacity; size-=1.")
    print("delete_last: clear (front+size-1)%capacity; size-=1.")
    dq=CircularDeque(4)
    dq.add_last(20); dq.add_first(10); dq.add_last(30)
    print("After additions:",dq.display())
    print("delete_first:",dq.delete_first())
    print("delete_last:",dq.delete_last())
    print("Remaining:",dq.display())

if __name__=="__main__":
    main()
