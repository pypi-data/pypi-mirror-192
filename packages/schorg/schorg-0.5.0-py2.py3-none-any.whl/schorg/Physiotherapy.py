"""
The practice of treatment of disease, injury, or deformity by physical methods such as massage, heat treatment, and exercise rather than by drugs or surgery.

https://schema.org/Physiotherapy
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PhysiotherapyInheritedProperties(TypedDict):
    """The practice of treatment of disease, injury, or deformity by physical methods such as massage, heat treatment, and exercise rather than by drugs or surgery.

    References:
        https://schema.org/Physiotherapy
    Note:
        Model Depth 5
    Attributes:
    """

    


class PhysiotherapyProperties(TypedDict):
    """The practice of treatment of disease, injury, or deformity by physical methods such as massage, heat treatment, and exercise rather than by drugs or surgery.

    References:
        https://schema.org/Physiotherapy
    Note:
        Model Depth 5
    Attributes:
    """

    

#PhysiotherapyInheritedPropertiesTd = PhysiotherapyInheritedProperties()
#PhysiotherapyPropertiesTd = PhysiotherapyProperties()


class AllProperties(PhysiotherapyInheritedProperties , PhysiotherapyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PhysiotherapyProperties, PhysiotherapyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Physiotherapy"
    return model
    

Physiotherapy = create_schema_org_model()