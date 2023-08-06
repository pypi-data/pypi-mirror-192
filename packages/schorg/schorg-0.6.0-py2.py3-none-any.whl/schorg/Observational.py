"""
An observational study design.

https://schema.org/Observational
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ObservationalInheritedProperties(TypedDict):
    """An observational study design.

    References:
        https://schema.org/Observational
    Note:
        Model Depth 6
    Attributes:
    """

    


class ObservationalProperties(TypedDict):
    """An observational study design.

    References:
        https://schema.org/Observational
    Note:
        Model Depth 6
    Attributes:
    """

    

#ObservationalInheritedPropertiesTd = ObservationalInheritedProperties()
#ObservationalPropertiesTd = ObservationalProperties()


class AllProperties(ObservationalInheritedProperties , ObservationalProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ObservationalProperties, ObservationalInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Observational"
    return model
    

Observational = create_schema_org_model()