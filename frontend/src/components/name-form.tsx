import React from "react";
import { connect } from "react-redux";

import { Button, FormControl, InputLabel, MenuItem, Select, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField } from '@mui/material';

import { OperatingContext } from "../interfaces/operating-context";
import { SimStoreState } from "../interfaces/sim-store-state";
import { SIM_REDUCER_KEY } from "./sim-reducers";

export interface StoreStateProps {
  /**
   * Current operating context.
   */
  operatingContext: OperatingContext;
}

/**
 * Component props.
 */
export type NameFormProps = StoreStateProps;

export class NameForm extends React.Component<NameFormProps, any> {
    constructor(props: NameFormProps) {
      super(props);
      this.state = {
        targets: 8,
        attackers: 13
      };
  
      this.handleChange = this.handleChange.bind(this);
    }
  
    handleChange(event: any) {
      this.setState({ value: event.target.value });
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
        fetch('http://localhost:5000/GetPlanAssessment', {
            method: 'POST',
            mode: 'cors',
            headers: {
              'Allow': 'application/json',
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(operatingContext)
        })
        .then(res => res.json())
        .then(data => {
            // enter you logic when the fetch is successful
            console.log(data)
        })
        .catch(error => {
            alert("Issue with calling server:" + error)
        });
    }
  
    render() {
      function createData(
        name: string,
        status: string,
      ) {
        return { name, status };
      }
  
      const rows = [
        createData('Ship 1', 'None'),
        createData('Ship 2', 'Disabled'),
        createData('Ship 3', 'Disabled'),
        createData('Ship 4', 'Destroyed'),
        createData('Ship 5', 'Destroyed'),
      ];
      return (
        <div>
          <form>
            <TextField id="outlined-basic" label="Number of targets:" variant="outlined" margin="normal" value={this.state.targets} onChange={this.handleChange} />
            <br />
            <TextField id="outlined-basic" label="Number of attackers:" variant="outlined" margin="normal" value={this.state.attackers} onChange={this.handleChange} />
            <br />
            <Button variant="contained" onClick={() => this.generatePlanAssessment(this.props.operatingContext)}>
              Simulate
            </Button>
          </form>
  
          <TableContainer>
            <Table aria-label="a dense table">
              <TableHead>
                <TableRow>
                  <TableCell>Target</TableCell>
                  <TableCell>Status</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {rows.map((row) => (
                  <TableRow
                    key={row.name}
                  >
                    <TableCell>{row.name}</TableCell>
                    <TableCell>
                      <FormControl fullWidth>
                        <InputLabel id="demo-simple-select-label">Status</InputLabel>
                        <Select
                          labelId="demo-simple-select-label"
                          id="demo-simple-select"
                        >
                          <MenuItem>None</MenuItem>
                          <MenuItem>Disabled</MenuItem>
                          <MenuItem>Destroyed</MenuItem>
                        </Select>
                      </FormControl>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
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
  }
};

export default connect(mapStoreToProps)(NameForm);