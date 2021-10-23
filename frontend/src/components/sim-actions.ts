import { Dispatch } from "redux";
import { Action, OperatingContext } from "../interfaces/sim-store-state";

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
 * Type for updating actions.
 */
 export const UPDATE_ACTIONS = "UpdateActions";

/**
 * Payload for updating latest actions.
 */
export interface UpdateActionsPayload extends BaseActionPayload {
    /**
     * Actions to update with.
     */
    actions: Action[];
}

/**
 * Action creator for updating latest actions.
 * 
 * @param {Action[]} actions Actions.
 * @returns {UpdateActionsPayload} Payload.
 */
export const updateActionsAction = (actions: Action[]): UpdateActionsPayload => ({
    type: UPDATE_ACTIONS,
    actions,
});

/**
 * Thunk for dispatching an action to update actions in the store.
 * 
 * @param {Action[]} actions Actions.
 * @returns {UpdateActionsPayload} Payload.
 */
export const updateActions = (actions: Action[]):
    ((dispatch: Dispatch<UpdateActionsPayload>) => UpdateActionsPayload) => {
    return (dispatch: Dispatch<UpdateActionsPayload>): UpdateActionsPayload => {
        return dispatch(updateActionsAction(actions));
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
    type: UPDATE_ACTIONS,
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