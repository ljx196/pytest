import datetime
import json
import os
import random


class dataprocess():

    def __init__(self, path='', save_path=''):
        """
        初始化的方法，指定数据存储的路劲以及数据处理之后存储的路劲
        :param path: str 数据存储的路劲
        :param save_path: str 数据处理之后存储的路劲
        """
        self.path = path
        self.save_path = save_path

    def load_data(self, path='', encoding_='utf-8'):
        """
        加载数据进类文件中，可以在调用这个方法中指定方法路径
        :param encoding_: str 指定数据读取的格式
        :param path: str 指定数据的文件
        :return:
        """
        if path is not '':
            self.path = path
        else:
            if self.path is '':
                raise Exception('Please specific work direction ! ')

        print('从路径 {} 开始读取数据'.format(self.path))
        self.file = open(self.path, 'r', encoding=encoding_)
        self.data_lines = self.file.readlines()
        self.file.seek(0)
        self.data = self.file.read()

    def pre_process(self):
        """
        对处理之前的数据进行处理，例如将从文件夹读取出来的数据再次进行处理
        :return:
        """
        pass

    def process(self):
        """
        对数据进行主要的处理
        :return:
        """
        pass

    def after_process(self):
        """
        对数据处理之后的处理，这里可以加入一些对输出数据的处理
        :return:
        """
        pass

    def save_data(self, save_path='', encoding_='utf-8', mod='w+'):
        """
        对数据进行最终的处理，这里可以特定存储的路径，如果没有指定，那么将会在数据数据目录下创建一个以当前时间命名的文件
        :param encoding_: str 指定数据输出的格式
        :param save_path: str 文件输出的目录
        :return:
        """
        if save_path is '':
            if self.save_path is '':
                self.set_default_work_dir()
        else:
            self.save_path = save_path

        print('将数据存储至 {}'.format(self.save_path))

        self.save_file = open(self.save_path, mod, encoding=encoding_)
        if isinstance(self.save_data_, list):
            self.save_file.writelines(self.save_data_)
        else:
            self.save_file.write(self.save_data_)

    def set_default_work_dir(self):
        """
        返回当前工作路径，以输入路径为准
        :return:
        """
        self.save_path = '{}\\{}{}'.format(os.path.dirname(self.path), self.get_time(), self.get_suffix(self.path))

    def get_suffix(self, path):
        """
        接受输入数据路径参数，返回数据数据的文件后缀
        :param path: str 输入数据路径
        :return:
        """
        if path.__contains__('.'):
            return '.' + path.split('.')[1]
        return ''

    def get_time(self):
        """
        获取当前时间，年月日小时分秒
        :return: str 当前时间
        """
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def execute(self, path='', save_path=''):
        """
        执行所有的方法
        :param path:
        :param save_path:
        :return:
        """
        self.load_data(path)
        self.pre_process()
        self.process()
        self.after_process()
        self.save_data(save_path)


class treedataprocess(dataprocess):
    """
    将将eqnet数据集序列化，并生成训练数据
    """

    def combine(self, ori, noi):
        tmp = []
        for noii in noi:
            tmp.append(ori + '\t' + noii + '\t1')

        return tmp

    def combine_neg(self, data):
        tmp_ = []
        cnt = 0

        for data_ in data:
            cnt += len(data_) - 1

        for _ in range(cnt):
            tmp = random.choices(data, k=2)
            tmp_.append('{}\t{}\t0'.format(random.choice(tmp[0]), random.choice(tmp[1])))

        return tmp_

    def process(self):
        self.save_data_ = []
        tmp_data = []
        json_obj = json.loads(self.data)
        for ori in json_obj:
            noises = []
            origin = json_obj[ori]['Original']['Tokens']
            noise = json_obj[ori]['Noise']
            for Noise in noise:
                noises.append(' '.join(Noise['Tokens']))


            self.save_data_.extend(self.combine(' '.join(origin), noises))
            noises.append(' '.join(origin))
            tmp_data.append(noises)

        self.save_data_.extend(self.combine_neg(tmp_data))

    def execute(self, path='', save_path=''):
        """
        执行所有的方法
        :param path:
        :param save_path:
        :return:
        """
        self.load_data(path)
        self.pre_process()
        self.process()
        self.after_process()
        self.save_data(save_path=r'C:\work\ExpData\poly8data.json', mod='a+')

    def after_process(self):
        for idx, data in enumerate(self.save_data_):
            self.save_data_[idx] = self.save_data_[idx] + '\n'

        random.shuffle(self.save_data_)

if __name__ == '__main__':
    dataprocess = treedataprocess('C:\work\eqnet-master\expressions-synthetic\poly8\poly8-testset.json')
    dataprocess.execute()