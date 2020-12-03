import time

class ExpRepr(object):

    operatorList = [
        ['=', '>=', '<=', '>', '<', '≤', '≥', '≠'],
        ['+', '-'],
        ['*', '/'],
        ['^'],
        ['_']
    ]

    bracket = ['(', '{', '[']

    left_bracket = [')', '}', ']']

    operLevels = ['relation', 'priOperator', 'operator', 'uporientation', 'downorientation']

    pattern = ['sin(e?x?p)', 'cos(e?x?p)', 'tan(e?x?p)', '(e?x?p)', '[e?x?p]', '{e?x?p}', 'special', 'e?x?p']

    def __init__(self, exp, op='', pat=''):
        self.exp = exp
        if op == '' and pat == '':
            op, pat = self._pre_process(exp)
        self.childrens = []
        self.operLevel = ''
        if self._is_leaf() is not True:
            self._parse_exp()

        self._op = op
        self._pat = pat

    def _pre_process(self, exp):
        idx_ = [0]
        op_r = self._get_op(idx_, sum(self.operatorList, []))
        exp_, pat_ = self._get_exp_pat_(idx_)
        if idx_[0] >= len(exp):
            if pat_ == '':
                self.exp = exp
                return
            self.exp = exp_
            return op_r, pat_
        else:
            return '#', 'e?x?p'

    def _is_leaf(self):
        idx_ = [0]
        min_idx_ = self._get_next_op_idx(idx_)

        if min_idx_ == -1:
            return True

        return False

    def _leaf_construct(self):
        idx_ = [0]
        op_ = self._get_op(idx_, sum(self.operatorList,[]))
        exp_, pat_ = self._get_exp_pat_(idx_)

        self.exp = exp_
        self._pat = pat_
        self._op = '#'

    def _parse_exp(self):
        for index, oList in enumerate(self.operatorList):
            if self.__parse_exp_op(oList) is True:
                self.operLevel = self.operLevels[index]
                return

    # 定义了各种状态：
    # start 开始匹配的状态，只有开始时是
    def __parse_exp_op(self, oList):
        state = 'start'
        idx = [0]
        op_ = ''
        exp_ = ''
        while idx[0] < len(self.exp):
            op_ = self._get_op(idx, oList)
            exp_, pat_ = self._get_exp_pat(idx, oList)
            if state == 'start':
                if op_ == '':
                    op_ = '#'
                next_op_ = self._get_op(idx, oList)
                idx[0] -= len(next_op_)
                if next_op_ == '' and op_ == '#':
                    if not (self.operatorList.index(oList) == 1 and pat_ != 'e?x?p'):
                        return False
                state = 'normal'

            self._new_exp(op_, exp_, pat_)

        return True

    def _get_op(self, idx, oList):
        for op_ in oList:
            if self.exp.find(op_, idx[0]) == idx[0]:
                idx[0] += len(op_)
                return op_

        return ''

    def _get_exp_pat(self, idx, oList):
        r_exp_ = ''
        mod_ = 'start'
        while True:
            exp_, pat_ = self._get_exp_pat_(idx)
            op_ = self._get_op(idx, sum(self.operatorList, []))

            if exp_ == '':
                pass
            elif oList.count(op_) > 0 or op_ == '':
                idx[0] -= len(op_)
                if mod_ == 'start':
                    r_exp_ = exp_
                    r_pat_ = pat_
                else:
                    r_exp_ += pat_.replace('e?x?p', exp_)
                    r_pat_ = 'e?x?p'
                return r_exp_, r_pat_

            mod_ = 'normal'
            r_exp_ += pat_.replace('e?x?p', exp_)
            r_exp_ += op_

    def _new_exp(self, op, exp, pat):
        exp_obj = ExpRepr(exp, op, pat)
        self.childrens.append(exp_obj)

    def _get_exp_pat_(self, idx):
        idx_ = idx[0]
        if idx_ >= len(self.exp):
            return '', ''
        for op_ in sum(self.operatorList, []):
            if self.exp.find(op_, idx[0]) == idx[0]:
                return '', ''

        for pat in self.pattern:
            if pat == 'special':
                op_idx_ = self._get_next_op_idx(idx)
                bracket_idx_ = self.get_next_bracket_idx(idx)
                if bracket_idx_ == -1 or op_idx_ == -1 and bracket_idx_ == -1:
                    continue
                if bracket_idx_ < op_idx_ or op_idx_ == -1:
                    idx[0] = bracket_idx_
                    self._next_bracket(idx)
                    return self.exp[bracket_idx_+1:idx[0]-1], self.exp[idx_:bracket_idx_+1] + 'e?x?p' + self.exp[idx[0]-1:idx[0]]

            splt_ = pat.split('e?x?p')
            if self.exp.find(splt_[0], idx[0]) == idx[0]:
                if pat == 'e?x?p':
                    next_op_idx_ = self._get_next_op_idx(idx)
                    if next_op_idx_ == -1:
                        idx[0] = len(self.exp)
                        return self.exp[idx_:], pat
                    else:
                        idx[0] = next_op_idx_
                        return self.exp[idx_:next_op_idx_], pat
                else:
                    idx[0] += len(splt_[0]) - 1
                    self._next_bracket(idx)
                    return self.exp[idx_+len(splt_[0]):idx[0]-1], pat

    def _next_bracket(self, idx):
        bracket_idx = self.bracket.index(self.exp[idx[0]])
        cnt_ = 0
        while True:
            if self.exp[idx[0]] == self.bracket[bracket_idx]:
                cnt_ += 1
            if self.exp[idx[0]] == self.left_bracket[bracket_idx]:
                cnt_ -= 1
            idx[0] += 1
            if cnt_ == 0:
                return True

    # idx寻找下一个op的idx如果没找到就返回-1
    def _get_next_op_idx(self, idx):
        return self.get_next_symb_idx(idx, sum(self.operatorList, []))

    # 获取下一个bracket的idx如果没有返回-1
    def get_next_bracket_idx(self, idx):
        return self.get_next_symb_idx(idx, self.bracket)

    def get_next_symb_idx(self, idx, symb_list):
        min_ = 999

        for symb_ in symb_list:
            idx_ = self.exp.find(symb_, idx[0])
            if idx_ != -1:
                min_ = min(min_, idx_)

        return -1 if min_ == 999 else min_

    def print_structure(self):
        self.tree_data = []
        self._load_tree()
        for row in self.tree_data:
            print(row)

    def _load_tree(self, start=0, exp_obj=None, f=0):
        if exp_obj == None:
            exp_obj = self

        width_ = self._get_exp_len(exp_obj)
        indent_ = int((width_ - len(exp_obj.exp)) / 2 + start)
        self._load_tree_data(f, indent_, exp_obj)
        for exp_obj_ in exp_obj.childrens:
            self._load_tree(start, exp_obj_, f+1)
            start += self._get_exp_len(exp_obj_)


    def _get_exp_len(self, exp_obj):
        if len(exp_obj.childrens) == 0:
            return len(self._load_exp(exp_obj)) + 6

        len_ = 0

        for exp_obj_ in exp_obj.childrens:
            len_ += self._get_exp_len(exp_obj_)

        return len_

    def _load_exp(self, exp_obj):
        return exp_obj._op + exp_obj._pat.replace('e?x?p', exp_obj.exp)

    def _load_tree_data(self, f, indent, exp_obj):
        while len(self.tree_data) <= f * 2:
            self.tree_data.append('')

        if f * 2 - 1 >= 0:
            self.tree_data[f*2-1] += ' ' * (indent + int(len(self._load_exp(exp_obj)) / 2) - len(self.tree_data[f*2-1]))
        self.tree_data[f * 2] += ' ' * (indent - len(self.tree_data[f * 2]))

        if f * 2 - 1 >= 0:
            self.tree_data[f*2-1] += '|'
        self.tree_data[f*2] += self._load_exp(exp_obj)

    def exp_repr(self, exp_obj=None):
        if exp_obj == None:
            exp_obj = self

        rst = ''

        if len(exp_obj.childrens) == 0:
            rst = exp_obj.exp
        for cidx, chld in enumerate(exp_obj.childrens):
            exp_ = self.exp_repr(chld)
            if cidx > 0 and (chld._op == '#' or chld._op == ''):
                exp_ = '*' + exp_
            rst += exp_

        rst = exp_obj._pat.replace('e?x?p', rst)
        if exp_obj._op != '#':
            rst = exp_obj._op + rst
        return rst



if __name__ == '__main__':
    # print(' ' * 6 + '123')
    # a = ExpRepr('x*z+y+z+2*cos(c+e*b)')
    # a = ExpRepr('((((Pi)/2))+a)')
    # a = ExpRepr('(bcosC-a)+2bsinC-c=0')
    s = time.time()
    a = ExpRepr('f(x)=((3^(1/2)))(cosx)^2+sinx*cosx+((((3^(1/2)))/2))=((3^(1/2)))*(((1+cos2x)/2))+(1/2)sin2x+((((3^(1/2)))/2))=sin(2x+(((Pi)/3)))+((3^(1/2)))')
    e = time.time()
    print(e-s<0.01)
    # a = ExpRepr('((3^(1/2)))(cosx)^2')
    # a = ExpRepr('(-α<((f(x')
    # a = ExpRepr('-α<k<α')
    # a = ExpRepr('x-6≤-2x≤0')
    # a = ExpRepr('f_S(1)=(Com_1_1)=1')
    # a = ExpRepr('y=1+sin0=1')
    # a = ExpRepr('y=1+sin(-(((Pi)/2)))=0')
    a.print_structure()
    print(a.exp_repr())
    print('')
