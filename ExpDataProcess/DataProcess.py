import os
import time
import datetime
import re
import random
from ExpDataProcess.ExpRepr import ExpRepr
import func_timeout


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

    # dlabels = ['','表','∨','轨','⨁','ŷ','程','２','','分','','∝','','υ','↓','数',
    #            '１','﹡','直','最','７','','★','＇','₂','﹑','⋯','⊗','解','垂','≡','不',
    #            'Ⅱ','ｂ','和','等','~','.','公','％','值','般','','←','平','﹐','≪','♁',
    #            '｛', '⊊', '﹛', '∠','⌈','方','曲','☆','↘','∩','⊕','⊂','⌒','项','￢','ʹ',
    #            'ⅲ','｝','﹢','∃','ع', '→','∼','≠','前','┉','〔','ε','ⅱ','⊇','⊃','Ω','\'',
    #            '″','∶','∀','Г','３','⟹','０','双','⋮','ϖ','∫','※','一','⌉','⊄','`','ξ',
    #            '','迹','⑷','通','ζ','∓','⟩','','⇔','℃','﹙','τ','＠','Ⅲ','﹒','ϑ','〈',
    #            'ϵ','⇏',',','，','小','组','ψ','ⅳ','列','↗','︰','','﹚','▽','●','⫋','ɛ',
    #            'η','√','︱','▪','～','≦','达','〉','﹜','⟺','≈','〕','¬','','ˈ','析','差',
    #            '线','@','₁','》','∣','∗','︳','｜','Ⅰ ','═','≧','⩾','６','ｔ','﹤','﹡','《',
    #            '','⟨','Ⅰ','—','∂','I','○','↑','㏑','⋂','ⅰ','⌋','J','・','%','γ','∑','Γ',
    #            '°','','&','Β','⨂','４','H','Z','','','ϕ','┐','♧','∧','⫌','Χ','̂','ƒ',
    #            'δ','μ','σ','ν','j','U','Y','Α','〉','⌊']
    dlabels = ['','L','>']

    for labeli in dlabels:
        if linesplit[0].count(labeli):
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
    if line.count(':'):
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


# 如果只含2个及一下的字符就默认丢弃
def lineprocess12(line):
    linesplit = line.split()

    if len(linesplit[0]) < 3:
        return ''

    return line


@func_timeout.func_set_timeout(0.02)
def lineprocess13(line):
    linesplit = line.split()

    exp_obj = ExpRepr(linesplit[0]).rpar_obj()

    linesplit[0] = exp_obj.good_form()

    return '\t'.join(linesplit) + '\n'

def lineprocess14(line):
    linespt = line.split()

    bracket = 0
    for idx, symb in enumerate(linespt[0]):
        if symb == '(':
            if idx + 1 < len(linespt[0]) and linespt[0][idx+1] == ')':
                raise Exception
            bracket += 1
        if symb == ')':
            bracket -= 1
        if bracket < 0:
            raise Exception

    return line

def lineprocess15(line):
    s = ['[', ']']
    t = ['(', ')']
    for i in range(len(s)):
        line = line.replace(s[i], t[i])
    return line

def lineprocess16(line):
    linespt = line.split()

    back = ''

    for spt in linespt[1:]:
        back += '\t' + spt

    back += '\n'

    if linespt[0].count(':'):
        return linespt[0].split(':')[1] + back

    return line

def lineprocess17(line):
    if line.count('|') % 2:
        line = ''

    return line

def lineprocess18(line):
    if line.count('|'):
        spt = line.split()
        tspt = '#' + spt[0] + '#'
        sspt = tspt.split('|')
        rst = ''
        for idx in range(len(sspt)-1):
            if idx % 2 == 0:
                rst += sspt[idx] + 'abs(' + sspt[idx+1] + ')'

        rst += sspt[len(sspt)-1]
        return rst[1:-1]

    return line

@func_timeout.func_set_timeout(0.025)
def lineprocess20(line):
    spt = line.split()
    origin = spt[0]

    origin_exp = ExpRepr(origin).rpar_obj()
    origin = origin_exp.good_form()
    cnt = random.randint(1, 5)
    change_list = origin_exp.datagen(cnt)
    rst = [origin + '\t' + exp_ +'\n' for exp_ in change_list]

    return rst

