import json
import uuid
import sys
import os
import logging
from typing import Dict, Any

sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))
from app.schemas.ces import CESEvent
from app.core.versioning import SchemaVersionError

class WarningCaptureHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.warnings = []
    def emit(self, record):
        if record.levelno == logging.WARNING:
            self.warnings.append(record.getMessage())

capture_handler = WarningCaptureHandler()
logging.getLogger("app.core.versioning").addHandler(capture_handler)
logging.getLogger("app.core.versioning").setLevel(logging.WARNING)

datasets = {
    "vpn_login_success.json": {
        "schema_version": "1.0",
        "event_id": str(uuid.uuid4()),
        "timestamp": "2026-06-12T08:15:30Z",
        "source_type": "vpn",
        "event_type": "authentication.login.success",
        "severity": "info",
        "actor": {"username": "jroberts", "ip": "198.51.100.42"},
        "target": {"hostname": "vpn.corp.global"},
        "artifacts": [{"type": "ip", "value": "198.51.100.42"}],
        "raw_event": "2026-06-12 08:15:30 ASA-6-113004: AAA user authentication Successful : server =  10.1.2.3 : user = jroberts",
        "metadata": {"vpn_group": "Engineering", "auth_method": "RADIUS"}
    },
    "vpn_login_failure.json": {
        "schema_version": "1.0",
        "event_id": str(uuid.uuid4()),
        "timestamp": "2026-06-12T08:16:01Z",
        "source_type": "vpn",
        "event_type": "authentication.login.failure",
        "severity": "low",
        "actor": {"username": "jroberts", "ip": "198.51.100.42"},
        "target": {"hostname": "vpn.corp.global"},
        "artifacts": [{"type": "ip", "value": "198.51.100.42"}],
        "raw_event": "2026-06-12 08:16:01 ASA-6-113005: AAA user authentication Rejected : reason = AAA failure : server = 10.1.2.3 : user = jroberts",
        "metadata": {"vpn_group": "Engineering", "reason": "AAA failure"}
    },
    "windows_logon_success.json": {
        "schema_version": "1.0",
        "event_id": str(uuid.uuid4()),
        "timestamp": "2026-06-12T09:01:22Z",
        "source_type": "windows",
        "event_type": "authentication.login.success",
        "severity": "info",
        "actor": {"username": "msmith", "domain": "CORP_AD"},
        "target": {"hostname": "WS-INT-04"},
        "artifacts": [],
        "raw_event": "EventID: 4624, LogonType: 3, TargetUserName: msmith, TargetDomainName: CORP_AD...",
        "metadata": {"event_id": "4624", "logon_type": "3", "process_name": "advapi"}
    },
    "windows_logon_failure.json": {
        "schema_version": "1.0",
        "event_id": str(uuid.uuid4()),
        "timestamp": "2026-06-12T09:02:45Z",
        "source_type": "windows",
        "event_type": "authentication.login.failure",
        "severity": "medium",
        "actor": {"username": "admin_service", "domain": "CORP_AD"},
        "target": {"hostname": "SRV-DB-01"},
        "artifacts": [],
        "raw_event": "EventID: 4625, TargetUserName: admin_service, Status: 0xC000006D",
        "metadata": {"event_id": "4625", "logon_type": "3", "failure_reason": "0xC000006D"}
    },
    "firewall_connection_allowed.json": {
        "schema_version": "1.0",
        "event_id": str(uuid.uuid4()),
        "timestamp": "2026-06-12T10:14:05Z",
        "source_type": "firewall",
        "event_type": "network.connection.allowed",
        "severity": "info",
        "actor": {"ip": "10.0.5.15", "port": 50124},
        "target": {"ip": "203.0.113.88", "port": 443},
        "artifacts": [{"type": "ip", "value": "203.0.113.88"}],
        "raw_event": "10.0.5.15,203.0.113.88,50124,443,tcp,allow,Outbound_HTTPS",
        "metadata": {"rule_name": "Outbound_HTTPS", "bytes_sent": 4096, "bytes_received": 8192}
    },
    "firewall_connection_blocked.json": {
        "schema_version": "1.0",
        "event_id": str(uuid.uuid4()),
        "timestamp": "2026-06-12T10:15:10Z",
        "source_type": "firewall",
        "event_type": "network.connection.blocked",
        "severity": "low",
        "actor": {"ip": "10.0.5.15", "port": 50128},
        "target": {"ip": "198.51.100.99", "port": 22},
        "artifacts": [{"type": "ip", "value": "198.51.100.99"}],
        "raw_event": "10.0.5.15,198.51.100.99,50128,22,tcp,deny,Block_Outbound_SSH",
        "metadata": {"rule_name": "Block_Outbound_SSH"}
    },
    "powershell_execution_success.json": {
        "schema_version": "1.0",
        "event_id": str(uuid.uuid4()),
        "timestamp": "2026-06-12T11:22:33Z",
        "source_type": "powershell",
        "event_type": "process.execution.success",
        "severity": "high",
        "actor": {"username": "sadmin", "process": "powershell.exe"},
        "target": {"command_line": "powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \"Get-Process\""},
        "artifacts": [],
        "raw_event": "EventID: 4104, ScriptBlockText: Get-Process...",
        "metadata": {"event_id": "4104", "script_block_id": "abc-123"}
    },
    "powershell_execution_failure.json": {
        "schema_version": "1.0",
        "event_id": str(uuid.uuid4()),
        "timestamp": "2026-06-12T11:25:40Z",
        "source_type": "powershell",
        "event_type": "process.execution.failure",
        "severity": "medium",
        "actor": {"username": "sadmin", "process": "powershell.exe"},
        "target": {"command_line": "powershell.exe -Command \"Stop-Service WinDefend\""},
        "artifacts": [],
        "raw_event": "EventID: 4104, ScriptBlockText: Stop-Service WinDefend, Error: Access Denied",
        "metadata": {"event_id": "4104", "error_code": "AccessDenied"}
    },
    "cloud_login_success.json": {
        "schema_version": "1.0",
        "event_id": str(uuid.uuid4()),
        "timestamp": "2026-06-12T12:05:15Z",
        "source_type": "cloudtrail",
        "event_type": "authentication.login.success",
        "severity": "info",
        "actor": {"username": "cloud_arch", "ip": "203.0.113.10"},
        "target": {"hostname": "console.aws.amazon.com"},
        "artifacts": [{"type": "ip", "value": "203.0.113.10"}],
        "raw_event": "{\"eventName\": \"ConsoleLogin\", \"userIdentity\": {\"userName\": \"cloud_arch\"}, \"sourceIPAddress\": \"203.0.113.10\"}",
        "metadata": {"mfa_used": True}
    },
    "application_audit_event.json": {
        "schema_version": "1.0",
        "event_id": str(uuid.uuid4()),
        "timestamp": "2026-06-12T13:45:00Z",
        "source_type": "application",
        "event_type": "application.data.exported",
        "severity": "high",
        "actor": {"username": "finance_lead", "ip": "10.0.10.50"},
        "target": {"hostname": "crm.corp.global", "name": "Q3_Earnings_Report.csv"},
        "artifacts": [{"type": "file", "value": "Q3_Earnings_Report.csv"}],
        "raw_event": "USER=finance_lead ACTION=Export RESOURCE=Q3_Earnings_Report.csv IP=10.0.10.50",
        "metadata": {"records_exported": 5000}
    }
}

report = []

output_dir = os.path.join(os.path.dirname(__file__), '../datasets/golden/ces')
os.makedirs(output_dir, exist_ok=True)

for filename, data in datasets.items():
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    status = "PASS"
    errors = []
    
    capture_handler.warnings.clear()
    
    try:
        event = CESEvent(**data)
        json_out = event.model_dump_json()
    except Exception as e:
        status = "FAIL"
        errors.append(str(e))
        
    report.append({
        "dataset_name": filename,
        "validation_status": status,
        "warnings": list(capture_handler.warnings),
        "errors": errors
    })

report_path = os.path.join(os.path.dirname(__file__), '../datasets/golden/validation_report.json')
with open(report_path, 'w') as f:
    json.dump(report, f, indent=2)

print("Golden datasets and validation report regenerated.")
