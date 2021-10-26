import { OperatingContext } from "./operating-context";
import { PlanAssessment } from "./plan-assessment";

/**
 * Shape of the sim store state.
 */
export interface SimStoreState {
    /**
     * Latest captured plan assessment.
     */
    planAssessment: PlanAssessment | null,
    /**
     * Current operating picture.
     */
    operatingContext: OperatingContext;
};
