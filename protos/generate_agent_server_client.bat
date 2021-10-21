python -m grpc_tools.protoc -I./ --python_out=../Backend/agent-server --grpc_python_out=../Backend/agent-server agent.proto

cd ../frontend
npm run gen-client