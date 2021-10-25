import React from "react";

import { Button, FormControl, InputLabel, MenuItem, Select, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField } from '@mui/material';

// Would like test-data to be in common area outside frontend/backend,
// but React app doesn't allow imports outside its src area.
import cannedRequestJson from '../test-data/getPlanAssessmentRequest.json';

export class NameForm extends React.Component<any, any> {
    constructor(props: any) {
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
            <Button variant="contained" onClick={() => { 
              alert(this.state.targets + ' targets and ' + this.state.attackers + ' attackers')
  
              fetch('http://localhost:5000/GetPlanAssessment', {
                method: 'POST',
                mode: 'cors',
                headers: {
                  'Allow': 'application/json',
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify(cannedRequestJson)
              })
                .then(res => res.json())
                .then(data => {
                // enter you logic when the fetch is successful
                  console.log(data)
                })
                .catch(error => {
                // enter your logic for when there is an error (ex. error toast)
                console.log(error)
                })
            }
            }>Sumulate</Button>
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

export default NameForm;