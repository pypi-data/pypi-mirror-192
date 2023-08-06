"""
The act of editing a recipient by removing one of its objects.

https://schema.org/DeleteAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DeleteActionInheritedProperties(TypedDict):
    """The act of editing a recipient by removing one of its objects.

    References:
        https://schema.org/DeleteAction
    Note:
        Model Depth 4
    Attributes:
        collection: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of object. The collection target of the action.
        targetCollection: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of object. The collection target of the action.
    """

    collection: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    targetCollection: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class DeleteActionProperties(TypedDict):
    """The act of editing a recipient by removing one of its objects.

    References:
        https://schema.org/DeleteAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#DeleteActionInheritedPropertiesTd = DeleteActionInheritedProperties()
#DeleteActionPropertiesTd = DeleteActionProperties()


class AllProperties(DeleteActionInheritedProperties , DeleteActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DeleteActionProperties, DeleteActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DeleteAction"
    return model
    

DeleteAction = create_schema_org_model()