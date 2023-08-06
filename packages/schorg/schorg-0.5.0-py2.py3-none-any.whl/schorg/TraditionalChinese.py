"""
A system of medicine based on common theoretical concepts that originated in China and evolved over thousands of years, that uses herbs, acupuncture, exercise, massage, dietary therapy, and other methods to treat a wide range of conditions.

https://schema.org/TraditionalChinese
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TraditionalChineseInheritedProperties(TypedDict):
    """A system of medicine based on common theoretical concepts that originated in China and evolved over thousands of years, that uses herbs, acupuncture, exercise, massage, dietary therapy, and other methods to treat a wide range of conditions.

    References:
        https://schema.org/TraditionalChinese
    Note:
        Model Depth 6
    Attributes:
    """

    


class TraditionalChineseProperties(TypedDict):
    """A system of medicine based on common theoretical concepts that originated in China and evolved over thousands of years, that uses herbs, acupuncture, exercise, massage, dietary therapy, and other methods to treat a wide range of conditions.

    References:
        https://schema.org/TraditionalChinese
    Note:
        Model Depth 6
    Attributes:
    """

    

#TraditionalChineseInheritedPropertiesTd = TraditionalChineseInheritedProperties()
#TraditionalChinesePropertiesTd = TraditionalChineseProperties()


class AllProperties(TraditionalChineseInheritedProperties , TraditionalChineseProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TraditionalChineseProperties, TraditionalChineseInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "TraditionalChinese"
    return model
    

TraditionalChinese = create_schema_org_model()