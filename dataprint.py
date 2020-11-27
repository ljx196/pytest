import os

def getleft(arg):
    rst = []
    rst.append(arg.split(' ')[0])
    rst.extend(arg.split(' ')[1].split('-'))
    return rst


def printoans(file, sidx, eidx, str, numbers, label):
    ans = 'T{}\t{} {} {}\t{}'.format(numbers+1, label, sidx, eidx, str)
    print(ans)
    file.write(ans + '\n')


def handleData():
    global str
    rfile = open(r'C:\WorkSpace\output\output1.txt', 'r', encoding='utf-8')
    nfile = open(r'C:\WorkSpace\output\nums.txt', 'r', encoding='utf-8')
    dfilelist = os.listdir(r'C:\WorkSpace\output\test')
    words = rfile.readlines()
    nlines = nfile.readlines()
    oidx = 0
    fidx = 0
    for nidx in dfilelist:

        filePath = "C:\WorkSpace\output\\test\\"
        dfile = open(filePath + dfilelist[fidx], 'r', encoding='utf-8')
        ftmp = str(1000+fidx)
        filed = open(filePath + ftmp + '.ann', 'w+', encoding='utf-8')
        fidx = fidx + 1
        dtext = dfile.readlines()[0]
        flag = False
        sidx = 0
        strs = ''
        numbers = 0
        label = ''
        for didx in range(len(dtext)):

            if oidx >= len(words):
                break

            while words[oidx] == '\n':
                oidx = oidx + 1

            if dtext[didx] == getleft(words[oidx])[0]:

                if getleft(words[oidx])[1].strip('\n') == 'O':
                    if flag:
                        printoans(filed, sidx, didx, strs, numbers, label)
                        strs = ''
                        numbers = numbers + 1
                        flag = False
                    else:
                        pass
                elif getleft(words[oidx])[1] == 'B':
                    if flag:
                        # 单字实体不存在
                        printoans(filed, sidx, didx, strs, numbers, label)
                        label = getleft(words[oidx])[2].strip('\n')
                        strs = getleft(words[oidx])[0]
                        sidx = didx
                        numbers = numbers + 1
                    else:
                        strs = getleft(words[oidx])[0]
                        label = getleft(words[oidx])[2].strip('\n')
                        sidx = didx
                        flag = True
                elif getleft(words[oidx])[1] == 'I':
                    if flag:
                        strs = strs + getleft(words[oidx])[0]
                    else:
                        pass

                oidx = oidx + 1


if __name__ == '__main__':
    handleData()
    # filePath = "C:\WorkSpace\output\\test\\"
