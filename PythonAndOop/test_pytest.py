from . import *
import pytest



# from . import *   在测试中只要导入的包，就会执行里面的代码,尤其是有运行环节的,所以包中执行的部分要放在main下面


@pytest.mark.test1
@pytest.mark.parametrize(
    "shuru,shuchu_expected",
    [
        ('a','a'),
        (1,1),
        ([1],[1]),
        ({"test":1},{"test":1}),
        ((1,),(1,)),
        ({1},{1}),
    ]
)
def test_N1_encapsulation_1(shuru,shuchu_expected):
    val=N1_encapsulation_1.MyClass()
    val.set_val(shuru)
    assert shuchu_expected==val.get_val()

@pytest.mark.parametrize(
    "shuru,shuchu_expected",
    [
        ('a','a'),
        (1,1),
        ([1],[1]),
        ({"test":1},{"test":1}),
        ((1,),(1,)),
        ({1},{1}),
    ]
)
def test_N2_encapsulation_1(shuru,shuchu_expected):
    val=N2_encapsulation_2.MyClass()
    val.set_val(shuru)
    assert shuchu_expected==val.value


@pytest.mark.parametrize(
    "set_val_param1,val_expected_after_increment",
    [
        ('1',2),
        (1,2),
    ]
)
def test_N3_encapsulation_3(set_val_param1,val_expected_after_increment):
    #数字取整，获得或加一
    object = N3_encapsulation_3.MyInteger()
    object.set_val(set_val_param1)
    object.increment_val()
    assert val_expected_after_increment==object.val


@pytest.mark.parametrize(
    "val_expected_after_increment",
    [
        1,
    ]
)
def test_N4_init_constructor_1(val_expected_after_increment):
    n4 =N4_init_constructor_1.MyNum()
    n4.increment()
    assert val_expected_after_increment==n4.val

@pytest.mark.parametrize(
    "set_val_param1,val_expected_after_increment",
    [
        (1,2),
        ('1',2),
        ('a',1),
    ]
)
def test_N5_init_constructor_2(set_val_param1,val_expected_after_increment):
    n5 =N5_init_constructor_2.MyNum(set_val_param1)
    n5.increment()
    assert val_expected_after_increment==n5.value

@pytest.mark.parametrize(
    "class_attri,instance_attri",
    [
        (10,100),
    ]
)
def test_N6_class_attributes_1(class_attri,instance_attri):
    n6=N6_class_attributes_1.YourClass()
    n6.set_val()
    assert class_attri==n6.classy and instance_attri==n6.insty

@pytest.mark.parametrize(
    "class_attri",
    [
        "class value",
    ]
)
def test_N7_class_attributes_2(class_attri):
    n7=N7_class_attributes_2.YourClass()
    assert class_attri==n7.classy

@pytest.mark.parametrize(
    "set_value",
    [
        "set_value",
        1,
    ]
)
def test_N8_class_instance_attributes_1(set_value):
    count=N8_class_instance_attributes_1.InstanceCounter.count
    n8=N8_class_instance_attributes_1.InstanceCounter(set_value)
    #print(N8_class_instance_attributes_1.InstanceCounter.count)  内部测试print函数不好使
    assert count+1==N8_class_instance_attributes_1.InstanceCounter.count

@pytest.mark.parametrize(
    "date,time",
    [
        ('2020-09-19','21:28:10')
    ]
)
def test_N9_inheritance_1(date,time):
    n9=N9_inheritance_1.Time()
    assert date==n9.get_date(date) and time==n9.get_time(time)

