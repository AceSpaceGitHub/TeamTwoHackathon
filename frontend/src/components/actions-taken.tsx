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

const stateDict = {
    0: 'Unharmed',
    1: 'Disabled',
    2: 'Destroyed'
}

const colorDict = {
    0: 'PaleGreen',
    1: 'Salmon',
    2: 'FireBrick'
}

export class ActionsTaken extends React.Component<ActionsTakenProps, ActionsTakenState> {
  constructor(props: ActionsTakenProps) {
    super(props);
  }

  render(){
    let rows = [];
    let targets = [];
    let prevState : any;
    let newState: any;
    for(let i = 0; i < this.props.planAssessment.sortieActions.length; i++){
        //rows = [];
        targets = [];
        newState = [];
        this.props.planAssessment.resultingStates[i].targetIdToDamage.entries.forEach((target) => {
            newState[target.id] = (target.damage);
        })
        for(let j = 0; j < this.props.planAssessment.sortieActions[i].missileLoadouts.length; j++){
            targets.push({
                targetId: this.props.planAssessment.sortieActions[i].targetIds[j],
                missiles: this.props.planAssessment.sortieActions[i].missileLoadouts[j],
                targetsHit: (prevState ? prevState[this.props.planAssessment.sortieActions[i].targetIds[j]] !== newState[this.props.planAssessment.sortieActions[i].targetIds[j]] : newState[this.props.planAssessment.sortieActions[i].targetIds[j]])
            });
        }
        
        rows.push({
            attacks: _.cloneDeep(targets),
            targetState: _.cloneDeep(this.props.planAssessment.resultingStates[i].targetIdToDamage.entries)
        })
       prevState = newState;

    }
    
    console.log(rows);

    return (
        <div>
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableCell sx={{borderRight:'groove', borderLeft:'groove', borderBottom:'groove'}}>Target 1</TableCell>
                    <TableCell sx={{borderRight:'groove', borderLeft:'groove', borderBottom:'groove'}}>Target 2</TableCell>
                    <TableCell sx={{borderRight:'groove', borderLeft:'groove', borderBottom:'groove'}}>{rows[0].targetState[0].id} State</TableCell>
                    <TableCell sx={{borderRight:'groove', borderLeft:'groove', borderBottom:'groove'}}>{rows[0].targetState[1].id} State</TableCell>
                    <TableCell sx={{borderRight:'groove', borderLeft:'groove', borderBottom:'groove'}}>{rows[0].targetState[2].id} State</TableCell>
                    <TableCell sx={{borderRight:'groove', borderLeft:'groove', borderBottom:'groove'}}>{rows[0].targetState[3].id} State</TableCell>
                    <TableCell sx={{borderRight:'groove', borderLeft:'groove', borderBottom:'groove'}}>{rows[0].targetState[4].id} State</TableCell>
                    <TableCell sx={{borderRight:'groove', borderLeft:'groove', borderBottom:'groove'}}>{rows[0].targetState[5].id} State</TableCell>
                    <TableBody>
                        {
                        rows.map((row) => (
                        <TableRow
                            key={'Action'}
                            sx={{ "&:last-child td, &:last-child th": { backgroundColor:'#353839', borderRight: 'groove', borderLeft:'groove' } }}
                        >
                            {row.attacks.map((target) => (
                                <TableCell sx={{backgroundColor: '#353839',borderRight:'groove', borderLeft:'groove'}}>Target: {target.targetId}{<br></br>}Missiles: {target.missiles}{<br></br>}{target.targetsHit ? 'Hit Target' : 'Missed Target'}</TableCell>
                            ))}
                            {row.targetState.map((target) => (
                                <TableCell sx={{backgroundColor:'#353839', borderRight:'groove', borderLeft:'groove'}}>ID: {target.id} Damage: {stateDict[target.damage]}</TableCell>
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