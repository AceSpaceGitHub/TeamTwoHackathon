import React from 'react';
import './App.css';
import ReactDOM from 'react-dom';
import { Button, FormControl, InputLabel, MenuItem, Paper, Select, Table, TableBody, TableCell, TableContainer, TableRow, TextField } from '@mui/material';

class NameForm extends React.Component<any, any> {
  constructor(props: any) {
    super(props);
    this.state = {
      missiles: ''
    };

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event: any) {
    this.setState({ missiles: event.target.value });
  }

  render() {
    //Plug this missilesNum array into this line `{ships.map((row) => (` to dynamically update table rows
    const missilesNum: string[] = [];
    for (let k = 0; k < Number(this.state.missiles); k++) {
      var displayVal = k + 1
      missilesNum[k] = 'Ship ' + displayVal
    }

    const ships = ['Ship 1', 'Ship 2', 'Ship 3', 'Ship 4', 'Ship 5', 'Ship 6']
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
          onChange={this.handleChange}
        />

        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableBody>
              {ships.map((row) => (
                <TableRow
                  key={row}
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell component="th" scope="row">
                    {row}
                  </TableCell>
                  <TableCell>
                    <FormControl fullWidth>
                      <InputLabel id="demo-simple-select-label">Status</InputLabel>
                      <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                      >
                        <MenuItem>No Damage</MenuItem>
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
        <br />
        <Button variant="contained" onClick={() => { alert(this.state.missiles + ' missiles') }}>Simulate</Button>
      </div>
    );
  }
}

ReactDOM.render(
  <NameForm />,
  document.getElementById('root')
);

export default NameForm;