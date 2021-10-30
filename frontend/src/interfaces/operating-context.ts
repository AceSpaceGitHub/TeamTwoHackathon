import { TargetIdToDamage } from "./target-damage-assessment";

/**
 * Entry for mapping targets to time constraints.
 */
 export interface TargetIdToTimeConstraintEntry {
    /**
     * Target ID.
     */
    id: string;
    /**
     * Max sortie time (hours).
     */
    maxSortieTimeHours: number;
}

/**
 * Operating context of the scenario.
 */
export interface OperatingContext {
    numJets: number,
    numPilots: number,
    numMissiles: number,
    intendedTargetIdToDamage: TargetIdToDamage
}