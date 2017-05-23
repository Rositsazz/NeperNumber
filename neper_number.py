from argparse import ArgumentParser
from multiprocessing import Process, Queue
from math import factorial, ceil
from decimal import Decimal, getcontext
from timeit import default_timer

parser = ArgumentParser(description="Calculate Neper number")
parser.add_argument("-p", "--precision", type=int,
                    help="Number of members", required=True)
parser.add_argument("-t", "--threads", type=int,
                    help="Number of threads", required=True)
parser.add_argument("-o", "--output", type=str, default="result.txt",
                    help="output file name")
parser.add_argument("-q", "--quiet", action="store_true",
                    help="quiet mode")

arguments = parser.parse_args()
members = arguments.precision
getcontext().prec = members + 1
threads = arguments.threads
quiet_mode = arguments.quiet
filename = arguments.output
DEC_1 = Decimal(1)


def split_sections_equaly(members, threads):
    ns = ceil(members / threads)
    return [list(range(j, members, ns)) for j in range(ns)]


def calculator(section, thread, res, quiet_mode):
    member_res = 0
    if not quiet_mode:
        print("Thread {0} is running".format(thread + 1))
    for i in section:
        member_res += float(DEC_1 / Decimal(factorial(i)))
    res.put(member_res)


def main():
    res = Queue()
    sections = split_sections_equaly(members, threads)

    start_time = default_timer()
    processes = []
    for t in range(threads):
        p = Process(target=calculator,
                    args=(sections[t],
                          t, res, quiet_mode))
        processes.append(p)
        p.start()

    neper_number = sum([res.get() for thread in range(0, threads)])
    for p in processes:
        p.join()

    final_time = default_timer() - start_time
    msg = "Threads: {}\nMembers: {}\nTime: {}\nNeper number: {}\n".format(threads,
                                                                          members, str(final_time), neper_number)

    if not quiet_mode:
        print(msg)
    if filename:
        with open(filename, 'a') as f:
            f.write("=" * 80 + "\n" + msg)


if __name__ == '__main__':
    main()
