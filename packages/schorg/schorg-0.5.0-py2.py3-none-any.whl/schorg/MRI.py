"""
Magnetic resonance imaging.

https://schema.org/MRI
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MRIInheritedProperties(TypedDict):
    """Magnetic resonance imaging.

    References:
        https://schema.org/MRI
    Note:
        Model Depth 6
    Attributes:
    """

    


class MRIProperties(TypedDict):
    """Magnetic resonance imaging.

    References:
        https://schema.org/MRI
    Note:
        Model Depth 6
    Attributes:
    """

    

#MRIInheritedPropertiesTd = MRIInheritedProperties()
#MRIPropertiesTd = MRIProperties()


class AllProperties(MRIInheritedProperties , MRIProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MRIProperties, MRIInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MRI"
    return model
    

MRI = create_schema_org_model()