import logging
from opentelemetry import trace, metrics
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.logs_exporter import OTLPLogExporter
from opentelemetry.sdk.logs.export import BatchLogProcessor
from opentelemetry.sdk.logs import LoggingHandler, LoggerProvider

# Configure tracing
resource = Resource(attributes={"service.name": "simple.ytdownload.com"})
trace.set_tracer_provider(TracerProvider(resource=resource))
trace_exporter = OTLPSpanExporter(endpoint = "http://otel-collector.monitoring.svc.cluster.local:4317")
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(trace_exporter))

# Configure metrics
metric_exporter = OTLPMetricExporter(endpoint = "http://otel-collector.monitoring.svc.cluster.local:4317")
metrics.set_meter_provider(MeterProvider(resource=resource, metric_exporters=[metric_exporter]))

# Logging Configuration
logger_provider = LoggerProvider(resource=resource)
log_exporter = OTLPLogExporter(endpoint="http://otel-collector.monitoring.svc.cluster.local:4317")
logger_provider.add_log_processor(BatchLogProcessor(log_exporter))

# Set up logging with OpenTelemetry
logging.basicConfig(level=logging.INFO)
otel_handler = LoggingHandler(logger_provider=logger_provider)
logging.getLogger().addHandler(otel_handler)

# Instrument Flask
def setup_otel(app):
    FlaskInstrumentor().instrument_app(app)
    SQLAlchemyInstrumentor().instrument()
