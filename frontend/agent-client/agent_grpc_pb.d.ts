// package: agent
// file: agent.proto

/* tslint:disable */
/* eslint-disable */

import * as grpc from "@grpc/grpc-js";
import * as agent_pb from "./agent_pb";

interface IAgentService extends grpc.ServiceDefinition<grpc.UntypedServiceImplementation> {
    getPlanAssessment: IAgentService_IGetPlanAssessment;
}

interface IAgentService_IGetPlanAssessment extends grpc.MethodDefinition<agent_pb.OperatingPicture, agent_pb.PlanAssessment> {
    path: "/agent.Agent/GetPlanAssessment";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<agent_pb.OperatingPicture>;
    requestDeserialize: grpc.deserialize<agent_pb.OperatingPicture>;
    responseSerialize: grpc.serialize<agent_pb.PlanAssessment>;
    responseDeserialize: grpc.deserialize<agent_pb.PlanAssessment>;
}

export const AgentService: IAgentService;

export interface IAgentServer extends grpc.UntypedServiceImplementation {
    getPlanAssessment: grpc.handleUnaryCall<agent_pb.OperatingPicture, agent_pb.PlanAssessment>;
}

export interface IAgentClient {
    getPlanAssessment(request: agent_pb.OperatingPicture, callback: (error: grpc.ServiceError | null, response: agent_pb.PlanAssessment) => void): grpc.ClientUnaryCall;
    getPlanAssessment(request: agent_pb.OperatingPicture, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: agent_pb.PlanAssessment) => void): grpc.ClientUnaryCall;
    getPlanAssessment(request: agent_pb.OperatingPicture, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: agent_pb.PlanAssessment) => void): grpc.ClientUnaryCall;
}

export class AgentClient extends grpc.Client implements IAgentClient {
    constructor(address: string, credentials: grpc.ChannelCredentials, options?: Partial<grpc.ClientOptions>);
    public getPlanAssessment(request: agent_pb.OperatingPicture, callback: (error: grpc.ServiceError | null, response: agent_pb.PlanAssessment) => void): grpc.ClientUnaryCall;
    public getPlanAssessment(request: agent_pb.OperatingPicture, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: agent_pb.PlanAssessment) => void): grpc.ClientUnaryCall;
    public getPlanAssessment(request: agent_pb.OperatingPicture, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: agent_pb.PlanAssessment) => void): grpc.ClientUnaryCall;
}
