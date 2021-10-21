// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('@grpc/grpc-js');
var agent_pb = require('./agent_pb.js');

function serialize_agent_OperatingPicture(arg) {
  if (!(arg instanceof agent_pb.OperatingPicture)) {
    throw new Error('Expected argument of type agent.OperatingPicture');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_agent_OperatingPicture(buffer_arg) {
  return agent_pb.OperatingPicture.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_agent_PlanAssessment(arg) {
  if (!(arg instanceof agent_pb.PlanAssessment)) {
    throw new Error('Expected argument of type agent.PlanAssessment');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_agent_PlanAssessment(buffer_arg) {
  return agent_pb.PlanAssessment.deserializeBinary(new Uint8Array(buffer_arg));
}


// Interface for talking to the trained agent.
var AgentService = exports.AgentService = {
  // Gets a new plan/assessment from the agent.
getPlanAssessment: {
    path: '/agent.Agent/GetPlanAssessment',
    requestStream: false,
    responseStream: false,
    requestType: agent_pb.OperatingPicture,
    responseType: agent_pb.PlanAssessment,
    requestSerialize: serialize_agent_OperatingPicture,
    requestDeserialize: deserialize_agent_OperatingPicture,
    responseSerialize: serialize_agent_PlanAssessment,
    responseDeserialize: deserialize_agent_PlanAssessment,
  },
};

exports.AgentClient = grpc.makeGenericClientConstructor(AgentService);
