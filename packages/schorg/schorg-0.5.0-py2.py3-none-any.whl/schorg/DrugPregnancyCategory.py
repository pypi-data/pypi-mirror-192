"""
Categories that represent an assessment of the risk of fetal injury due to a drug or pharmaceutical used as directed by the mother during pregnancy.

https://schema.org/DrugPregnancyCategory
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DrugPregnancyCategoryInheritedProperties(TypedDict):
    """Categories that represent an assessment of the risk of fetal injury due to a drug or pharmaceutical used as directed by the mother during pregnancy.

    References:
        https://schema.org/DrugPregnancyCategory
    Note:
        Model Depth 5
    Attributes:
    """

    


class DrugPregnancyCategoryProperties(TypedDict):
    """Categories that represent an assessment of the risk of fetal injury due to a drug or pharmaceutical used as directed by the mother during pregnancy.

    References:
        https://schema.org/DrugPregnancyCategory
    Note:
        Model Depth 5
    Attributes:
    """

    

#DrugPregnancyCategoryInheritedPropertiesTd = DrugPregnancyCategoryInheritedProperties()
#DrugPregnancyCategoryPropertiesTd = DrugPregnancyCategoryProperties()


class AllProperties(DrugPregnancyCategoryInheritedProperties , DrugPregnancyCategoryProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DrugPregnancyCategoryProperties, DrugPregnancyCategoryInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DrugPregnancyCategory"
    return model
    

DrugPregnancyCategory = create_schema_org_model()