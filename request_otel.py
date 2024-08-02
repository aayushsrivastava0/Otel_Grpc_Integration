import time
import requests
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor

# Set up tracing
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

# Instrument the requests library for tracing
RequestsInstrumentor().instrument()

# Set up metrics
exporter = ConsoleMetricExporter()
metric_reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)  # Export every 5 seconds
meter_provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

# Customize metrics collection
configuration = {
    "system.memory.usage": ["used", "free", "cached"],
    "system.cpu.time": ["idle", "user", "system", "irq"],
    "process.runtime.memory": ["rss", "vms"],
    "process.runtime.cpu.time": ["user", "system"],
    "process.runtime.context_switches": ["involuntary", "voluntary"],
}
SystemMetricsInstrumentor(config=configuration).instrument()

#sample HTTP request
response = requests.get(url="https://www.google.com/")
print(f"Response status code: {response.status_code}")

try:
    print("Collecting system metrics for 10 seconds...")
    time.sleep(10)
except KeyboardInterrupt:
    pass

print("Metrics collection complete.")
