"""
The act of downloading an object.

https://schema.org/DownloadAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DownloadActionInheritedProperties(TypedDict):
    """The act of downloading an object.

    References:
        https://schema.org/DownloadAction
    Note:
        Model Depth 4
    Attributes:
        toLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The final location of the object or the agent after the action.
        fromLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The original location of the object or the agent before the action.
    """

    toLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    fromLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class DownloadActionProperties(TypedDict):
    """The act of downloading an object.

    References:
        https://schema.org/DownloadAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#DownloadActionInheritedPropertiesTd = DownloadActionInheritedProperties()
#DownloadActionPropertiesTd = DownloadActionProperties()


class AllProperties(DownloadActionInheritedProperties , DownloadActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DownloadActionProperties, DownloadActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DownloadAction"
    return model
    

DownloadAction = create_schema_org_model()