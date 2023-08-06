"""
A subclass of OrganizationRole used to describe employee relationships.

https://schema.org/EmployeeRole
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EmployeeRoleInheritedProperties(TypedDict):
    """A subclass of OrganizationRole used to describe employee relationships.

    References:
        https://schema.org/EmployeeRole
    Note:
        Model Depth 5
    Attributes:
        numberedPosition: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): A number associated with a role in an organization, for example, the number on an athlete's jersey.
    """

    numberedPosition: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    


class EmployeeRoleProperties(TypedDict):
    """A subclass of OrganizationRole used to describe employee relationships.

    References:
        https://schema.org/EmployeeRole
    Note:
        Model Depth 5
    Attributes:
        baseSalary: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The base salary of the job or of an employee in an EmployeeRole.
        salaryCurrency: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The currency (coded using [ISO 4217](http://en.wikipedia.org/wiki/ISO_4217)) used for the main salary information in this job posting or for this employee.
    """

    baseSalary: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    salaryCurrency: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#EmployeeRoleInheritedPropertiesTd = EmployeeRoleInheritedProperties()
#EmployeeRolePropertiesTd = EmployeeRoleProperties()


class AllProperties(EmployeeRoleInheritedProperties , EmployeeRoleProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EmployeeRoleProperties, EmployeeRoleInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EmployeeRole"
    return model
    

EmployeeRole = create_schema_org_model()