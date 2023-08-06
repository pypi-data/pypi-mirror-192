"""
A specific branch of medical science that is concerned with poisons, their nature, effects and detection and involved in the treatment of poisoning.

https://schema.org/Toxicologic
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ToxicologicInheritedProperties(TypedDict):
    """A specific branch of medical science that is concerned with poisons, their nature, effects and detection and involved in the treatment of poisoning.

    References:
        https://schema.org/Toxicologic
    Note:
        Model Depth 6
    Attributes:
    """

    


class ToxicologicProperties(TypedDict):
    """A specific branch of medical science that is concerned with poisons, their nature, effects and detection and involved in the treatment of poisoning.

    References:
        https://schema.org/Toxicologic
    Note:
        Model Depth 6
    Attributes:
    """

    

#ToxicologicInheritedPropertiesTd = ToxicologicInheritedProperties()
#ToxicologicPropertiesTd = ToxicologicProperties()


class AllProperties(ToxicologicInheritedProperties , ToxicologicProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ToxicologicProperties, ToxicologicInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Toxicologic"
    return model
    

Toxicologic = create_schema_org_model()