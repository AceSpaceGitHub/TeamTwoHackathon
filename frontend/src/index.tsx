import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { createTheme, CssBaseline, ThemeProvider } from '@mui/material';

document.title = "Team Two AI Sim";

const theme = createTheme({
  palette: {
    mode:'dark'
  }
});

ReactDOM.render(
  <ThemeProvider theme={theme}>
    <CssBaseline>
      <React.StrictMode>
        <App />
      </React.StrictMode>
    </CssBaseline>
  </ThemeProvider>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
