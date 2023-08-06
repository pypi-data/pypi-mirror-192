"""
The act of inserting at the end if an ordered collection.

https://schema.org/AppendAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AppendActionInheritedProperties(TypedDict):
    """The act of inserting at the end if an ordered collection.

    References:
        https://schema.org/AppendAction
    Note:
        Model Depth 6
    Attributes:
        toLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The final location of the object or the agent after the action.
    """

    toLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class AppendActionProperties(TypedDict):
    """The act of inserting at the end if an ordered collection.

    References:
        https://schema.org/AppendAction
    Note:
        Model Depth 6
    Attributes:
    """

    

#AppendActionInheritedPropertiesTd = AppendActionInheritedProperties()
#AppendActionPropertiesTd = AppendActionProperties()


class AllProperties(AppendActionInheritedProperties , AppendActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AppendActionProperties, AppendActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AppendAction"
    return model
    

AppendAction = create_schema_org_model()