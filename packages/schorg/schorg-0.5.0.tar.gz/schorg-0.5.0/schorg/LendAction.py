"""
The act of providing an object under an agreement that it will be returned at a later date. Reciprocal of BorrowAction.Related actions:* [[BorrowAction]]: Reciprocal of LendAction.

https://schema.org/LendAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LendActionInheritedProperties(TypedDict):
    """The act of providing an object under an agreement that it will be returned at a later date. Reciprocal of BorrowAction.Related actions:* [[BorrowAction]]: Reciprocal of LendAction.

    References:
        https://schema.org/LendAction
    Note:
        Model Depth 4
    Attributes:
        toLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The final location of the object or the agent after the action.
        fromLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The original location of the object or the agent before the action.
    """

    toLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    fromLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class LendActionProperties(TypedDict):
    """The act of providing an object under an agreement that it will be returned at a later date. Reciprocal of BorrowAction.Related actions:* [[BorrowAction]]: Reciprocal of LendAction.

    References:
        https://schema.org/LendAction
    Note:
        Model Depth 4
    Attributes:
        borrower: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of participant. The person that borrows the object being lent.
    """

    borrower: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#LendActionInheritedPropertiesTd = LendActionInheritedProperties()
#LendActionPropertiesTd = LendActionProperties()


class AllProperties(LendActionInheritedProperties , LendActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LendActionProperties, LendActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LendAction"
    return model
    

LendAction = create_schema_org_model()