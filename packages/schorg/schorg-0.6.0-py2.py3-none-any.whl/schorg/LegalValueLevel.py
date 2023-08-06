"""
A list of possible levels for the legal validity of a legislation.

https://schema.org/LegalValueLevel
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LegalValueLevelInheritedProperties(TypedDict):
    """A list of possible levels for the legal validity of a legislation.

    References:
        https://schema.org/LegalValueLevel
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class LegalValueLevelProperties(TypedDict):
    """A list of possible levels for the legal validity of a legislation.

    References:
        https://schema.org/LegalValueLevel
    Note:
        Model Depth 4
    Attributes:
    """

    

#LegalValueLevelInheritedPropertiesTd = LegalValueLevelInheritedProperties()
#LegalValueLevelPropertiesTd = LegalValueLevelProperties()


class AllProperties(LegalValueLevelInheritedProperties , LegalValueLevelProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LegalValueLevelProperties, LegalValueLevelInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LegalValueLevel"
    return model
    

LegalValueLevel = create_schema_org_model()