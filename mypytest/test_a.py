# 所有的单测文件名都需要满足test_*.py格式或*_test.py格式。
# 在单测文件中，测试类以Test开头，
# 并且不能带有 init 方法(注意：定义class时，需要以T开头，不然pytest是不会去运行该class的)

import pytest  # 引入pytest包


def test_aa():  # test开头的测试函数
    print("------->test_a")
    assert 1  # 断言成功


def test_b():
    print("------->test_b")
    assert 1  # 断言成功


if __name__ == '__main__':
    pytest.main("-s test_aa.py")  # 调用pytest的main函数执行测试
