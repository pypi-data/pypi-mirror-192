"""
The act of participating in performance arts.

https://schema.org/PerformAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PerformActionInheritedProperties(TypedDict):
    """The act of participating in performance arts.

    References:
        https://schema.org/PerformAction
    Note:
        Model Depth 4
    Attributes:
        event: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Upcoming or past event associated with this place, organization, or action.
        audience: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An intended audience, i.e. a group for whom something was created.
    """

    event: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    audience: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class PerformActionProperties(TypedDict):
    """The act of participating in performance arts.

    References:
        https://schema.org/PerformAction
    Note:
        Model Depth 4
    Attributes:
        entertainmentBusiness: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The entertainment business where the action occurred.
    """

    entertainmentBusiness: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#PerformActionInheritedPropertiesTd = PerformActionInheritedProperties()
#PerformActionPropertiesTd = PerformActionProperties()


class AllProperties(PerformActionInheritedProperties , PerformActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PerformActionProperties, PerformActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PerformAction"
    return model
    

PerformAction = create_schema_org_model()