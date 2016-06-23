from argparse import ArgumentParser
from multiprocessing import Process, Queue
from math import factorial
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

def split_sections(members, threads):
   section_length = members / threads
   sections = []
   for i in range(threads):
       sections.append(range(i*section_length,(i+1)*section_length))

   sections[-1].extend(range(sections[-1][-1], members))
   return sections

def calculator(section, thread, res, quiet_mode):
    member_res = 0
    if not quiet_mode:
        print "Thread {0} is running".format(thread + 1)
    for i in section:
        member_res += DEC_1/Decimal(factorial(i))
    res.put(member_res)

def main():
    res = Queue()
    sections = split_sections(members, threads)

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
    msg = "Threads: %s\nMembers: %s\nTime: %s\nNeper number: %s\n" % (threads,
            members, unicode(str(final_time), "utf-8"), neper_number)

    if not quiet_mode:
        print(msg)
    if filename:
        with open(filename, 'a') as f:
            delimeter = "="*80
            f.write(delimeter + "\n" + msg)

if __name__ == '__main__':
    main()
