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
 * Mapping of targets to time constraints.
 */
 export interface TargetIdToTimeConstraints {
    /**
     * Map entries.
     * Should probably just be a straight map,
     * but just how it turned out when originally working with
     * client/server auto-generators.
     */
    entries: TargetIdToTimeConstraintEntry[];
}

/**
 * Describes squadron and its contents.
 */
export interface Squadron {
    /**
     * Squadron ID.
     */
    id: string;
    /**
     * IDs of remaining jets.
     */
    jetIds: string[];
    /**
     * IDs of remaining pilots.
     */
    pilotIds: string[];
    /**
     * IDs of remaining missiles.
     */
    missileIds: string[];
}

/**
 * Describes carrier and its contents.
 */
export interface Carrier {
    /**
     * Carrier ID.
     */
    id: string;
    /**
     * List of remaining squadrons.
     */
    squadrons: Squadron[];
}

/**
 * Describes friendly forces available.
 */
export interface FriendlyForceLaydown {
    /**
     * List of remaining carriers.
     */
    carriers: Carrier[];
}

/**
 * Operating context of the scenario.
 */
export interface OperatingContext {
    /**
     * Commander's intent for target damage.
     */
    intendedTargetIdToDamage: TargetIdToDamage;
    /**
     * Target time constraints.
     */
    targetTimeConstraints: TargetIdToTimeConstraints;
    /**
     * Minimum number of jets required for a sortie.
     */
    minJetsPerSortie: number;
    /**
     * Friendly force laydown.
     */
    friendlyForces: FriendlyForceLaydown;
}