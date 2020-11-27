import math


class ExpRepr(object):
    childrens = []

    operatorList = [
        ['=', '>=', '<=', '>', '<'],
        ['+', '-'],
        ['*', '/'],
        ['^', '_']
    ]

    bracket = ['(', '{', '[', '|']

    left_bracket = [')', '}', '[', '|']

    operLevels = ['relation', 'priOperator', 'operator', 'orientation']

    pattern = ['sin(e?x?p)', 'cos(e?x?p)', 'tan(e?x?p)', '(e?x?p)', '{e?x?p}', 'special', 'e?x?p']

    def __init__(self, Exp):
        self.operLevel = ''
        if self._is_leaf(Exp) is not True:
            self._parse_exp(Exp)

    def __init__(self, Exp, op, pat):
        self.__init__(Exp)
        self._op = op
        self._pat = pat

    def _is_leaf(self, exp):
        idx_ = [0]
        min_idx_ = self._get_next_op_idx(exp, idx_)

        if min_idx_ == -1:
            return False

        return True

    def _parse_exp(self, Exp):
        for index, oList in enumerate(self.operatorList):
            if self.__parse_exp_op(Exp, oList) is True:
                self.operLevel = self.operLevels[index]
                return

    # 定义了各种状态：
    # start 开始匹配的状态，只有开始时是
    def __parse_exp_op(self, Exp, oList):
        state = 'start'
        idx = [0]
        op_ = ''
        exp_ = ''
        while idx[0] < len(Exp):
            op_ = self._get_op(idx, Exp, oList)
            exp_, pat_ = self._get_exp_pat(idx, Exp, oList)
            if state == 'start':
                if op_ == '':
                    op_ = '#'

                state = 'normal'

            self._new_exp(op_, exp_, pat_)

    def _get_op(self, idx, exp, oList):
        for op_ in oList:
            if exp.find(op_, idx[0]) == idx[0]:
                idx[0] += len(op_)
                return op_

        return ''

    def _get_exp_pat(self, idx, exp, oList):
        r_exp_ = ''
        mod_ = 'start'
        while True:
            exp_, pat_ = self._get_exp_pat_(idx, exp)
            op_ = self._get_op(idx, exp, oList)

            if exp_ == '':
                pass
            elif op_ == '':
                pass
            elif oList.count(op_) > 0:
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

    def _get_exp_pat_(self, idx, exp):
        idx_ = idx[0]
        for op_ in sum(self.operatorList, []):
            if exp.find(op_, idx[0]) == idx[0]:
                return ''

        for pat in self.pattern:
            if pat == 'special':
                op_idx_ = self._get_next_op_idx(exp, idx)
                bracket_idx_ = self.get_next_bracket_idx(exp, idx)
                if bracket_idx_ < op_idx_:
                    self._next_bracket(idx, exp)
                    return exp[bracket_idx_:idx[0]-1], exp[idx_:bracket_idx_+1] + 'e?x?p' + exp[idx[0]:idx[0]+1]

            splt_ = pat.split('e?x?p')
            if exp.find(splt_[0:-1], idx[0]) == idx[0]:
                idx[0] += len(splt_) - 1
                self._next_bracket(idx, exp)
                return exp[idx_+len(splt_):idx[0]-1], pat

    def _next_bracket(self, idx, exp):
        bracket_idx = self.bracket.index(exp[idx[0]])
        cnt_ = 0
        while True:
            if exp[idx[0]] == self.bracket[bracket_idx]:
                cnt_ += 1

            if exp[idx[0]] == self.left_bracket[bracket_idx]:
                cnt_ -= 1

            idx[0] += 1
            if cnt_ == 0:
                return

    # idx寻找下一个op的idx如果没找到就返回-1
    def _get_next_op_idx(self, exp, idx):
        return self.get_next_symb_idx(exp, idx, sum(operatorList, []))

    # 获取下一个bracket的idx如果没有返回-1
    def get_next_bracket_idx(self, exp, idx):
        return self.get_next_symb_idx(exp, idx, self.bracket)

    def get_next_symb_idx(self, exp, idx, symb_list):
        min_ = 999

        for symb_ in symb_list:
            idx_ = exp.find(symb_, idx[0])
            if idx_ != -1:
                min_ = math.min(min_, idx_)

        return -1 if min_ == 999 else min_


if __name__ == '__main__':
    operatorList = [
        ['=', '>=', '<=', '>', '<'],
        ['+', '-'],
        ['*', '/'],
        ['^', '_']
    ]

    str = '2cos(e?x?p)'
    print(str.replace('e?x?p', 'a+b'))

    for _, idx in enumerate(str):
        print(_)

