import React from "react";
import { connect } from "react-redux";

import {
  FormControl,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  TextField,
} from "@mui/material";

import { OperatingContext } from "../interfaces/operating-context";
import { SimStoreState } from "../interfaces/sim-store-state";
import { SIM_REDUCER_KEY } from "./sim-reducers";
import { updatePlanAssessment } from "./sim-actions";
import { DamageType } from "../types/damage-type";
import { ActionsTaken } from "./actions-taken";
import _, { initial } from "lodash";
import { newPlanAssessment } from "../interfaces/new-store";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import LoadingButton from "@mui/lab/LoadingButton";
import { TargetIdToDamage } from "../interfaces/target-damage-assessment";


enum page {
  INITIAL,
  SIMULATING,
  RESULTS
}

const shipNames = ['Enemy Carrier A', 'Enemy Carrier B', 'Enemy Destroyer A', 'Enemy Destroyer B', 'Enemy Cruiser A', 'Enemy Cruiser B'];

interface NameState {
  numShips: number,
  numJets: number,
  numPilots: number,
  missiles: number,
  ships: {name:string, damage: DamageType}[],
  page: page;
  loading: boolean;
  planAssessment: newPlanAssessment | null;
}

const stateDict = {
  0: 'Unharmed',
  1: 'Disabled',
  2: 'Destroyed'
}

export interface StoreStateProps {
  /**
   * Current operating context.
   */
  operatingContext: OperatingContext;

  /**
   * Current plan assessment.
   */
  //planAssessment: newPlanAssessment | null;

  
}

export interface DispatchProps {
  /**
   * Updates latest plan assessment.
   *
   * @param {PlanAssessment} planAssessment Plan assessment.
   */
  updatePlanAssessment: (planAssessment: newPlanAssessment) => void;
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
      page: page.INITIAL,
      loading: false,
      planAssessment: null,
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
        newShips[i] = this.state.ships[i] ?? {name:shipNames[i], damage: DamageType.Unharmed};
      }
      newShips = newShips.slice(0,this.state.numShips);
      this.setState({ships: newShips});
    }
  }

  componentDidUpdate(){
    if(this.state.numShips !== this.state.ships.length){
      let newShips = this.state.ships;
      for(let i = 0; i < this.state.numShips; i++){
        newShips[i] = this.state.ships[i] ?? {name:shipNames[i], damage: DamageType.Unharmed};
      }
      newShips = newShips.slice(0,this.state.numShips);
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
        const planAssessment = data as newPlanAssessment;
        this.setState({ planAssessment:planAssessment, page: page.RESULTS, loading:false })
        //this.props.updatePlanAssessment(planAssessment);
      })
      .catch((error) => {
        alert("Issue with calling server:" + error);
      });
  }

  getMainPage(){
    switch(this.state.page){
      case page.INITIAL:
        return(
          <TableContainer sx={{height:'100vh', width: '80%'}}>
            <LoadingButton
            sx={{top:'40%', left:'40%'}}
              variant="contained"
              onClick={() => {
                let input : OperatingContext;
                this.setState({loading: true});
                let targetList : TargetIdToDamage = {entries:[]};
                this.state.ships.forEach((ship) => {
                  targetList.entries.push({id: ship.name, damage:ship.damage});
                })
                input = {
                  numJets: this.state.numJets,
                  numPilots: this.state.numPilots,
                  numMissiles: this.state.missiles,
                  intendedTargetIdToDamage:targetList,
                }
                this.generatePlanAssessment(input);
                //setTimeout(() => this.setState({ page: page.RESULTS }), 7000);
              }}
              endIcon={<PlayArrowIcon />}
              loadingPosition="end"
              loading={this.state.loading}
            >
              Simulate
            </LoadingButton>
          </TableContainer>
        );
      case page.RESULTS:
        if(!this.state.planAssessment) return (<></>);
        return(
          <div style={{display:'flex', overflowX:'hidden'}}>
            <TableContainer sx={{ width: '40vh', height:'fit-content'}} component={Paper}>
              <TextField
                sx={{marginLeft:'10%'}}
                id="outlined-basic"
                label="Number of missiles remaining:"
                variant="outlined"
                margin="normal"
                type="string"
                value={this.state.planAssessment?.resultingState.missilesRemaining}
                InputLabelProps={{ shrink: true }}
              />
              <TextField
                  sx={{marginLeft:'10%'}}
                  id="outlined-basic"
                  label="Number of jets remaining:"
                  variant="outlined"
                  margin="normal"
                  type="string"
                  value={this.state.planAssessment?.resultingState.vehiclesRemaining}
                  InputLabelProps={{ shrink: true }}
                />
              <TextField
                  sx={{marginLeft:'10%'}}
                  id="outlined-basic"
                  label="Number of pilots survived:"
                  variant="outlined"
                  margin="normal"
                  type="string"
                  value={this.state.planAssessment?.resultingState.peopleRemaining}
                  InputLabelProps={{ shrink: true }}
                />
              <Table sx={{ }} aria-label="simple table">
                <TableBody>
                  {this.state.planAssessment?.resultingState.targetState.entries.map((target) => (
                    <TableRow
                      key={target.id}
                      sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                    >
                      <TableCell>{target.id}</TableCell>
                      <TableCell>
                        <FormControl sx={{float: 'right', maxWidth:'150px'}}>
                          <TextField
                            value={target.chanceOfSuccess ?? 0}
                            label={`Probability of success`}
                            id="demo-simple-select"
                          />
                        </FormControl>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
            <TableContainer sx={{height: '100vh', display:'contents', overflowY:'scroll'}}>
              <ActionsTaken planAssessment={this.state.planAssessment as newPlanAssessment}/>
            </TableContainer>
          </div>
        )
        break;
      case page.SIMULATING:
        break;
    }
    
  }

  render() {

    //Plug this missilesNum array into
    //line `{ships.map((row) => (` to dynamically update table rows
    const missilesNum: string[] = [];
    for (let k = 0; k < Number(this.state.missiles); k++) {
      var displayVal = k + 1;
      missilesNum[k] = "Ship " + displayVal;
    }

    return (
      <div style={{
        backgroundImage: "url(../../img/image.jpg)",
        backgroundRepeat: "no-repeat",
        backgroundSize: "cover",
        backgroundPosition: "top",
      }}>
        

        <TableContainer sx={{float:'left', width: '40vh', height:'fit-content'}} component={Paper}>
          <TextField
            sx={{marginLeft:'10%'}}
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
              sx={{marginLeft:'10%'}}
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
              sx={{marginLeft:'10%'}}
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
          <Table sx={{ }} aria-label="simple table">
            <TableBody>
              {this.state.ships.map((row) => (
                <TableRow
                  key={row.name}
                  sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                >
                  <TableCell>{row.name}</TableCell>
                  <TableCell>
                    <FormControl sx={{float: 'right', maxWidth:'150px'}}>
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
                        <MenuItem value={DamageType.Unharmed}>Unharmed</MenuItem>
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
        {this.getMainPage()}
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
    //planAssessment:state[SIM_REDUCER_KEY].planAssessment,
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
    updatePlanAssessment: (planAssessment: newPlanAssessment): void =>
      dispatch(updatePlanAssessment(planAssessment)),
  };
};

export default connect(mapStoreToProps, mapDispatchToProps)(NameForm);
