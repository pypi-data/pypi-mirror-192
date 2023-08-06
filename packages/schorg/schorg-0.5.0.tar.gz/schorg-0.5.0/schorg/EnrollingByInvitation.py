"""
Enrolling participants by invitation only.

https://schema.org/EnrollingByInvitation
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EnrollingByInvitationInheritedProperties(TypedDict):
    """Enrolling participants by invitation only.

    References:
        https://schema.org/EnrollingByInvitation
    Note:
        Model Depth 6
    Attributes:
    """

    


class EnrollingByInvitationProperties(TypedDict):
    """Enrolling participants by invitation only.

    References:
        https://schema.org/EnrollingByInvitation
    Note:
        Model Depth 6
    Attributes:
    """

    

#EnrollingByInvitationInheritedPropertiesTd = EnrollingByInvitationInheritedProperties()
#EnrollingByInvitationPropertiesTd = EnrollingByInvitationProperties()


class AllProperties(EnrollingByInvitationInheritedProperties , EnrollingByInvitationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EnrollingByInvitationProperties, EnrollingByInvitationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EnrollingByInvitation"
    return model
    

EnrollingByInvitation = create_schema_org_model()