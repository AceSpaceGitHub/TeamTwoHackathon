import { ActionType } from "../types/action-type";
import { DamageType } from "../types/damage-type";

/**
 * Action projected by the sim.
 */
export interface Action {
    /**
     * Action type.
     */
    actionType: ActionType,
    /**
     * ID of target action was taken against (if any).
     */
    targetId?: string,
};

/**
 * Mapping of targets to damage assessments.
 */
export interface TargetIdToDamage {
    [targetId: string] : DamageType;
}

/**
 * Operating context of the scenario.
 */
export interface OperatingContext {
    /**
     * Current number of missiles.
     */
    numMissiles: number;
    /**
     * Commander's intent for targets.
     */
    intendedTargetDamage: TargetIdToDamage;
}

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
