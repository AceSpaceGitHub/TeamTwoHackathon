import producer from 'immer';
import { WritableDraft } from 'immer/dist/internal';

import { SimStoreState } from "../interfaces/sim-store-state";
import { BaseActionPayload, UpdateActionsPayload, UpdateOperatingContextPayload, UPDATE_ACTIONS, UPDATE_OPERATING_CONTEXT } from "./sim-actions";

/**
 * Sim reducer key.
 */
export const SIM_REDUCER_KEY = "SimReducer";

/**
 * Initial store state.
 */
export const initialSimStoreState: SimStoreState = {
    actions: [],
    operatingContext: {
        numMissiles: 0,
        intendedTargetDamage: {},
    }
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
            case UPDATE_ACTIONS: {
                handleUpdateActions(draft, action as UpdateActionsPayload)
                break;
            }
            case UPDATE_OPERATING_CONTEXT: {
                handleUpdateOperatingContext(draft, action as UpdateOperatingContextPayload)
                break;
            }
            default: {
                break;
            }
        }
    });
}

/**
 * Handles update actions payload.
 * 
 * @param {WritableDraft<SimStoreState>} draft Current draft state of store.
 * @param {UpdateActionsPayload} payload Payload.
 */
const handleUpdateActions = (draft: WritableDraft<SimStoreState>, payload: UpdateActionsPayload): void => {
    draft.actions = payload.actions;
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