import os
import datetime
import re

# 获取文件夹下所有的以bdir结尾的文件名
def getfilelist(path, bdir):
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(bdir)]

def getallfile(path, bdir):
    files = []
    for p in getfilelist(path, bdir):
        files.append(open(p, 'r', encoding='utf-8'))

    return files

def gettime():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

def getalldatatolines(path, bdir):
    lines = []
    files = getallfile(path, bdir)
    for file in files:
        lines.extend(file.readlines())

    # print(lines)
    return lines

def writetofile(lines, path):
    with open(os.path.join(path, gettime() + '.csv'), 'w+', encoding='utf-8') as file:
        for line in lines:
            if line == '' or line is None:
                continue
            file.write(line)

# 去掉数字，2个字符以下，空
def lineprocess(line):

    linesplit = line.split()

    if len(linesplit) <= 2:
        return ''

    if len(linesplit[0]) <= 2:
        return ''

    if re.match('^[()/0-9.-]+$', linesplit[0]) is not None:
        return ''

    return line

# 去除包含∅的
def lineprocess2(line):

    if line.count('begin') != 0:
        return ''

    return line

# 去掉类别中含指定类别的数据
def lineprocess3(line):

    linesplit = line.split()

    dlabels = ['递归方程']

    for labeli in dlabels:
        if linesplit.count(labeli) != 0:
            return ''

    return line

# 去掉含中文字符的
def lineprocess4(line):

    linesplit = line.split()

    if len(re.findall('[\u4e00-\u9fa5]', linesplit[0])) != 0:
        return ''

    return line

# 返回所有的标签
def lineprocess5(line):

    linesplit = line.split()

    rset = set()

    for i in range(len(linesplit)):
        if re.match('^[\u4e00-\u9fa5]+$', linesplit[i]) is None:
            continue

        rset.add(linesplit[i])

    return rset

# 去掉包含字符x的行
def lineprocess6(line):

    if line.count('\''):
        return ''


    return line

# 去掉包含A={1, 2, 3}等形式的数据
def lineprocess7(line):

    if re.match('.*={.*?}.*', line) is not None:
        return ''

    return line

# 去掉数据中没有a-zA-Z等字母的数据，表示这行数据大概率是单字符组成的
def lineprocess8(line):

    if re.match('.*[a-zA-Z]+.*', line) is None:
        return ''

    return line

# 去掉数据中没有+-*/的表达式，包含表达式结果信息过低
def lineprocess9(line):

    if re.match('.*[+\\-*/]+.*', line) is None:
        return ''

    return line

def lineprocess10(line):

    linesplit = line.split()

    for splits in linesplit:
        if re.match('^[a-zA-Z]+=[-/0-9]+$', splits) is None:
            return ''

    return line

def lineprocess11(line):

    rst = []
    linesplit = line.split()
    back = ''
    for splits in linesplit[1:]:
        back += '\t' + splits

    for sl in linesplit[0].split('，'):
        for sll in sl.split(','):
           rst.append(sll + back + '\n')

    return rst




def process(path, opath, bdir):

    lines = getalldatatolines(path, bdir)
    # print(lines)
    olines = []
    # oset = set()

    for line in lines:
        olines.append(lineprocess6(line))
        # olines.extend(lineprocess11(line))
        # oset = oset | lineprocess5(line)

    # print(oset)
    #
    writetofile(olines, opath)

def test1():
    line = 'a^20,03+b^，2004=_,-1	等式	17274777\n'
    print(lineprocess11(line))

if __name__ == '__main__':
    # 数据文件夹path，读取所有以bdir结尾的文件，并且输出到opath中输出文件名为系统当前时间+.csv
    path = 'C:\WorkSpace\ExpData\ExpDatav2'
    bdir = '20201124102521.csv'
    opath = 'C:\WorkSpace\ExpData\ExpDatav2'
    process(path, opath, bdir)
    # test1()
    # print(lineprocess6(r'a^2003+b^2004=_,-1	等式	17274777'))

