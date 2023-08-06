"""
The act of editing a recipient by replacing an old object with a new object.

https://schema.org/ReplaceAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReplaceActionInheritedProperties(TypedDict):
    """The act of editing a recipient by replacing an old object with a new object.

    References:
        https://schema.org/ReplaceAction
    Note:
        Model Depth 4
    Attributes:
        collection: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of object. The collection target of the action.
        targetCollection: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of object. The collection target of the action.
    """

    collection: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    targetCollection: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class ReplaceActionProperties(TypedDict):
    """The act of editing a recipient by replacing an old object with a new object.

    References:
        https://schema.org/ReplaceAction
    Note:
        Model Depth 4
    Attributes:
        replacee: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of object. The object that is being replaced.
        replacer: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of object. The object that replaces.
    """

    replacee: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    replacer: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#ReplaceActionInheritedPropertiesTd = ReplaceActionInheritedProperties()
#ReplaceActionPropertiesTd = ReplaceActionProperties()


class AllProperties(ReplaceActionInheritedProperties , ReplaceActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReplaceActionProperties, ReplaceActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReplaceAction"
    return model
    

ReplaceAction = create_schema_org_model()