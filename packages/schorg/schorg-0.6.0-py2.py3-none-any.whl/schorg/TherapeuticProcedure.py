"""
A medical procedure intended primarily for therapeutic purposes, aimed at improving a health condition.

https://schema.org/TherapeuticProcedure
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TherapeuticProcedureInheritedProperties(TypedDict):
    """A medical procedure intended primarily for therapeutic purposes, aimed at improving a health condition.

    References:
        https://schema.org/TherapeuticProcedure
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
    


class TherapeuticProcedureProperties(TypedDict):
    """A medical procedure intended primarily for therapeutic purposes, aimed at improving a health condition.

    References:
        https://schema.org/TherapeuticProcedure
    Note:
        Model Depth 4
    Attributes:
        doseSchedule: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A dosing schedule for the drug for a given population, either observed, recommended, or maximum dose based on the type used.
        drug: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Specifying a drug or medicine used in a medication procedure.
        adverseOutcome: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A possible complication and/or side effect of this therapy. If it is known that an adverse outcome is serious (resulting in death, disability, or permanent damage; requiring hospitalization; or otherwise life-threatening or requiring immediate medical attention), tag it as a seriousAdverseOutcome instead.
    """

    doseSchedule: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    drug: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    adverseOutcome: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#TherapeuticProcedureInheritedPropertiesTd = TherapeuticProcedureInheritedProperties()
#TherapeuticProcedurePropertiesTd = TherapeuticProcedureProperties()


class AllProperties(TherapeuticProcedureInheritedProperties , TherapeuticProcedureProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TherapeuticProcedureProperties, TherapeuticProcedureInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "TherapeuticProcedure"
    return model
    

TherapeuticProcedure = create_schema_org_model()