"""
A designation by the US FDA signifying that there is positive evidence of human fetal risk based on adverse reaction data from investigational or marketing experience or studies in humans, but potential benefits may warrant use of the drug in pregnant women despite potential risks.

https://schema.org/FDAcategoryD
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FDAcategoryDInheritedProperties(TypedDict):
    """A designation by the US FDA signifying that there is positive evidence of human fetal risk based on adverse reaction data from investigational or marketing experience or studies in humans, but potential benefits may warrant use of the drug in pregnant women despite potential risks.

    References:
        https://schema.org/FDAcategoryD
    Note:
        Model Depth 6
    Attributes:
    """

    


class FDAcategoryDProperties(TypedDict):
    """A designation by the US FDA signifying that there is positive evidence of human fetal risk based on adverse reaction data from investigational or marketing experience or studies in humans, but potential benefits may warrant use of the drug in pregnant women despite potential risks.

    References:
        https://schema.org/FDAcategoryD
    Note:
        Model Depth 6
    Attributes:
    """

    

#FDAcategoryDInheritedPropertiesTd = FDAcategoryDInheritedProperties()
#FDAcategoryDPropertiesTd = FDAcategoryDProperties()


class AllProperties(FDAcategoryDInheritedProperties , FDAcategoryDProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FDAcategoryDProperties, FDAcategoryDInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "FDAcategoryD"
    return model
    

FDAcategoryD = create_schema_org_model()