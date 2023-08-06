"""
Play mode: CoOp. Co-operative games, where you play on the same team with friends.

https://schema.org/CoOp
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CoOpInheritedProperties(TypedDict):
    """Play mode: CoOp. Co-operative games, where you play on the same team with friends.

    References:
        https://schema.org/CoOp
    Note:
        Model Depth 5
    Attributes:
    """

    


class CoOpProperties(TypedDict):
    """Play mode: CoOp. Co-operative games, where you play on the same team with friends.

    References:
        https://schema.org/CoOp
    Note:
        Model Depth 5
    Attributes:
    """

    

#CoOpInheritedPropertiesTd = CoOpInheritedProperties()
#CoOpPropertiesTd = CoOpProperties()


class AllProperties(CoOpInheritedProperties , CoOpProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CoOpProperties, CoOpInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CoOp"
    return model
    

CoOp = create_schema_org_model()