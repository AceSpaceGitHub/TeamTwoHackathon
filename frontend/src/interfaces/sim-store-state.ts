import { OperatingContext } from "./operating-context";

/**
 * Shape of the sim store state.
 */
export interface SimStoreState {
    /**
     * Latest results of actions.
     */
    actions: Action[],
    /**
     * Current operating picture.
     */
    operatingContext: OperatingContext;
};
