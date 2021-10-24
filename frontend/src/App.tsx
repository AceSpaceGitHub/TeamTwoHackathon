import React from "react";
import "./App.css";
import ReactDOM from "react-dom";
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
  TableRow,
  TextField,
} from "@mui/material";

class NameForm extends React.Component<any, any> {
  constructor(props: any) {
    super(props);
    this.state = {
      missiles: "",
    };

    this.handleTextChange = this.handleTextChange.bind(this);
  }

  handleTextChange(event: any) {
    this.setState({ missiles: event.target.value });
  }

  // handleSelectChange(event: any) {
  //   this.setState((prevState: { shipDamage: any }) => ({
  //     shipDamage: [...prevState.shipDamage, event.target.value],
  //   }));
  // }

  render() {
    function createData(name: string, damage: string) {
      return { name, damage };
    }

    const ships = [
      createData("Ship 1", ""),
      createData("Ship 2", ""),
      createData("Ship 3", ""),
      createData("Ship 4", ""),
      createData("Ship 5", ""),
    ];

    //Plug this missilesNum array into
    //line `{ships.map((row) => (` to dynamically update table rows
    const missilesNum: string[] = [];
    for (let k = 0; k < Number(this.state.missiles); k++) {
      var displayVal = k + 1;
      missilesNum[k] = "Ship " + displayVal;
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

        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableBody>
              {ships.map((row) => (
                <TableRow
                  key={row.name}
                  sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                >
                  <TableCell component="th" scope="row">
                    {row.name}
                  </TableCell>
                  <TableCell>
                    <FormControl fullWidth>
                      <InputLabel id="demo-simple-select-label">
                        Status
                      </InputLabel>
                      <Select
                        value={row.damage}
                        labelId="demo-simple-select-label"
                        // onChange={this.handleSelectChange}
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
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableBody>
              {ships.map((row) => (
                <TableRow
                  key={row.name}
                  sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                >
                  <TableCell component="th" scope="row">
                    {row.name}
                  </TableCell>
                  {ships.forEach((element) => {
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

ReactDOM.render(<NameForm />, document.getElementById("root"));

export default NameForm;
