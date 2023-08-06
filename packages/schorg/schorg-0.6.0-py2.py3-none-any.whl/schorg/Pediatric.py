"""
A specific branch of medical science that specializes in the care of infants, children and adolescents.

https://schema.org/Pediatric
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PediatricInheritedProperties(TypedDict):
    """A specific branch of medical science that specializes in the care of infants, children and adolescents.

    References:
        https://schema.org/Pediatric
    Note:
        Model Depth 5
    Attributes:
    """

    


class PediatricProperties(TypedDict):
    """A specific branch of medical science that specializes in the care of infants, children and adolescents.

    References:
        https://schema.org/Pediatric
    Note:
        Model Depth 5
    Attributes:
    """

    

#PediatricInheritedPropertiesTd = PediatricInheritedProperties()
#PediatricPropertiesTd = PediatricProperties()


class AllProperties(PediatricInheritedProperties , PediatricProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PediatricProperties, PediatricInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Pediatric"
    return model
    

Pediatric = create_schema_org_model()