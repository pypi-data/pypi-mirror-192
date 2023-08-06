"""
BasicIncome: this is a benefit for basic income.

https://schema.org/BasicIncome
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BasicIncomeInheritedProperties(TypedDict):
    """BasicIncome: this is a benefit for basic income.

    References:
        https://schema.org/BasicIncome
    Note:
        Model Depth 5
    Attributes:
    """

    


class BasicIncomeProperties(TypedDict):
    """BasicIncome: this is a benefit for basic income.

    References:
        https://schema.org/BasicIncome
    Note:
        Model Depth 5
    Attributes:
    """

    

#BasicIncomeInheritedPropertiesTd = BasicIncomeInheritedProperties()
#BasicIncomePropertiesTd = BasicIncomeProperties()


class AllProperties(BasicIncomeInheritedProperties , BasicIncomeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BasicIncomeProperties, BasicIncomeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BasicIncome"
    return model
    

BasicIncome = create_schema_org_model()