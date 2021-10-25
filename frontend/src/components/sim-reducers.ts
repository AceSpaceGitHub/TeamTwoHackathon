import producer from 'immer';
import { WritableDraft } from 'immer/dist/internal';

import { SimStoreState } from "../interfaces/sim-store-state";
import { BaseActionPayload, UpdateOperatingContextPayload, UpdatePlanAssessmentPayload, UPDATE_OPERATING_CONTEXT, UPDATE_PLAN_ASSESSMENT } from "./sim-actions";

// Would like test-data to be in common area outside frontend/backend,
// but React app doesn't allow imports outside its src area.
import cannedRequestJson from '../test-data/getPlanAssessmentRequest.json';

/**
 * Sim reducer key.
 */
export const SIM_REDUCER_KEY = "SimReducer";

/**
 * Initial store state.
 */
export const initialSimStoreState: SimStoreState = {
    planAssessment: null,
    operatingContext: cannedRequestJson.body,
};

/**
 * Reducer for the sim store.
 * 
 * @param {SimStoreState} state Previous state.
 * @param {BaseActionPayload} action Action payload.
 * @returns {SimStoreState} Next state.
 */
export const SimReducer = (
    state: SimStoreState = initialSimStoreState,
    action: BaseActionPayload = { type: 'NoActionType' },
): SimStoreState => {
    return producer(state, (draft) => {
        switch (action.type) {
            case UPDATE_OPERATING_CONTEXT: {
                handleUpdateOperatingContext(draft, action as UpdateOperatingContextPayload)
                break;
            }
            case UPDATE_PLAN_ASSESSMENT: {
                handleUpdatePlanAssessment(draft, action as UpdatePlanAssessmentPayload)
                break;
            }
            default: {
                break;
            }
        }
    });
}

/**
 * Handles update operating context payload.
 * 
 * @param {WritableDraft<SimStoreState>} draft Current draft state of store.
 * @param {UpdateOperatingContextPayload} payload Payload.
 */
const handleUpdateOperatingContext = (draft: WritableDraft<SimStoreState>, payload: UpdateOperatingContextPayload) : void => {
    draft.operatingContext = payload.operatingContext;
}

/**
 * Handles update plan assessment payload.
 * 
 * @param {WritableDraft<SimStoreState>} draft Current draft state of store.
 * @param {UpdatePlanAssessmentPayload} payload Payload.
 */
 const handleUpdatePlanAssessment = (draft: WritableDraft<SimStoreState>, payload: UpdatePlanAssessmentPayload): void => {
    draft.planAssessment = payload.planAssessment;
}