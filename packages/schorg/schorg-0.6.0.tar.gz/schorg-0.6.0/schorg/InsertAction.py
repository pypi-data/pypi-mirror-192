"""
The act of adding at a specific location in an ordered collection.

https://schema.org/InsertAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class InsertActionInheritedProperties(TypedDict):
    """The act of adding at a specific location in an ordered collection.

    References:
        https://schema.org/InsertAction
    Note:
        Model Depth 5
    Attributes:
    """

    


class InsertActionProperties(TypedDict):
    """The act of adding at a specific location in an ordered collection.

    References:
        https://schema.org/InsertAction
    Note:
        Model Depth 5
    Attributes:
        toLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The final location of the object or the agent after the action.
    """

    toLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#InsertActionInheritedPropertiesTd = InsertActionInheritedProperties()
#InsertActionPropertiesTd = InsertActionProperties()


class AllProperties(InsertActionInheritedProperties , InsertActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[InsertActionProperties, InsertActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "InsertAction"
    return model
    

InsertAction = create_schema_org_model()