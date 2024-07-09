import time
import os
from random import randint
from threading import Thread
from fastapi import FastAPI, HTTPException
import asyncio
from concurrent.futures import ThreadPoolExecutor

# ایجاد یک اپلیکیشن FastAPI
app = FastAPI()
executor = ThreadPoolExecutor()

# تعریف کلاس برای رشته‌ها
class MyThreadClass(Thread):
    def __init__(self, name, duration):
        Thread.__init__(self)
        self.name = name
        self.duration = duration
        self.result = None

    def run(self):
        pid = os.getpid()
        start_time = time.time()
        print(f"---> {self.name} running, belonging to process ID {pid}\n")
        time.sleep(self.duration)
        end_time = time.time()
        self.result = {
            "name": self.name,
            "pid": pid,
            "duration": self.duration,
            "start_time": start_time,
            "end_time": end_time
        }
        print(f"---> {self.name} over\n")

def run_threads(num_threads: int):
    start_time = time.time()

    threads = []
    for i in range(1, num_threads + 1):
        thread = MyThreadClass("Thread#" + str(i), randint(5, 10))
        threads.append(thread)
        thread.start()

    results = []
    for thread in threads:
        thread.join()
        if thread.result:
            results.append(thread.result)

    total_duration = time.time() - start_time
    return {"threads": results, "total_duration": total_duration}

# نقطه پایانی API برای اجرای رشته‌ها
@app.get("/run-threads/{num_threads}")
async def run_threads_endpoint(num_threads: int):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, run_threads, num_threads)
    return result

# اجرای اپلیکیشن
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
