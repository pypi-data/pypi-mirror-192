"""
A designation by the US FDA signifying that animal reproduction studies have shown an adverse effect on the fetus and there are no adequate and well-controlled studies in humans, but potential benefits may warrant use of the drug in pregnant women despite potential risks.

https://schema.org/FDAcategoryC
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FDAcategoryCInheritedProperties(TypedDict):
    """A designation by the US FDA signifying that animal reproduction studies have shown an adverse effect on the fetus and there are no adequate and well-controlled studies in humans, but potential benefits may warrant use of the drug in pregnant women despite potential risks.

    References:
        https://schema.org/FDAcategoryC
    Note:
        Model Depth 6
    Attributes:
    """

    


class FDAcategoryCProperties(TypedDict):
    """A designation by the US FDA signifying that animal reproduction studies have shown an adverse effect on the fetus and there are no adequate and well-controlled studies in humans, but potential benefits may warrant use of the drug in pregnant women despite potential risks.

    References:
        https://schema.org/FDAcategoryC
    Note:
        Model Depth 6
    Attributes:
    """

    

#FDAcategoryCInheritedPropertiesTd = FDAcategoryCInheritedProperties()
#FDAcategoryCPropertiesTd = FDAcategoryCProperties()


class AllProperties(FDAcategoryCInheritedProperties , FDAcategoryCProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FDAcategoryCProperties, FDAcategoryCInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "FDAcategoryC"
    return model
    

FDAcategoryC = create_schema_org_model()