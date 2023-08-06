"""
Used to describe membership in a loyalty programs (e.g. "StarAliance"), traveler clubs (e.g. "AAA"), purchase clubs ("Safeway Club"), etc.

https://schema.org/ProgramMembership
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ProgramMembershipInheritedProperties(TypedDict):
    """Used to describe membership in a loyalty programs (e.g. "StarAliance"), traveler clubs (e.g. "AAA"), purchase clubs ("Safeway Club"), etc.

    References:
        https://schema.org/ProgramMembership
    Note:
        Model Depth 3
    Attributes:
    """

    


class ProgramMembershipProperties(TypedDict):
    """Used to describe membership in a loyalty programs (e.g. "StarAliance"), traveler clubs (e.g. "AAA"), purchase clubs ("Safeway Club"), etc.

    References:
        https://schema.org/ProgramMembership
    Note:
        Model Depth 3
    Attributes:
        member: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A member of an Organization or a ProgramMembership. Organizations can be members of organizations; ProgramMembership is typically for individuals.
        hostingOrganization: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The organization (airline, travelers' club, etc.) the membership is made with.
        membershipNumber: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A unique identifier for the membership.
        members: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A member of this organization.
        membershipPointsEarned: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The number of membership points earned by the member. If necessary, the unitText can be used to express the units the points are issued in. (E.g. stars, miles, etc.)
        programName: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The program providing the membership.
    """

    member: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    hostingOrganization: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    membershipNumber: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    members: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    membershipPointsEarned: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    programName: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#ProgramMembershipInheritedPropertiesTd = ProgramMembershipInheritedProperties()
#ProgramMembershipPropertiesTd = ProgramMembershipProperties()


class AllProperties(ProgramMembershipInheritedProperties , ProgramMembershipProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ProgramMembershipProperties, ProgramMembershipInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ProgramMembership"
    return model
    

ProgramMembership = create_schema_org_model()