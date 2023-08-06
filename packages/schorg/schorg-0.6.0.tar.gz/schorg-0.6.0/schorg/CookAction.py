"""
The act of producing/preparing food.

https://schema.org/CookAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CookActionInheritedProperties(TypedDict):
    """The act of producing/preparing food.

    References:
        https://schema.org/CookAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class CookActionProperties(TypedDict):
    """The act of producing/preparing food.

    References:
        https://schema.org/CookAction
    Note:
        Model Depth 4
    Attributes:
        foodEvent: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The specific food event where the action occurred.
        recipe: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of instrument. The recipe/instructions used to perform the action.
        foodEstablishment: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The specific food establishment where the action occurred.
    """

    foodEvent: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    recipe: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    foodEstablishment: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#CookActionInheritedPropertiesTd = CookActionInheritedProperties()
#CookActionPropertiesTd = CookActionProperties()


class AllProperties(CookActionInheritedProperties , CookActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CookActionProperties, CookActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CookAction"
    return model
    

CookAction = create_schema_org_model()