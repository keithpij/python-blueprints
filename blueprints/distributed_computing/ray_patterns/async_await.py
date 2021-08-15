import asyncio
import os
import threading
import time


async def long_calculation():
    print('Process ID:  {}'.format(os.getpid()))
    print('Thread ID:  {}'.format(threading.get_ident()))
    time.sleep(5)
    print('Long calculation complete')


async def call_long_calcualtion():
    print('Process ID:  {}'.format(os.getpid()))
    print('Thread ID:  {}'.format(threading.get_ident()))
    await long_calculation()
    print('Long call complete.')


if __name__ == '__main__':
    print('Process ID:  {}'.format(os.getpid()))
    print('Thread ID:  {}'.format(threading.get_ident()))
    asyncio.run(call_long_calcualtion())