def lineprocess21(lines):
    tot = len(lines)

    olines = []

    for idx, line in enumerate(lines):
        if idx % 200 == 0:
            print(idx)
        rnd = random.randint(0, 5)
        spt = line.split()

        if random.randint(0, 10) > 8:
            exp = line.split()[random.randint(0, 1)]
            exp_obj = ExpRepr(exp).rpar_obj()
            while True:
                fake_exp = exp_obj.fake_tree()
                if fake_exp != exp:
                    break
            olines.append(exp + '\t' + fake_exp + '\n')
        for _ in range(rnd):
            slct = random.randint(0, 1)
            slctline = random.randint(0, tot-1)
            cnt = spt[slct] + '\t' + lines[slctline].split()[slct] + '\n'
            olines.append(cnt)
            if idx < 5:
                print(cnt)

    return olines

@func_timeout.func_set_timeout(0.1)
def lineprocess21(line):
    spt = line.split()

    exp1 = ExpRepr(spt[0])
    exp2 = ExpRepr(spt[1])

    exp1.rpar_obj()
    exp2.rpar_obj()

    spt[0] = exp1.get_train_form()
    spt[1] = exp2.get_train_form()

    return '\t'.join(spt) + '\n'

def lineprocess22(line):
    spt = line.split('\t')

    print(spt)




def process(path, opath, bdir):
    lines = getalldatatolines(path, bdir)

    olines = []


    # olines = lineprocess21(lines)

    err = 0
    cnt = 0
    with open('C:\work\ExpData\exceptdata7.csv', 'w+', encoding='utf-8') as efile:
        for lidx, line in enumerate(lines):
            if lidx % 1000 == 0:
                print(lidx)
            try:
                # olines.extend(lineprocess21(line))
                olines.append(lineprocess21(line))
            except:
                print(line)
                print(lidx)
                efile.write(line)
                err += 1
                if err % 1000 == 0:
                    print(err)

        # olines.extend(lineprocess11(line))
        # oset = oset | lineprocess5(line)

    # print(oset)
    #
    writetofile(olines, opath)

def getlinesymbol(line):
    linespt = line.split()

    return [i for i in linespt[0]]

@func_timeout.func_set_timeout(0.01)
def getvariables(line):
    linespt = line.split()

    exp_obj = ExpRepr(linespt[0])

    return exp_obj._vars

def get_all_var(path, opath, bdir):
    lines = getalldatatolines(path, bdir)

    symdict = {}
    err = 0
    cnt = 0
    for line in lines:
        cnt += 1
        # print(cnt)
        try:
            linesylist = getvariables(line)
            add2dict(linesylist, symdict)
        except(BaseException,func_timeout.exceptions.FunctionTimedOut):
            err += 1
            print(err)

    writetofile(dict2list(symdict), opath)

def set2list(sset:set):
    return [s+'\n' for s in sset]


def get_all_symb(path, opath, bdir):
    lines = getalldatatolines(path, bdir)

    symbdict = {}
    for line in lines:

        linesymblist = getlinesymbol(line)
        add2dict(linesymblist, symbdict)

    # for key in symbdict:
    #     if symbdict[key] == 1 or symbdict[key] == 860 or symbdict[key] == 4831:
    #         print(key)
    writetofile(dict2list(symbdict), opath)

def add2dict(llist, sdict:dict):
    for i in llist:
        if sdict.__contains__(i):
            sdict[i] += 1
        else:
            sdict[i] = 1

def dict2list(ddict):
    rst = []

    for key in ddict:
        rst.append(key + ": " + str(ddict[key]) + '\n')

    return rst

def test1():
    line = 'a^20,03+b^，2004=_,-1	等式	17274777\n'
    # print(len(line))
    # print([i for i in line])
    # # print(lineprocess11(line))
    s = set([i for i in line])
    # print(len(s))
    for idx, i in enumerate(s):
        print(i+' ' + str(idx))


def get_var_dict(lines):
    rst = {}

    for line in lines:
        spt = line.split()
        if rst.__contains__(int(spt[1])):
            rst[int(spt[1])] += 1
        else:
            rst[int(spt[1])] = 1

    return rst


def get_var_distri(path, bdir, num):
    lines = getalldatatolines(path, bdir)

    cntdict = get_var_dict(lines)

    cnt = 0
    for key in cntdict:
        if key < num:
            cnt += cntdict[key] * key

    print(cnt)

def filter_lines(lines, vars):
    rst = []
    for idx, line in enumerate(lines):
        flag = 0
        for var in vars:
            if line.count(var):
                flag = 1
                rst.append(line)
                lines[idx] = ''
            if flag == 1:
                break

    return rst

