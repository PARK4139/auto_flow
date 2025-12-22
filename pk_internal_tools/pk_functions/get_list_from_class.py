import logging
from typing import Any, List

from pk_internal_tools.pk_objects.pk_modes import PkModesForGetListFromClass


def get_list_from_class(
        target_class: Any,
        member_type: PkModesForGetListFromClass = PkModesForGetListFromClass.ALL
) -> List[Any]:
    import inspect

    from pk_internal_tools.pk_objects.pk_modes import PkModesForGetListFromClass

    if not inspect.isclass(target_class):
        raise TypeError("target_class 인자는 클래스여야 합니다.")

    members = inspect.getmembers(target_class)
    result = []

    if member_type == PkModesForGetListFromClass.ALL:
        result = [name for name, _ in members]
    elif member_type == PkModesForGetListFromClass.METHOD:
        result = [name for name, value in members if inspect.isfunction(value) or inspect.ismethod(value)]
    elif member_type == PkModesForGetListFromClass.ATTRIBUTE:
        # Enum의 경우, 클래스의 인스턴스인 멤버만 필터링하여 순수 멤버 이름만 반환
        result = [
            name for name, value in members
            if isinstance(value, target_class)
        ]
    elif member_type == PkModesForGetListFromClass.ATTRIBUTE_VALUE:
        # Enum의 경우, 클래스의 인스턴스인 멤버의 '값'만 필터링하여 반환
        result = [
            value.value for name, value in members
            if isinstance(value, target_class)
        ]

    return result


if __name__ == '__main__':
    from enum import Enum


    class WslDistrosNotSupportedOfficiallyAnymore(Enum):
        ubuntu_18_04 = "Ubuntu-18.04"


    logging.debug("--- 속성 이름 ---")
    attributes = get_list_from_class(WslDistrosNotSupportedOfficiallyAnymore, PkModesForGetListFromClass.ATTRIBUTE)
    logging.debug(attributes)

    logging.debug("--- 속성 값 ---")
    attribute_values = get_list_from_class(WslDistrosNotSupportedOfficiallyAnymore, PkModesForGetListFromClass.ATTRIBUTE_VALUE)
    logging.debug(attribute_values)


    class ExampleClass:
        class_variable = "I am a class variable"

        def __init__(self, instance_variable):
            self.instance_variable = instance_variable

        def example_method(self):
            """This is an example method."""
            return "Hello from method"


    logging.debug("--- 모든 멤버 ---")
    all_members = get_list_from_class(ExampleClass, PkModesForGetListFromClass.ALL)
    logging.debug(all_members)

    logging.debug("--- 메서드 ---")
    methods = get_list_from_class(ExampleClass, PkModesForGetListFromClass.METHOD)
    logging.debug(methods)
