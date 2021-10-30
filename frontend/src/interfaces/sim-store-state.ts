import { newPlanAssessment } from "./new-store";
import { OperatingContext } from "./operating-context";
/**
 * Shape of the sim store state.
 */
export interface SimStoreState {
    /**
     * Latest captured plan assessment.
     */
    planAssessment: newPlanAssessment | null,
    /**
     * Current operating picture.
     */
    operatingContext: OperatingContext;
};
