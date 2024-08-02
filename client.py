import grpc
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient
from opentelemetry.sdk.resources import Resource
import hello_world_pb2_grpc, hello_world_pb2

resource = Resource(attributes={
    # You can add here what ever resource info you want
    "service.name": "my_grpc_client",
    "service.version": "1.0.0",
    "telemetry.sdk.language": "python",
    "telemetry.sdk.name": "opentelemetry",
    "telemetry.sdk.version": "1.26.0",
})

# Set up tracer with the resource

tracer_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer_provider)
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

# Instrument gRPC client
grpc_client_instrumentor = GrpcInstrumentorClient()
grpc_client_instrumentor.instrument()


def run():
    tracer = trace.get_tracer(__name__)
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = hello_world_pb2_grpc.GreeterStub(channel)

        # Create a span for the SayHello RPC
        with tracer.start_as_current_span("SayHelloSpan") as span:
            response = stub.SayHello(hello_world_pb2.HelloRequest(name="RPC"))
            span.set_attribute("client.custom.trace", "SayHello executed")
            span.add_event("client.event", {"description": "SayHello RPC called"})

        # Create a span for the SayName RPC
        with tracer.start_as_current_span("SayNameSpan") as span:
            response_ = stub.SayName(hello_world_pb2.NameRequest(name="Aayush"))
            span.set_attribute("client.custom.trace", "SayName executed")
            span.add_event("client.event", {"description": "SayName RPC called"})

    print("Greeter client received: " + response.message)
    print("Greeter name client received: " + response_.message)


if __name__ == "__main__":
    run()
