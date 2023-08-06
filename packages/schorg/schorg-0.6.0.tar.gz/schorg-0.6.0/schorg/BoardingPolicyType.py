"""
A type of boarding policy used by an airline.

https://schema.org/BoardingPolicyType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BoardingPolicyTypeInheritedProperties(TypedDict):
    """A type of boarding policy used by an airline.

    References:
        https://schema.org/BoardingPolicyType
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class BoardingPolicyTypeProperties(TypedDict):
    """A type of boarding policy used by an airline.

    References:
        https://schema.org/BoardingPolicyType
    Note:
        Model Depth 4
    Attributes:
    """

    

#BoardingPolicyTypeInheritedPropertiesTd = BoardingPolicyTypeInheritedProperties()
#BoardingPolicyTypePropertiesTd = BoardingPolicyTypeProperties()


class AllProperties(BoardingPolicyTypeInheritedProperties , BoardingPolicyTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BoardingPolicyTypeProperties, BoardingPolicyTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BoardingPolicyType"
    return model
    

BoardingPolicyType = create_schema_org_model()