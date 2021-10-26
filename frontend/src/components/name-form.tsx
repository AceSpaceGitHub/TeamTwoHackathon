import React from "react";
import { connect } from "react-redux";

import {
  Button,
  FormControl,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
} from "@mui/material";

import { OperatingContext } from "../interfaces/operating-context";
import { SimStoreState } from "../interfaces/sim-store-state";
import { SIM_REDUCER_KEY } from "./sim-reducers";
import { PlanAssessment } from "../interfaces/plan-assessment";
import { updatePlanAssessment } from "./sim-actions";
import { DamageType } from "../types/damage-type";
import { ActionsTaken } from "./actions-taken";
const sampleData = require('../test-data/getPlanAssessmentResponse.json');

interface NameState {
  numShips: number,
  numJets: number,
  numPilots: number,
  missiles: number,
  ships: {name:string, damage: DamageType}[]
}

export interface StoreStateProps {
  /**
   * Current operating context.
   */
  operatingContext: OperatingContext;

  /**
   * Current plan assessment.
   */
  planAssessment: PlanAssessment | null;
}

export interface DispatchProps {
  /**
   * Updates latest plan assessment.
   *
   * @param {PlanAssessment} planAssessment Plan assessment.
   */
  updatePlanAssessment: (planAssessment: PlanAssessment) => void;
}

/**
 * Component props.
 */
export type NameFormProps = StoreStateProps & DispatchProps;

export class NameForm extends React.Component<NameFormProps, NameState> {
  constructor(props: NameFormProps) {
    super(props);
    this.state = {
      numShips:6,
      numJets:0,
      numPilots:0,
      missiles: 0,
      ships: [],
    };

    this.handleTextChange = this.handleTextChange.bind(this);
  }

  handleTextChange(event: any) {
    this.setState({ missiles: +event.target.value });
  }

  createData(name: string, damage: string) {
    return { name, damage };
  }

  componentDidMount(){
    if(this.state.numShips !== this.state.ships.length){
      let newShips = this.state.ships;
      for(let i = 0; i < this.state.numShips; i++){
        newShips[i] = this.state.ships[i] ?? {name:`Ship ${i+1}`, damage: DamageType.Untouched};
      }
      newShips = newShips.slice(0,this.state.numShips);
      this.setState({ships: newShips});
    }
  }

  componentDidUpdate(){
    if(this.state.numShips !== this.state.ships.length){
      let newShips = this.state.ships;
      for(let i = 0; i < this.state.numShips; i++){
        newShips[i] = this.state.ships[i] ?? {name:`Ship ${i+1}`, damage: DamageType.Untouched};
      }
      newShips = newShips.slice(0,this.state.numShips);
      this.setState({ships: newShips});
    }
  }

