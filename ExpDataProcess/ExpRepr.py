class ExpRepr(object):

    operatorList = [
        ['=', '>=', '<=', '>', '<'],
        ['+', '-'],
        ['*', '/'],
        ['^', '_']
    ]

    bracket = ['(', '{', '[']

    left_bracket = [')', '}', ']']

    operLevels = ['relation', 'priOperator', 'operator', 'orientation']

    pattern = ['sin(e?x?p)', 'cos(e?x?p)', 'tan(e?x?p)', '(e?x?p)', '[e?x?p]', '{e?x?p}', 'special', 'e?x?p']

    def __init__(self, exp, op='', pat=''):
        self.exp = exp
        self.childrens = []
        self.operLevel = ''
        if self._is_leaf() is not True:
            self._parse_exp()
            self._op = op
            self._pat = pat
        else:
            self._leaf_construct()

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



if __name__ == '__main__':
    a = ExpRepr('f(a)')
    print('sad')
