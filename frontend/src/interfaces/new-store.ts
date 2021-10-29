import { TargetIdToDamage } from "./target-damage-assessment";

export enum actionType{
    Helo,
    Sortie
}

export interface resultState{
    targetState: TargetIdToDamage;
    missilesRemaining: number;
    peopleRemaining: number;
    vehiclesRemaining: number;

}

export interface action{

    type : actionType;
    targetList: string[];
    involvedVehicles: string[];
    departingCarrier: string;
    involvedPersonelle: string[];
    numberOfMissiles: number[];
    startTime: string;
    endTime: string;

}

export interface newPlanAssessment {

    resultingActions: action[];

    resultingState: resultState;
}
