import { Dispatch } from "redux";
import { newPlanAssessment } from "../interfaces/new-store";
import { OperatingContext } from "../interfaces/operating-context";
//import { PlanAssessment } from "../interfaces/plan-assessment";

/**
 * Base payload type.
 */
export interface BaseActionPayload {
    /**
     * Action type.
     */
    type: string;
}

/**
 * Type for updating plan assessment.
 */
 export const UPDATE_PLAN_ASSESSMENT = "UpdatePlanAssessment";

/**
 * Payload for updating plan assessment.
 */
export interface UpdatePlanAssessmentPayload extends BaseActionPayload {
    /**
     * Data to update with.
     */
    planAssessment: newPlanAssessment;
}

/**
 * Action creator for updating plan assessment.
 * 
 * @param {PlanAssessment} planAssessment Plan assessment.
 * @returns {UpdatePlanAssessmentPayload} Payload.
 */
export const updatePlanAssessmentAction = (planAssessment: newPlanAssessment): UpdatePlanAssessmentPayload => ({
    type: UPDATE_PLAN_ASSESSMENT,
    planAssessment,
});

/**
 * Thunk for dispatching an action to update plan assessment in the store.
 * 
 * @param {PlanAssessment} planAssessment Plan assessment.
 * @returns {UpdatePlanAssessmentPayload} Payload.
 */
export const updatePlanAssessment = (planAssessment: newPlanAssessment):
    ((dispatch: Dispatch<UpdatePlanAssessmentPayload>) => UpdatePlanAssessmentPayload) => {
    return (dispatch: Dispatch<UpdatePlanAssessmentPayload>): UpdatePlanAssessmentPayload => {
        return dispatch(updatePlanAssessmentAction(planAssessment));
    };
};

/**
 * Type for updating operating context.
 */
 export const UPDATE_OPERATING_CONTEXT = "UpdateOperatingContext";

/**
 * Payload for updating current operating context.
 */
export interface UpdateOperatingContextPayload extends BaseActionPayload {
    operatingContext: OperatingContext;
}

/**
 * Action creator for updating current operating context.
 * 
 * @param {OperatingContext} operatingContext Operating context.
 * @returns {UpdateOperatingContextPayload} Payload.
 */
 export const updateOperatingContextAction =
    (operatingContext: OperatingContext): UpdateOperatingContextPayload => ({
    type: UPDATE_OPERATING_CONTEXT,
    operatingContext,
});

/**
 * Thunk for dispatching an action to update operating context in the store.
 * 
 * @param {OperatingContext} operatingContext Operating context.
 * @returns {UpdateOperatingContextPayload} Payload.
 */
 export const updateOperatingContext = (operatingContext: OperatingContext):
 ((dispatch: Dispatch<UpdateOperatingContextPayload>) => UpdateOperatingContextPayload) => {
 return (dispatch: Dispatch<UpdateOperatingContextPayload>): UpdateOperatingContextPayload => {
     return dispatch(updateOperatingContextAction(operatingContext));
 };
};