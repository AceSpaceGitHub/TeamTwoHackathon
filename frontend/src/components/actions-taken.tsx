import {
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableRow,
  } from "@mui/material";
import React from "react";
import { PlanAssessment } from "../interfaces/plan-assessment";
import _ from 'lodash';

export interface ActionsTakenProps{

    planAssessment: PlanAssessment,
}
export interface ActionsTakenState{

}


export class ActionsTaken extends React.Component<ActionsTakenProps, ActionsTakenState> {
  constructor(props: ActionsTakenProps) {
    super(props);
  }

  render(){
    let rows = [];
    let targets = [];
    for(let i = 0; i < this.props.planAssessment.sortieActions.length; i++){
        //rows = [];
        targets = [];
        for(let j = 0; j < this.props.planAssessment.sortieActions[i].missileLoadouts.length; j++){
            targets.push({
                targetId: this.props.planAssessment.sortieActions[i].targetIds[j],
                missiles: this.props.planAssessment.sortieActions[i].missileLoadouts[j]
            });
        }
        rows.push({
            attacks: _.cloneDeep(targets),
            targetState: _.cloneDeep(this.props.planAssessment.resultingStates[i].targetIdToDamage.entries)
        })
    }
    console.log(rows);

    return (
        <div>
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                <TableBody>
                    {
                    rows.map((row) => (
                    <TableRow
                        key={'Action'}
                        sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                    >
                        {row.attacks.map((target) => (
                            <TableCell>Target: {target.targetId}  Missiles: {target.missiles}</TableCell>
                        ))}
                        {row.targetState.map((target) => (
                            <TableCell>ID: {target.id} Damage: {target.damage}</TableCell>
                        ))}
                    </TableRow>
                    ))}
                </TableBody>
                </Table>
            </TableContainer>
        </div>
    );
  }

}