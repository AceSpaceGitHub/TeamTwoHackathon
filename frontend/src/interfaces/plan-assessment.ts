import { TargetIdToDamage } from "./target-damage-assessment";

/**
 * Describes what the sortie's goal is
 * for a particular step in the prediction.
 */
export interface SortieAction {
    /**
     * ID of targetted entities in this sortie.
     */
     targetIds: string[];
     /**
      * Missile count per target.
      * Expected to be same size as target IDs,
      * so this is a parallel array to that.
      */
     missileLoadouts: number[];
}

/**
 * Describes preducted state of the world
 * after a sortie is carried out.
 */
export interface SortieState {
    /**
     * Missile count.
     */
    numMissiles: number;
    /**
     * Jet count.
     */
    numJets: number;
    /**
     * Pilot count.
     */
    numPilots: number;
    /**
     * Target ID to its damage assessment at this state.
     */
    targetIdToDamage: TargetIdToDamage;
}

/**
 * Whatever response we expect to get back from the server,
 * so the name is kept vague.
 * 
 * At the moment, this is what we'd get from the RL prediction.
 */
export interface PlanAssessment {
    /**
     * Sortie actions/intents.
     */
    sortieActions: SortieAction[];
    /**
     * Sortie state after action is taken.
     * Expected to be same size as sortie actions,
      * so this is a parallel array to that.
     */
    resultingStates: SortieState[];
}