## pytest 
#### 基本用法
- 写好测试文件
```angular2
filename:test.py
相同函数测试边界值
import pytest
　
@pytest.mark.parametrize(
"x,expected",
[(1,1),
(2,2),
]
)
def test1(x):
    assert 目标值==测试函数的返回值
测试异常代码是否可用：
    with pytest.raises(Error类型)
        执行带有错误参数函数

shell:
pytest -vv test.py
-vv 输出详细的测试内容

pytest单独执行,会测试当前文件夹下面所有test开头的py文件
调优可用参数：
--durations=１ 测试１ｓ以上的方法
--markers 查看分组
-m groupname 选择只测试哪个组的函数

组的设置,在测试文件所在目录创建pytest.ini文件
[pytest]
markers = 
    自定义组名1:详细描述.
    自定义组名2:详细描述.

```