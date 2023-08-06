"""
X-ray computed tomography imaging.

https://schema.org/CT
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CTInheritedProperties(TypedDict):
    """X-ray computed tomography imaging.

    References:
        https://schema.org/CT
    Note:
        Model Depth 6
    Attributes:
    """

    


class CTProperties(TypedDict):
    """X-ray computed tomography imaging.

    References:
        https://schema.org/CT
    Note:
        Model Depth 6
    Attributes:
    """

    

#CTInheritedPropertiesTd = CTInheritedProperties()
#CTPropertiesTd = CTProperties()


class AllProperties(CTInheritedProperties , CTProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CTProperties, CTInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CT"
    return model
    

CT = create_schema_org_model()