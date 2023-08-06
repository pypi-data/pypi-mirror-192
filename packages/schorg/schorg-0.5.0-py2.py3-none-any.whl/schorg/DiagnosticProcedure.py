"""
A medical procedure intended primarily for diagnostic, as opposed to therapeutic, purposes.

https://schema.org/DiagnosticProcedure
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DiagnosticProcedureInheritedProperties(TypedDict):
    """A medical procedure intended primarily for diagnostic, as opposed to therapeutic, purposes.

    References:
        https://schema.org/DiagnosticProcedure
    Note:
        Model Depth 4
    Attributes:
        howPerformed: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): How the procedure is performed.
        procedureType: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The type of procedure, for example Surgical, Noninvasive, or Percutaneous.
        status: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The status of the study (enumerated).
        bodyLocation: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Location in the body of the anatomical structure.
        followup: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Typical or recommended followup care after the procedure is performed.
        preparation: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Typical preparation that a patient must undergo before having the procedure performed.
    """

    howPerformed: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    procedureType: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    status: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    bodyLocation: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    followup: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    preparation: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    


class DiagnosticProcedureProperties(TypedDict):
    """A medical procedure intended primarily for diagnostic, as opposed to therapeutic, purposes.

    References:
        https://schema.org/DiagnosticProcedure
    Note:
        Model Depth 4
    Attributes:
    """

    

#DiagnosticProcedureInheritedPropertiesTd = DiagnosticProcedureInheritedProperties()
#DiagnosticProcedurePropertiesTd = DiagnosticProcedureProperties()


class AllProperties(DiagnosticProcedureInheritedProperties , DiagnosticProcedureProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DiagnosticProcedureProperties, DiagnosticProcedureInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DiagnosticProcedure"
    return model
    

DiagnosticProcedure = create_schema_org_model()