"""
Any physical activity engaged in for job-related purposes. Examples may include waiting tables, maid service, carrying a mailbag, picking fruits or vegetables, construction work, etc.

https://schema.org/OccupationalActivity
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OccupationalActivityInheritedProperties(TypedDict):
    """Any physical activity engaged in for job-related purposes. Examples may include waiting tables, maid service, carrying a mailbag, picking fruits or vegetables, construction work, etc.

    References:
        https://schema.org/OccupationalActivity
    Note:
        Model Depth 5
    Attributes:
    """

    


class OccupationalActivityProperties(TypedDict):
    """Any physical activity engaged in for job-related purposes. Examples may include waiting tables, maid service, carrying a mailbag, picking fruits or vegetables, construction work, etc.

    References:
        https://schema.org/OccupationalActivity
    Note:
        Model Depth 5
    Attributes:
    """

    

#OccupationalActivityInheritedPropertiesTd = OccupationalActivityInheritedProperties()
#OccupationalActivityPropertiesTd = OccupationalActivityProperties()


class AllProperties(OccupationalActivityInheritedProperties , OccupationalActivityProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OccupationalActivityProperties, OccupationalActivityInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OccupationalActivity"
    return model
    

OccupationalActivity = create_schema_org_model()