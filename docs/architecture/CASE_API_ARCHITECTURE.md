# Case API Architecture

## Overview
The Case API provides a secure, RESTful interface for managing the Case lifecycle, assigning ownership, and tracking associated evidence. It is implemented using FastAPI and adheres to the ASTRA platform's strict RBAC and Auditing requirements.

## Base URL
`/api/v1/cases`

## Endpoints

### 1. Create Case
- **Method**: `POST`
- **Path**: `/api/v1/cases`
- **RBAC**: Analyst, Responder, Manager, Admin
- **Payload**: `CaseCreate` (title, description, priority, severity)
- **Response**: `CaseResponse` (includes DRAFT status, generated ID, timestamps)
- **Side Effects**: Generates `CASE_CREATED` Timeline event and `CREATED` Audit event.

### 2. List Cases
- **Method**: `GET`
- **Path**: `/api/v1/cases`
- **RBAC**: Viewer, Analyst, Responder, Manager, Admin
- **Parameters**: `skip` (int), `limit` (int), `case_status`, `priority`, `severity`, `assigned_to`
- **Response**: `List[CaseResponse]`

### 3. Get Case by ID
- **Method**: `GET`
- **Path**: `/api/v1/cases/{case_id}`
- **RBAC**: Viewer, Analyst, Responder, Manager, Admin
- **Response**: `CaseResponse`

### 4. Update Case
- **Method**: `PATCH`
- **Path**: `/api/v1/cases/{case_id}`
- **RBAC**: Analyst, Responder, Manager, Admin
- **Payload**: `CaseUpdate` (title, description, priority, severity)
- **Response**: `CaseResponse`
- **Side Effects**: Generates diff-based `UPDATED` Audit event.

### 5. Assign Case
- **Method**: `POST`
- **Path**: `/api/v1/cases/{case_id}/assign`
- **RBAC**: Analyst (self-assignment only), Responder, Manager, Admin
- **Payload**: `CaseAssignRequest` (assigned_user_id)
- **Response**: `CaseResponse`
- **Side Effects**: Generates `ASSIGNMENT` Timeline event and `ASSIGNED` Audit event.

### 6. Change Status
- **Method**: `POST`
- **Path**: `/api/v1/cases/{case_id}/status`
- **RBAC**: Dynamic (Evaluated by State Machine matrix and role gates)
- **Payload**: `CaseStatusChange` (new_status, reason)
- **Response**: `CaseResponse`
- **Side Effects**: Generates `STATUS_CHANGE` Timeline event and `STATUS_CHANGED` Audit event.

### 7. Get Case Timeline
- **Method**: `GET`
- **Path**: `/api/v1/cases/{case_id}/timeline`
- **RBAC**: Viewer, Analyst, Responder, Manager, Admin
- **Parameters**: `skip`, `limit`
- **Response**: `List[CaseTimelineResponse]`

### 8. Link Evidence
- **Method**: `POST`
- **Path**: `/api/v1/cases/{case_id}/evidence`
- **RBAC**: Analyst, Responder, Manager, Admin
- **Payload**: `CaseEvidenceLinkCreate` (evidence_id)
- **Response**: `CaseEvidenceLinkResponse`
- **Side Effects**: Generates `SYSTEM_ACTION` Timeline event and `CREATED` Audit event. Reactivates link if previously soft-unlinked.

### 9. Get Evidence Links
- **Method**: `GET`
- **Path**: `/api/v1/cases/{case_id}/evidence`
- **RBAC**: Viewer, Analyst, Responder, Manager, Admin
- **Response**: `List[CaseEvidenceLinkResponse]` (Only returns active links)

### 10. Soft Unlink Evidence
- **Method**: `DELETE`
- **Path**: `/api/v1/cases/{case_id}/evidence/{link_id}`
- **RBAC**: Responder, Manager, Admin
- **Response**: `CaseEvidenceLinkResponse` (with `is_active=False`)
- **Side Effects**: Marks link `is_active=False`. Never deletes actual `Evidence`. Generates `SYSTEM_ACTION` Timeline event and `DELETED` Audit event.

## Error Handling
The API returns standard HTTP status codes:
- **400 Bad Request**: Invalid state transitions, malformed payloads.
- **401 Unauthorized**: Missing or invalid authentication token.
- **403 Forbidden**: Valid token, but insufficient RBAC privileges for the endpoint or specific action (e.g., Analyst closing a case).
- **404 Not Found**: Case or Evidence ID does not exist.
