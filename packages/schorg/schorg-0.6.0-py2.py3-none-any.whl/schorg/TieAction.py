"""
The act of reaching a draw in a competitive activity.

https://schema.org/TieAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TieActionInheritedProperties(TypedDict):
    """The act of reaching a draw in a competitive activity.

    References:
        https://schema.org/TieAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class TieActionProperties(TypedDict):
    """The act of reaching a draw in a competitive activity.

    References:
        https://schema.org/TieAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#TieActionInheritedPropertiesTd = TieActionInheritedProperties()
#TieActionPropertiesTd = TieActionProperties()


class AllProperties(TieActionInheritedProperties , TieActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TieActionProperties, TieActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "TieAction"
    return model
    

TieAction = create_schema_org_model()