import producer from 'immer';

import { SimStoreState } from "../interfaces/sim-store-state";
import { BaseActionPayload, UPDATE_ACTIONS, UPDATE_OPERATING_CONTEXT } from "./sim-actions";

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
                break;
            }
            case UPDATE_OPERATING_CONTEXT: {
                break;
            }
        }
    });
}