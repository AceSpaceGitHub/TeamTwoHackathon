import React from "react";

import { Provider } from "react-redux";
import { createStore, combineReducers, applyMiddleware } from "redux";
import thunk from "redux-thunk";

import "./App.css";

import { SimReducer, SIM_REDUCER_KEY } from "./components/sim-reducers";
import NameForm from "./components/name-form";

const rootReducer = combineReducers({ [SIM_REDUCER_KEY]: SimReducer });
const store = createStore(rootReducer, applyMiddleware(thunk));



class App extends React.Component {
  public render(): React.ReactNode {
    return (
        <Provider store={store}>
          <NameForm/>
        </Provider>
    );
  }
}

export default App;
