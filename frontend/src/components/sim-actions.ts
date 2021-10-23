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
 * Type for updating operating context.
 */
 export const UPDATE_OPERATING_CONTEXT = "UpdateOperatingContext";

/**
 * Payload for updating current operating context.
 */
export interface UpdateOperatingContextPayload extends BaseActionPayload {
    operatingContext: OperatingContext;
}