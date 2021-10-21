// package: agent
// file: agent.proto

/* tslint:disable */
/* eslint-disable */

import * as jspb from "google-protobuf";

export class OperatingPicture extends jspb.Message { 
    getNummissiles(): number;
    setNummissiles(value: number): OperatingPicture;

    hasTargetidtodamage(): boolean;
    clearTargetidtodamage(): void;
    getTargetidtodamage(): TargetToDamageMap | undefined;
    setTargetidtodamage(value?: TargetToDamageMap): OperatingPicture;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): OperatingPicture.AsObject;
    static toObject(includeInstance: boolean, msg: OperatingPicture): OperatingPicture.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: OperatingPicture, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): OperatingPicture;
    static deserializeBinaryFromReader(message: OperatingPicture, reader: jspb.BinaryReader): OperatingPicture;
}

export namespace OperatingPicture {
    export type AsObject = {
        nummissiles: number,
        targetidtodamage?: TargetToDamageMap.AsObject,
    }
}

export class TargetIdToDamageEntry extends jspb.Message { 
    getId(): string;
    setId(value: string): TargetIdToDamageEntry;
    getDamage(): number;
    setDamage(value: number): TargetIdToDamageEntry;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): TargetIdToDamageEntry.AsObject;
    static toObject(includeInstance: boolean, msg: TargetIdToDamageEntry): TargetIdToDamageEntry.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: TargetIdToDamageEntry, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): TargetIdToDamageEntry;
    static deserializeBinaryFromReader(message: TargetIdToDamageEntry, reader: jspb.BinaryReader): TargetIdToDamageEntry;
}

export namespace TargetIdToDamageEntry {
    export type AsObject = {
        id: string,
        damage: number,
    }
}

export class TargetToDamageMap extends jspb.Message { 
    clearEntriesList(): void;
    getEntriesList(): Array<TargetIdToDamageEntry>;
    setEntriesList(value: Array<TargetIdToDamageEntry>): TargetToDamageMap;
    addEntries(value?: TargetIdToDamageEntry, index?: number): TargetIdToDamageEntry;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): TargetToDamageMap.AsObject;
    static toObject(includeInstance: boolean, msg: TargetToDamageMap): TargetToDamageMap.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: TargetToDamageMap, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): TargetToDamageMap;
    static deserializeBinaryFromReader(message: TargetToDamageMap, reader: jspb.BinaryReader): TargetToDamageMap;
}

export namespace TargetToDamageMap {
    export type AsObject = {
        entriesList: Array<TargetIdToDamageEntry.AsObject>,
    }
}

export class PlanAssessment extends jspb.Message { 
    clearActionassessmentsList(): void;
    getActionassessmentsList(): Array<ActionAssessment>;
    setActionassessmentsList(value: Array<ActionAssessment>): PlanAssessment;
    addActionassessments(value?: ActionAssessment, index?: number): ActionAssessment;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): PlanAssessment.AsObject;
    static toObject(includeInstance: boolean, msg: PlanAssessment): PlanAssessment.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: PlanAssessment, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): PlanAssessment;
    static deserializeBinaryFromReader(message: PlanAssessment, reader: jspb.BinaryReader): PlanAssessment;
}

export namespace PlanAssessment {
    export type AsObject = {
        actionassessmentsList: Array<ActionAssessment.AsObject>,
    }
}

export class ActionAssessment extends jspb.Message { 
    getActiontargetid(): string;
    setActiontargetid(value: string): ActionAssessment;
    getNummissilesleft(): number;
    setNummissilesleft(value: number): ActionAssessment;

    hasTargetidtocurrentdamage(): boolean;
    clearTargetidtocurrentdamage(): void;
    getTargetidtocurrentdamage(): TargetToDamageMap | undefined;
    setTargetidtocurrentdamage(value?: TargetToDamageMap): ActionAssessment;

    hasTargetidtodesireddamage(): boolean;
    clearTargetidtodesireddamage(): void;
    getTargetidtodesireddamage(): TargetToDamageMap | undefined;
    setTargetidtodesireddamage(value?: TargetToDamageMap): ActionAssessment;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): ActionAssessment.AsObject;
    static toObject(includeInstance: boolean, msg: ActionAssessment): ActionAssessment.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: ActionAssessment, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): ActionAssessment;
    static deserializeBinaryFromReader(message: ActionAssessment, reader: jspb.BinaryReader): ActionAssessment;
}

export namespace ActionAssessment {
    export type AsObject = {
        actiontargetid: string,
        nummissilesleft: number,
        targetidtocurrentdamage?: TargetToDamageMap.AsObject,
        targetidtodesireddamage?: TargetToDamageMap.AsObject,
    }
}
