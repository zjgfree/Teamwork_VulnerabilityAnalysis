import time
from .rectify_func import *


def rectify():
    start = time.perf_counter()
    print("Rectifying proj dict...")
    rectify_out1()
    print(f"Done, used {time.perf_counter() - start:<.2f}s\n")

    start = time.perf_counter()
    print("Rectifying attr dict...")
    rectify_out2()
    print(f"Done, used {time.perf_counter() - start:<.2f}s\n")

    start = time.perf_counter()
    print("Rectifying graph dict...")
    rectify_out3()
    print(f"Done, used {time.perf_counter() - start:<.2f}s\n")

    start = time.perf_counter()
    print("Rectifying call dict...")
    rectify_out4()
    print(f"Done, used {time.perf_counter() - start:<.2f}s\n")

    start = time.perf_counter()
    print("Rectifying ref dict...")
    rectify_out5()
    print(f"Done, used {time.perf_counter() - start:<.2f}s\n")
