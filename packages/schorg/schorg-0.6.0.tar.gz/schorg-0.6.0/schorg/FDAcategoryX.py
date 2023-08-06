"""
A designation by the US FDA signifying that studies in animals or humans have demonstrated fetal abnormalities and/or there is positive evidence of human fetal risk based on adverse reaction data from investigational or marketing experience, and the risks involved in use of the drug in pregnant women clearly outweigh potential benefits.

https://schema.org/FDAcategoryX
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FDAcategoryXInheritedProperties(TypedDict):
    """A designation by the US FDA signifying that studies in animals or humans have demonstrated fetal abnormalities and/or there is positive evidence of human fetal risk based on adverse reaction data from investigational or marketing experience, and the risks involved in use of the drug in pregnant women clearly outweigh potential benefits.

    References:
        https://schema.org/FDAcategoryX
    Note:
        Model Depth 6
    Attributes:
    """

    


class FDAcategoryXProperties(TypedDict):
    """A designation by the US FDA signifying that studies in animals or humans have demonstrated fetal abnormalities and/or there is positive evidence of human fetal risk based on adverse reaction data from investigational or marketing experience, and the risks involved in use of the drug in pregnant women clearly outweigh potential benefits.

    References:
        https://schema.org/FDAcategoryX
    Note:
        Model Depth 6
    Attributes:
    """

    

#FDAcategoryXInheritedPropertiesTd = FDAcategoryXInheritedProperties()
#FDAcategoryXPropertiesTd = FDAcategoryXProperties()


class AllProperties(FDAcategoryXInheritedProperties , FDAcategoryXProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FDAcategoryXProperties, FDAcategoryXInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "FDAcategoryX"
    return model
    

FDAcategoryX = create_schema_org_model()