"""
A medical procedure intended primarily for palliative purposes, aimed at relieving the symptoms of an underlying health condition.

https://schema.org/PalliativeProcedure
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PalliativeProcedureInheritedProperties(TypedDict):
    """A medical procedure intended primarily for palliative purposes, aimed at relieving the symptoms of an underlying health condition.

    References:
        https://schema.org/PalliativeProcedure
    Note:
        Model Depth 4
    Attributes:
        seriousAdverseOutcome: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A possible serious complication and/or serious side effect of this therapy. Serious adverse outcomes include those that are life-threatening; result in death, disability, or permanent damage; require hospitalization or prolong existing hospitalization; cause congenital anomalies or birth defects; or jeopardize the patient and may require medical or surgical intervention to prevent one of the outcomes in this definition.
        duplicateTherapy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A therapy that duplicates or overlaps this one.
        contraindication: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A contraindication for this therapy.
        howPerformed: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): How the procedure is performed.
        procedureType: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The type of procedure, for example Surgical, Noninvasive, or Percutaneous.
        status: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The status of the study (enumerated).
        bodyLocation: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Location in the body of the anatomical structure.
        followup: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Typical or recommended followup care after the procedure is performed.
        preparation: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Typical preparation that a patient must undergo before having the procedure performed.
    """

    seriousAdverseOutcome: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    duplicateTherapy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    contraindication: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    howPerformed: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    procedureType: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    status: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    bodyLocation: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    followup: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    preparation: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    


class PalliativeProcedureProperties(TypedDict):
    """A medical procedure intended primarily for palliative purposes, aimed at relieving the symptoms of an underlying health condition.

    References:
        https://schema.org/PalliativeProcedure
    Note:
        Model Depth 4
    Attributes:
    """

    

#PalliativeProcedureInheritedPropertiesTd = PalliativeProcedureInheritedProperties()
#PalliativeProcedurePropertiesTd = PalliativeProcedureProperties()


class AllProperties(PalliativeProcedureInheritedProperties , PalliativeProcedureProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PalliativeProcedureProperties, PalliativeProcedureInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PalliativeProcedure"
    return model
    

PalliativeProcedure = create_schema_org_model()