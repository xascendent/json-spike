import time
from prometheus_client import CollectorRegistry, Counter, Gauge, push_to_gateway
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MetricsReporter:
    def __init__(self):
        """Initialize the metrics reporter with connection to Pushgateway."""
        PUSHGATEWAY_URL = os.getenv("PUSHGATEWAY_URL")
        PUSHGATEWAY_JOB_NAME = os.getenv("PUSHGATEWAY_JOB_NAME")

        self.pushgateway_url = PUSHGATEWAY_URL
        self.job_name = PUSHGATEWAY_JOB_NAME
        # Create a fresh registry
        self.registry = CollectorRegistry()
        
        # Initialize all metrics
        self._initialize_metrics()
    
    def _initialize_metrics(self):
        """Initialize all the metrics we want to track."""
        # Processing metrics
        self.records_processed = Counter(
            'processing_records_total', 
            'Total number of records processed', 
            ['file_id'],
            registry=self.registry
        )
        
        self.processing_status = Gauge(
            'processing_file_status', 
            'Processing status for a file (1=success, 0=failure)', 
            ['file_id'],
            registry=self.registry
        )
        
        # LLM-related metrics for de-identification
        self.deid_llm_failures = Counter(
            'deid_llm_failures_total', 
            'Number of LLM failures during de-identification', 
            ['file_id'],
            registry=self.registry
        )
        
        self.deid_processed_records = Counter(
            'deid_records_processed_total', 
            'Number of records processed through de-identification', 
            ['file_id'],
            registry=self.registry
        )
        
        # Medication-related metrics
        self.med_lookup_count = Counter(
            'med_lookups_total', 
            'Number of medication lookups performed', 
            ['file_id'],
            registry=self.registry
        )
        
        self.med_lookup_failures = Counter(
            'med_lookup_failures_total', 
            'Number of failed medication lookups', 
            ['file_id'],
            registry=self.registry
        )
        
        # Missing data metrics
        self.missing_narratives = Counter(
            'missing_narratives_total', 
            'Count of records with missing narratives', 
            ['file_id'],
            registry=self.registry
        )
    
    def report_records_processed(self, file_id, count=1):
        """Report the number of processed records for a file."""
        self.records_processed.labels(file_id=file_id).inc(count)
        self._push_metrics()
    
    def report_processing_status(self, file_id, success=True):
        """Report the processing status for a file (success/failure)."""
        status_value = 1 if success else 0
        self.processing_status.labels(file_id=file_id).set(status_value)
        self._push_metrics()
    
    def report_deid_llm_failure(self, file_id, count=1):
        """Report LLM failures during de-identification."""
        self.deid_llm_failures.labels(file_id=file_id).inc(count)
        self._push_metrics()
    
    def report_deid_record_processed(self, file_id, count=1):
        """Report the number of records processed through de-identification."""
        self.deid_processed_records.labels(file_id=file_id).inc(count)
        self._push_metrics()
    
    def report_med_lookup(self, file_id, count=1):
        """Report medication lookups performed."""
        self.med_lookup_count.labels(file_id=file_id).inc(count)
        self._push_metrics()
    
    def report_med_lookup_failure(self, file_id, count=1):
        """Report failed medication lookups."""
        self.med_lookup_failures.labels(file_id=file_id).inc(count)
        self._push_metrics()
    
    def report_missing_narrative(self, file_id, count=1):
        """Report count of records with missing narratives."""
        self.missing_narratives.labels(file_id=file_id).inc(count)
        self._push_metrics()
    
    def _push_metrics(self):
        """Push all metrics to Pushgateway."""
        try:
            push_to_gateway(
                self.pushgateway_url, 
                job=self.job_name, 
                registry=self.registry
            )
        except Exception as e:
            print(f"Failed to push metrics to {self.pushgateway_url}: {e}")


def example_usage():
    """Example function showing how to use the MetricsReporter."""
    # Initialize the reporter
    reporter = MetricsReporter()
    
    # Simulate some processing with a file ID
    file_id = "file_123456"
    
    # Report metrics during processing
    reporter.report_records_processed(file_id, 100)
    reporter.report_deid_record_processed(file_id, 98)
    reporter.report_deid_llm_failure(file_id, 2)
    reporter.report_med_lookup(file_id, 45)
    reporter.report_med_lookup_failure(file_id, 3)
    reporter.report_missing_narrative(file_id, 5)
    
    # Report final processing status
    reporter.report_processing_status(file_id, success=True)
    
    print(f"Metrics for file {file_id} have been pushed to Pushgateway")


if __name__ == "__main__":
    example_usage()