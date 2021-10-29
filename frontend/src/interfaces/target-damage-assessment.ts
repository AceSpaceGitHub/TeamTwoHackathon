import { DamageType } from "../types/damage-type";

/**
 * Entry for mapping targets to damage assessments.
 */
 export interface TargetIdToDamageEntry {
    /**
     * Target ID.
     */
    id: string;
    /**
     * Target damage.
     */
    damage?: DamageType;

    chanceOfSuccess?: number;
}

/**
 * Mapping of targets to damage assessments.
 */
export interface TargetIdToDamage {
    /**
     * Map entries.
     * Should probably just be a straight map,
     * but just how it turned out when originally working with
     * client/server auto-generators.
     */
    entries: TargetIdToDamageEntry[];
}