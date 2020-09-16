from . import *
import pytest


packages = ['N10_inheritance_2',
            'N11_polymorphism_1',
            'N12_polymorphism_2',
            'N13_inheriting_init_constructor_1',
            'N14_multiple_inheritance_1',
            'N15_multiple_inheritance_2',
            'N16_multiple_inheritance_3',
            'N17_instance_methods_1',
            'N18_instance_methods_2',
            'N19_decorators_1',
            'N1_encapsulation_1',
            'N20_decorators_2',
            'N21_decorators_3',
            'N22_decorators_4',
            'N23_decorators_5',
            'N24_decorators_6',
            'N25_decorators_7',
            'N26_class_decorators',
            'N27_classmethod_1',
            'N28_classmethod_2',
            'N29_staticmethod_1',
            'N2_encapsulation_2',
            'N30_staticmethod_2',
            'N31_magicmethods_1',
            'N32_magicmethods_2',
            'N34_abstractclasses',
            'N35_abstractclasses_2',
            'N36_abstractclasses_3',
            'N37_method_overloading_1',
            'N38_method_overloading_2',
            'N39_method_overloading_3',
            'N3_encapsulation_3',
            'N40_super_1',
            'N41_super_2',
            'N42_super_3',
            'N4_init_constructor_1',
            'N5_init_constructor_2',
            'N6_class_attributes_1',
            'N7_class_attributes_2',
            'N8_class_instance_attributes_1',
            'N9_inheritance_1']

# from . import *   只要导入的包，就会执行


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