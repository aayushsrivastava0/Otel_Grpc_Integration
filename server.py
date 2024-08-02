import logging
from concurrent import futures

import grpc

from opentelemetry import trace
from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)

import hello_world_pb2_grpc , hello_world_pb2


# Set up tracer
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

# Instrument gRPC server
grpc_server_instrumentor = GrpcInstrumentorServer()
grpc_server_instrumentor.instrument()



# Define the service implementation
class Greeter(hello_world_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return hello_world_pb2.HelloReply(message=f"Hello, {request.name}!")

    def SayName(self, request, context):
        return hello_world_pb2.NameReply(message=f"Hello, {request.name}!")
# Set up and start the server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    hello_world_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
