"""
The act of participating in exertive activity for the purposes of improving health and fitness.

https://schema.org/ExerciseAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ExerciseActionInheritedProperties(TypedDict):
    """The act of participating in exertive activity for the purposes of improving health and fitness.

    References:
        https://schema.org/ExerciseAction
    Note:
        Model Depth 4
    Attributes:
        event: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Upcoming or past event associated with this place, organization, or action.
        audience: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An intended audience, i.e. a group for whom something was created.
    """

    event: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    audience: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class ExerciseActionProperties(TypedDict):
    """The act of participating in exertive activity for the purposes of improving health and fitness.

    References:
        https://schema.org/ExerciseAction
    Note:
        Model Depth 4
    Attributes:
        toLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The final location of the object or the agent after the action.
        course: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The course where this action was taken.
        fromLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The original location of the object or the agent before the action.
        exerciseRelatedDiet: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of instrument. The diet used in this action.
        exerciseCourse: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The course where this action was taken.
        opponent: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of participant. The opponent on this action.
        sportsTeam: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of participant. The sports team that participated on this action.
        sportsEvent: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The sports event where this action occurred.
        diet: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of instrument. The diet used in this action.
        exercisePlan: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of instrument. The exercise plan used on this action.
        exerciseType: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Type(s) of exercise or activity, such as strength training, flexibility training, aerobics, cardiac rehabilitation, etc.
        distance: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The distance travelled, e.g. exercising or travelling.
        sportsActivityLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The sports activity location where this action occurred.
    """

    toLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    course: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    fromLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    exerciseRelatedDiet: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    exerciseCourse: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    opponent: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    sportsTeam: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    sportsEvent: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    diet: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    exercisePlan: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    exerciseType: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    distance: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    sportsActivityLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#ExerciseActionInheritedPropertiesTd = ExerciseActionInheritedProperties()
#ExerciseActionPropertiesTd = ExerciseActionProperties()


class AllProperties(ExerciseActionInheritedProperties , ExerciseActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ExerciseActionProperties, ExerciseActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ExerciseAction"
    return model
    

ExerciseAction = create_schema_org_model()