import multiprocessing
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm.contrib.concurrent import process_map

from schema import *

m = multiprocessing.Manager()
lock = m.Lock()


def chunk_list(lst, chunk_size):
    """将列表分块为指定大小的子列表"""
    chunked_list = []
    for i in range(0, len(lst), chunk_size):
        chunk = lst[i:i + chunk_size]
        chunked_list.append(chunk)
    return chunked_list


def process_data(data):
    def filter_data(l):
        if not l:
            return None
        if l.isdecimal():
            if l[0] == '0':
                return l
            return eval(l)
        return l

    for x in range(len(data)):
        data[x] = list(map(filter_data, data[x].split(',')))
        # if len(data[x]) > 10:
        #     idx = 3 if data[x][3] < data[x][4] else 4
        #     data[x].pop(idx)

    obj = [HostMeta(i) for i in data]
    session.add_all(obj)
    with lock:
        session.commit()


def get_data(file_name):
    cnt = 0
    # read the first 1e6 rows
    lines = []
    with open(file_name, 'r') as f:
        # f.readline()

        lines = [i.strip() for i in
                 f.readlines()]

        # while cnt < 5e4:
        #     line = f.readline().strip()
        #     if not line:
        #         break
        #     lines.append(line)
        #     cnt += 1

    # split the lines into chunks
    chunked_lines = chunk_list(lines, int(25e2))

    process_map(process_data, chunked_lines, max_workers=20, chunksize=8)


def get_csv():
    folder_name = pathlib.Path('cluster-trace-microarchitecture-v2022')
    file_list = pathlib.Path(folder_name).glob('host_meta-0.csv')

    for file_name in file_list:
        get_data(file_name)


if __name__ == '__main__':
    # mariadb
    engine = create_engine("mysql+pymysql://root:123456@localhost:3306/alibaba", echo=False, pool_size=50,
                           max_overflow=0)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # get_data()
    get_csv()
