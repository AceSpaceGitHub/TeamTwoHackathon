import {
    Container,
    List,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableRow,
  } from "@mui/material";
import React from "react";
import _ from 'lodash';
import heloImage from '../helo.jpg';
import sortieImage from '../jet.jpg'
import { actionType, newPlanAssessment } from "../interfaces/new-store";

export interface ActionsTakenProps{

    planAssessment: newPlanAssessment,
}
export interface ActionsTakenState{

}

const stateDict = {
    0: 'Unharmed',
    1: 'Disabled',
    2: 'Destroyed'
}

export class ActionsTaken extends React.Component<ActionsTakenProps, ActionsTakenState> {
  constructor(props: ActionsTakenProps) {
    super(props);
  }

    getArrayString(array: string[]){
        let string = '';
        for(let i = 0; i < array.length; i++){
            string += (array[i] + ' ');
            if(i === array.length -2) string += 'and ';
        }
        return string;
    }
    getAttackString(jets: string[],missiles: number[], personnel:string[]){
        let string = '';
        for(let i = 0; i < jets.length; i++){
            string += `${jets[i]} piloted by ${personnel[i]}, equipped with ${missiles[i]} ${missiles[i] === 1 ? 'missile' : 'missiles'}, `
            if(i === jets.length -2) string += 'and ';
        }
        return string;
    }

    getHeloString(helos: string[],personnel:string[]){
        let string = '';
        for(let i = 0; i < helos.length; i++){
            string += `${helos[i]} piloted by ${personnel[i]}, `
            if(i === helos.length -2) string += 'and ';
        }
        return string;
    }

  render(){
    let rows = [];
    let targets = [];
    let prevState : any;
    let newState: any;
    /*for(let i = 0; i < this.props.planAssessment.sortieActions.length; i++){
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

    }*/
    

    return (
        <div style={{display:'-webkit-box', overflowX:'hidden'}}>
            <List>
                {this.props.planAssessment.resultingActions.map((action) => (
                <Container sx={{height:'150px', marginLeft:'5%', marginBottom:'2%', marginRight:'5%', backgroundColor:'#353839', width:'auto'}}>
                    <Container sx={{position: 'absolute', margin:'5px', width:'250px', height:'140px', backgroundImage:`url(${action.type === actionType.Helo ? heloImage : sortieImage})`}}></Container>
                    <Container sx={{marginLeft:'260px', overflow:'normal', width:'auto'}}>
                        <div>
                            <p style={{fontSize:'18px'}}>
                                <b>{action.type === actionType.Helo ? 'Helo Launch' : 'Sortie Launch'}</b><br></br>
                            </p>
                            <p style={{fontSize:'14px'}}>
                                {action.type === actionType.Helo ? this.getHeloString(action.involvedVehicles, action.involvedPersonelle) : this.getAttackString(action.involvedVehicles,action.numberOfMissiles, action.involvedPersonelle)} took off from {action.departingCarrier}.<br></br>
                                {action.type === actionType.Sortie ? `Targeted Ships : ${this.getArrayString(action.targetList)}`:''}<br></br>
                                Time Departed: {action.startTime}<br></br>
                                Time Returned: {action.endTime}
                            </p>
                        </div>
                    </Container>
                </Container>
                ))}
            </List>
        </div>
    );
  }
/*<TableContainer component={Paper}>
                <Table sx={{ minWidth: 650, maxHeight:'100px' }} aria-label="simple table">
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
            </TableContainer>*/
}