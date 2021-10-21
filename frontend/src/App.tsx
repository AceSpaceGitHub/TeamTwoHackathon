import React from 'react';
import logo from './logo.svg';
import './App.css';

import * as grpc from "@grpc/grpc-js";

import { OperatingPicture, TargetIdToDamageEntry, TargetToDamageMap } from "./agent-client/agent_pb";
import { AgentClient } from "./agent-client/agent_grpc_pb";

const client = new AgentClient(
  "localhost:50051",
  grpc.credentials.createInsecure()
);

const request = new OperatingPicture();
request.setNummissiles(50);

const targetIdToDamage = new TargetToDamageMap();

const carrierA = new TargetIdToDamageEntry();
carrierA.setId('CarrierA');
carrierA.setDamage(1);
targetIdToDamage.addEntries(carrierA, 0);

const carrierB = new TargetIdToDamageEntry();
carrierB.setId('CarrierB');
carrierB.setDamage(2);
targetIdToDamage.addEntries(carrierB, 1);

const destroyerA = new TargetIdToDamageEntry();
destroyerA.setId('DestroyerA');
destroyerA.setDamage(1);
targetIdToDamage.addEntries(destroyerA, 2);

const destroyerB = new TargetIdToDamageEntry();
destroyerB.setId('DestroyerB');
destroyerB.setDamage(2);
targetIdToDamage.addEntries(destroyerB, 3);

const cruiserA = new TargetIdToDamageEntry();
cruiserA.setId('CruiserA');
cruiserA.setDamage(0);
targetIdToDamage.addEntries(cruiserA, 4);

const cruiserB = new TargetIdToDamageEntry();
cruiserB.setId('CruiserB');
cruiserB.setDamage(1);
targetIdToDamage.addEntries(cruiserB, 5);

request.setTargetidtodamage();

client.getPlanAssessment(request, (error, response) => {
  if(!error) {
    console.info("Response:", response.getActionassessmentsList());
  } else {
    console.error("Error:", error.message); 
  }
});

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