def delete_var_num(path, dpath, opath, bdir, dbdir, num):
    dlines = getalldatatolines(dpath, dbdir)
    lines = getalldatatolines(path, bdir)

    filtelist = []
    for dline in dlines:
        print(dline)
        dspt = dline.split()
        if int(dspt[1]) < num:
            filtelist.append(dspt[0][:-1])

    olines = filter_lines(lines, filtelist)

    writetofile(olines, opath)
    time.sleep(5)
    writetofile(lines, opath)

def linesprocess(lines, nlines):
    for idx in range(len(lines)):
        lines[idx] = lines[idx].strip() + '\t' + '1\n'
        if idx < 5:
            print(lines[idx])
    for idx in range(len(nlines)):
        nlines[idx] = nlines[idx].strip() + '\t' + '0\n'
        if idx < 5:
            print(nlines[idx])
    lines.extend(nlines)
    random.shuffle(lines)
    return lines

def shuffle_data(path, bdir, nbdir, opath):
    lines = getalldatatolines(path, bdir)
    nlines = getalldatatolines(path, nbdir)
    print(lines[0].strip())
    olines = linesprocess(lines, nlines)

    writetofile(olines, opath)


def split_data(path, opath, bdir):
    lines = getalldatatolines(path, bdir)

    lent = len(lines)

    writetofile(lines[:int(lent/100)], opath)
    writetofile(lines[int(lent/100):], opath)

def test_split(path, opath, bdir):
    with open(os.path.join(path, bdir), "r", encoding='utf-8') as lines:
        for line in lines:
            subword = line.strip('\n').split("\t")
            express = subword[0] + " , " + subword[1]
            target = 0
            if subword[2] == "1":
                target = 1
            else:
                target = 0
            print( {
                "inputs": express,
                "targets": target,
            })

def test_accuracy(path, bdir, bdir2):
    lines = getalldatatolines(path, bdir)
    lines2 = getalldatatolines(path, bdir2)

    tot = 0
    rt = 0
    for idx, line in enumerate(lines):
        if line.split('_')[1] == lines2[idx].split('\t')[2]:
            rt += 1
        else:
            print(line + " ### " + lines2[idx])

        tot += 1

    print(rt / tot)



if __name__ == '__main__':
    # 数据文件夹path，读取所有以bdir结尾的文件，并且输出到opath中输出文件名为系统当前时间+.csv
    path = 'C:\WorkSpace\ExpData\ExpDatav2'
    bdir = 'ans.out'
    nbdir = 'express5.csv'
    opath = 'C:\WorkSpace\ExpData\ExpDatav2'
    dpath = 'C:\WorkSpace\ExpData\ExpDatav2'
    dbdir = '20201207142503.csv'
    num = 1000
    # print(lineprocess20('x^2-4x+3≤0'))
    # print('f(x)=((3^(1/2)))(cosx)^2+sinx*cosx+((((3^(1/2)))/2))=((3^(1/2)))*(((1+cos2x)/2))+(1/2)sin2x+((((3^(1/2)))/2))=sin(2x+(((Pi)/3)))+((3^(1/2)))	函数	22083943')
    # print(lineprocess13('(-α<((f(x	_2)-f(x	_1))/(x	_2-x	_1))<α)	不等式	不等式	17274911'))
    # get_all_symb(path, opath, bdir)
    # get_all_var(path, opath, bdir)
    # delete_var_num(path, dpath, opath, bdir, dbdir, num)
    # get_var_distri(path, bdir, num)
    # print(lineprocess15('(log_{3}*(m^2+2)=3)	等式	等式	17275215'))
    # process(path, opath, bdir)
    # test_split(path, opath, bdir)
    test_accuracy(path, bdir, nbdir)
    # split_data(path, opath, bdir)
    # lineprocess22(' f ( a ) = f ( 1 / 2 ) 	 ( 6 / 7 ) ≤ x ≤ 3 	0')
    # shuffle_data(path, bdir, nbdir, opath)
    # datagenerator()
    # print(lineprocess18('|a+c|*((x/(|x|)))+((y/(|y|)))+((z/(|z|)))+(((|xyz|)/(xyz)))/|a+c|'))
    # print(lineprocess16('p:x^2-4x+3≤0'))
    # print('asd2fff'.replace('asd', 'c'))
    # print(lineprocess14('m=-(1/2)	等式	17274702'))
    # test1()
    # test1()
    # print(lineprocess6(r'a^2003+b^2004=_,-1	等式	17274777'))
