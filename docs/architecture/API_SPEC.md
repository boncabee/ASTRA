# ASTRA API Specification

Document ID: ASTRA-API-001
Version: 2.0
Status: Approved

Related Documents:

* ARCHITECTURE.md
* DATABASE_SCHEMA.md
* TRACEABILITY_MATRIX.md

---

# Purpose

Define all public API contracts.

---

# API Principles

* RESTful
* Stateless
* JSON Only
* Versioned

Base Path:

```text
/api/v1
```

---

# Response Standard

Success

```json
{
  "success": true,
  "data": {},
  "meta": {}
}
```

---

Error

```json
{
  "success": false,
  "error": {
    "code": "",
    "message": ""
  }
}
```

---

# Endpoint Matrix

| Endpoint                  | Requirement |
| ------------------------- | ----------- |
| POST /analysis            | FR-001      |
| GET /analysis/{id}        | FR-009      |
| GET /analysis/{id}/result | FR-010      |
| GET /incidents            | FR-010      |
| GET /health               | NFR         |

---

# POST /analysis

Purpose:

Upload logs.

Request:

```multipart
file
source_type
privacy_mode
```

Response:

```json
{
  "job_id": "",
  "status": "queued"
}
```

Traceability:

FR-001

---

# GET /analysis/{job_id}

Purpose:

Get job status.

Response:

```json
{
  "job_id": "",
  "status": ""
}
```

Traceability:

FR-009

---

# GET /analysis/{job_id}/result

Purpose:

Get completed analysis.

Response:

```json
{
  "incident_id": "",
  "timeline": [],
  "narrative": "",
  "mitre_mapping": [],
  "ioc_list": [],
  "confidence": 0.0
}
```

Traceability:

FR-004
FR-005
FR-006
FR-007
FR-008

---

# GET /incidents

Purpose:

List incidents.

Traceability:

FR-010

---

# GET /health

Purpose:

Health check.

Response:

```json
{
  "status": "healthy"
}
```

---

# API Governance

Any API change requires updates to:

* TRACEABILITY_MATRIX.md
* TESTING_STRATEGY.md
* AUDIT.md

```
```