  /**
   * Pop off a call to the backend to generate a new plan assessment.
   *
   * @param {OperatingContext} operatingContext Operating context.
   */
  generatePlanAssessment(operatingContext: OperatingContext) {
    // Think this is "supposed" to be hidden inside a client interface
    // that is then called inside a store action.
    // Not sure this is gonna be a huge point of contention.
    fetch("http://localhost:5000/GetPlanAssessment", {
      method: "POST",
      mode: "cors",
      headers: {
        Allow: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(operatingContext),
    })
      .then((res) => res.json())
      .then((data) => {
        const planAssessment = data as PlanAssessment;
        this.props.updatePlanAssessment(planAssessment);
      })
      .catch((error) => {
        alert("Issue with calling server:" + error);
      });
  }

  render() {

    //Plug this missilesNum array into
    //line `{ships.map((row) => (` to dynamically update table rows
    const missilesNum: string[] = [];
    for (let k = 0; k < Number(this.state.missiles); k++) {
      var displayVal = k + 1;
      missilesNum[k] = "Ship " + displayVal;
    }
    //const plan = JSON.parse(sampleData)
    console.log(sampleData)
    if(sampleData){
      return(
        <ActionsTaken planAssessment={sampleData as PlanAssessment}/>
      )
    }

    return (
      <div>
        <TextField
          id="outlined-basic"
          label="Number of missiles:"
          variant="outlined"
          margin="normal"
          type="number"
          value={this.state.missiles}
          InputLabelProps={{ shrink: true }}
          onChange={this.handleTextChange}
        />
        <TextField
            id="outlined-basic"
            label="Number of ships:"
            variant="outlined"
            margin="normal"
            type="number"
            value={6/*this.state.numShips*/}
            InputLabelProps={{ shrink: true }}
            onChange={(value) => {
              //this.setState({numShips: +value.target.value})
            }}
          />
        <TextField
            id="outlined-basic"
            label="Number of jets:"
            variant="outlined"
            margin="normal"
            type="number"
            value={this.state.numJets}
            InputLabelProps={{ shrink: true }}
            onChange={(value) => {
              this.setState({numJets: +value.target.value})
            }}
          />
        <TextField
            id="outlined-basic"
            label="Number of pilots:"
            variant="outlined"
            margin="normal"
            type="number"
            value={this.state.numPilots}
            InputLabelProps={{ shrink: true }}
            onChange={(value) => {
              this.setState({numPilots: +value.target.value})
            }}
          />

        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableBody>
              {this.state.ships.map((row) => (
                <TableRow
                  key={row.name}
                  sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                >
                  <TableCell>{row.name}</TableCell>
                  <TableCell>
                    <FormControl sx={{float: 'right', minWidth:'300px'}}>
                      <InputLabel id="demo-simple-select-label">
                        Status
                      </InputLabel>
                      <Select
                        value={row.damage}
                        labelId="demo-simple-select-label"
                        onChange={(value) => {
                          const ships = this.state.ships;
                          if(ships !== undefined){
                            ships.find((name) => { if(name.name === row.name) name.damage = value.target.value as DamageType})
                          }
                          this.setState({ships: ships});
                        }}
                        id="demo-simple-select"
                      >
                        <MenuItem value={DamageType.Untouched}>Untouched</MenuItem>
                        <MenuItem value={DamageType.Disabled}>Disabled</MenuItem>
                        <MenuItem value={DamageType.Destroyed}>Destroyed</MenuItem>
                      </Select>
                    </FormControl>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <br />
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableBody>
              {this.state.ships.map((row) => (
                <TableRow
                  key={row.name}
                  sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                >
                  <TableCell component="th" scope="row">
                    {row.name}
                  </TableCell>
                  {/* Was last trying to get this to work. Current implementation does not work */}
                  {this.state.ships.forEach((element) => {
                    if (element.name !== row.name) {
                      var labelString =
                        "Percent to protect " + element.name + ":";
                      {
                        <TableCell>
                          <TextField
                            label="percentage to protect"
                            variant="outlined"
                            type="number"
                            InputLabelProps={{ shrink: true }}
                          />
                        </TableCell>;
                      }
                    }
                  })}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <br />
        <Button
          variant="contained"
          onClick={() => {
            alert(this.state.missiles + " missiles");
          }}
        >
          Simulate
        </Button>
      </div>
    );
  }
}

/**
 * Maps store state to component props.
 *
 * @param {SimStoreState} state Store state.
 * @returns {StoreStateProps} Store state props.
 */
const mapStoreToProps = (state: {
  [SIM_REDUCER_KEY]: SimStoreState;
}): StoreStateProps => {
  return {
    operatingContext: state[SIM_REDUCER_KEY].operatingContext,
    planAssessment:state[SIM_REDUCER_KEY].planAssessment,
  };
};

/**
 * Maps store dispatches to component props.
 *
 * @param {any} dispatch Dispatch object.
 * @returns {DispatchProps} Store dispatch props.
 */
const mapDispatchToProps = (dispatch: any): DispatchProps => {
  return {
    updatePlanAssessment: (planAssessment: PlanAssessment): void =>
      dispatch(updatePlanAssessment(planAssessment)),
  };
};

export default connect(mapStoreToProps, mapDispatchToProps)(NameForm);
