"""
Enumerated categories of medical drug costs.

https://schema.org/DrugCostCategory
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DrugCostCategoryInheritedProperties(TypedDict):
    """Enumerated categories of medical drug costs.

    References:
        https://schema.org/DrugCostCategory
    Note:
        Model Depth 5
    Attributes:
    """

    


class DrugCostCategoryProperties(TypedDict):
    """Enumerated categories of medical drug costs.

    References:
        https://schema.org/DrugCostCategory
    Note:
        Model Depth 5
    Attributes:
    """

    

#DrugCostCategoryInheritedPropertiesTd = DrugCostCategoryInheritedProperties()
#DrugCostCategoryPropertiesTd = DrugCostCategoryProperties()


class AllProperties(DrugCostCategoryInheritedProperties , DrugCostCategoryProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DrugCostCategoryProperties, DrugCostCategoryInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DrugCostCategory"
    return model
    

DrugCostCategory = create_schema_org_model()