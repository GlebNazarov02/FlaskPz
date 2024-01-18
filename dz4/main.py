import requests
import os
import time
import multiprocessing
import threading
import asyncio

# Функция для скачивания изображения с заданного URL и сохранения на диск
def download_image(url, path):
    response = requests.get(url)
    with open(path, 'wb') as f:
        f.write(response.content)

# Функция для многопоточного подхода
def multithreaded_approach(url_list):
    start_time = time.time()
    os.makedirs('images', exist_ok=True)
    
    threads = []
    for url in url_list:
        filename = url.split('/')[-1]
        path = os.path.join('images', filename)
        thread = threading.Thread(target=download_image, args=(url, path))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time taken: {total_time} seconds-multithread")

# Функция для многопроцессорного подхода
def multiprocess_approach(url_list):
    start_time = time.time()
    os.makedirs('images', exist_ok=True)
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    for url in url_list:
        filename = url.split('/')[-1]
        path = os.path.join('images', filename)
        pool.apply_async(download_image, (url, path))
    pool.close()
    pool.join()
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time taken: {total_time} seconds-multiprocess")

# Функция для асинхронного подхода
async def download_and_save_image(url, path):
    response = await asyncio.get_event_loop().run_in_executor(None, requests.get, url)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)

async def async_approach(url_list):
    start_time = time.time()
    os.makedirs('images', exist_ok=True)
    tasks = []
    for url in url_list:
        filename = url.split('/')[-1]
        path = os.path.join('images', filename)
        task = asyncio.ensure_future(download_and_save_image(url, path))
        tasks.append(task)
    await asyncio.gather(*tasks)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time taken: {total_time} seconds-async")

# Функция для командной строки
def main():
    import sys
    
    url_list = sys.argv[1:]
    # url_list = ['https://w.forfun.com/fetch/5d/5d3aacefdbaad0ae0ad149dfc915613f.jpeg']
    # url_list1 = ['https://w.forfun.com/fetch/83/833a6677031e154a154802ee26b8d294.jpeg']
    # url_list2 = ['https://static16.tgcnt.ru/posts/_0/ed/ed1bc8b51cc22e94efbe2e28b176224a.jpg']
    if not url_list:
        print("Please provide a list of URLs.")
        return
    
    multithreaded_approach(url_list)
    # multiprocess_approach(url_list1)
    # asyncio.run(async_approach(url_list2))
    multiprocess_approach(url_list)
    asyncio.run(async_approach(url_list))

if __name__ == '__main__':
    main()
