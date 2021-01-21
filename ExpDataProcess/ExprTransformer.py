from ExpDataProcess.ExpRepr import *


class ExprTransformer:

    def __init__(self, _l_expr: ExpRepr = None, _r_expr: ExpRepr = None, _normal_expr: ExpRepr = None):
        """
        该类的初始化方法，参数是两个表达式对象，其分别是左值和右值
        :param _l_expr: ExprRepr 表达式变换的起始
        :param _r_expr: ExprRepr 表达式最终变换形态
        :param _normal_expr: ExpRepr 表达式进行变换的中间形态
        """
        self.__l_expr = _l_expr
        self.__r_expr = _r_expr
        self.__normal_expr = _normal_expr

    def process_expr(self):
        """
        对存储在该类中的表达式进行转换，如果该类没有存储表达式或者没有存储中间表达式，或者该表达式处理失败，那么该方法返回空，
        :return is_process:bool
        """

        pass

    def set_expr(self, _l_expr, _r_expr):
        """
        对该类存储的表达式进行初始化,先要判断传参是否是str
        :param _l_expr 表达式变换的起始
        :param _r_expr 表达式最终变换形态
        :return:
        """
        if isinstance(_l_expr, str):
            _l_expr = ExpRepr(_l_expr)
        if isinstance(_r_expr, str):
            _r_expr = ExpRepr(_r_expr)
        self.__l_expr = _l_expr
        self.__r_expr = _r_expr

    def set_nomal_expr(self, _nomal_expr):
        """
        设置类中的原表达式，即进行表达式插入操作的表达式，先要判断传参是否是str
        :param _normal_expr 想要插入的表达式
        """
        if isinstance(_nomal_expr, str):
            _nomal_expr = ExpRepr(_nomal_expr)
        self.__normal_expr = _nomal_expr


    def show_exp(self):
        """
        直接输出存在该方法中的表达式
        :return:
        """
        if self.__l_expr == None or self.__r_expr == None or self.__normal_expr == None:
            print("you have not initial correctly ! ")
            return
        print("lexp:")
        print(self.__l_expr.exp)
        print("")
        print("rexp:")
        print(self.__r_expr.exp)
        print("")
        print("normalexp:")
        print(self.__normal_expr.exp)
        print("")

    def show_exp_structure(self):
        """
        直接输出存储在该方法中的表达式，以表达式树的形式
        :return:
        """
        if self.__l_expr is None or self.__r_expr is None or self.__normal_expr is None:
            print("you have not initial correctly ! ")
            return
        print("lexp:")
        self.__l_expr.print_structure()
        print("")
        print("rexp:")
        self.__r_expr.print_structure()
        print("")
        print("normalexp:")
        self.__normal_expr.print_structure()
        print("")


if __name__ == '__main__':
    exp1 = ExpRepr("a+b+c")
    exp2 = ExpRepr("a+b+d")
    normal = ExpRepr("a+c")
    et = ExprTransformer(exp1, exp2, normal)
    et.show_exp()
    et.show_exp_structure()
    et.set_nomal_expr(exp1)
    et.show_exp()
