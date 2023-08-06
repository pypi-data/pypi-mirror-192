"""
The female gender.

https://schema.org/Female
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FemaleInheritedProperties(TypedDict):
    """The female gender.

    References:
        https://schema.org/Female
    Note:
        Model Depth 5
    Attributes:
    """

    


class FemaleProperties(TypedDict):
    """The female gender.

    References:
        https://schema.org/Female
    Note:
        Model Depth 5
    Attributes:
    """

    

#FemaleInheritedPropertiesTd = FemaleInheritedProperties()
#FemalePropertiesTd = FemaleProperties()


class AllProperties(FemaleInheritedProperties , FemaleProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FemaleProperties, FemaleInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Female"
    return model
    

Female = create_schema_org_model()