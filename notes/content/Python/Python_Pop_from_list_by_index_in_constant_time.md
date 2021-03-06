## Python, Popping by index in constant time

Normally, popping a given index from a list is done in linear time, since everything from that index to list-end has to be moved. 

But here is a way to do it in constant time (thanks to Leslie Klein): swap the index in question with the list-end, and then use `pop()`. Popping from the end of the list is done in constant time.

(Of course, the list is no longer in the same order after this operation.)

Here are timings (Python 3). A factor-of-ten increase in the size of the list increases running time ten-fold with this method, meaning constant time; the alternative (`pop(index)`) appears to cost linear time.

~~~
def main(upper_bound=100, trials=10):
    import random, time
    #
    # Pop index directly.
    start_time = time.time()
    for trial in range(trials):
        random.seed(trial*137)
        the_list = [random.random() for i in range(upper_bound)]
        for i in range(upper_bound):
            the_list.pop(random.randint(0, len(the_list) - 1))
    print('With direct removal of index, average: {:.4f} seconds / loop'.
            format((time.time() - start_time) / trials))
    #
    # First swap index with end, then pop end.
    start_time = time.time()
    for trial in range(trials):
        random.seed(trial*137)
        the_list = [random.random() for i in range(upper_bound)]
        for i in range(upper_bound):
            last = len(the_list) - 1
            chosen = random.randint(0, last)
            the_list[chosen], the_list[last] = the_list[last], the_list[chosen]
            the_list.pop()
    print('With swapping index to end then pop, average: {:.4f} seconds / loop'.
            format((time.time() - start_time) / trials))

In [2]: main()
With direct removal of index, average: 0.0004 seconds / loop
With swapping index to end then pop, average: 0.0003 seconds / loop

In [3]: main(1000, 100)
With direct removal of index, average: 0.0026 / loop
With swapping index to end then pop, average: 0.0026 seconds / loop

In [4]: main(10000, 100)
With direct removal of index, average: 0.0320 / loop
With swapping index to end then pop, average: 0.0266 seconds / loop

In [5]: main(100000, 10)
With direct removal of index, average: 1.0607 / loop
With swapping index to end then pop, average: 0.2685 seconds / loop

In [6]: main(1000000, 1)
With direct removal of index, average: 92.0455 / loop
With swapping index to end then pop, average: 2.9250 seconds / loop
~~~

[end]
