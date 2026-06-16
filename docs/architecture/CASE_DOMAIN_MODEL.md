# Case Domain Model

**Phase:** 7
**Project:** ASTRA

## 1. Domain Entities & Relationships

The Case Management domain is strictly relational and designed for immutability and precise access control.

### Core Case Entity
`Case` is the central aggregate root.
- **id**: UUID (Primary Key)
- **title**: String
- **description**: Text
- **status**: Enum (Draft, Open, Investigating, Mitigating, Monitoring, Resolved, Closed, Cancelled)
- **priority**: Enum (Low, Medium, High, Critical)
- **severity**: Enum (Info, Low, Medium, High, Critical)
- **created_at**: Timestamp
- **updated_at**: Timestamp
- **assigned_to**: UUID (Foreign Key -> User, Nullable)
- **created_by**: UUID (Foreign Key -> User/System)

### Relational Entities

**1. Case Assignment**
Tracks the history of ownership.
- **id**: UUID
- **case_id**: UUID (FK -> Case)
- **assigned_user_id**: UUID (FK -> User)
- **assigned_by**: UUID (FK -> User/System)
- **assigned_at**: Timestamp

**2. Case Comment**
Allows collaboration between analysts.
- **id**: UUID
- **case_id**: UUID (FK -> Case)
- **user_id**: UUID (FK -> User)
- **content**: Text
- **created_at**: Timestamp
- **updated_at**: Timestamp (Nullable)

**3. Case Timeline (Audit Log)**
The immutable ledger of all case activity.
- **id**: UUID
- **case_id**: UUID (FK -> Case)
- **event_type**: String (e.g., STATUS_CHANGE, ASSIGNMENT, EVIDENCE_ADDED, AUTOMATION_TRIGGERED)
- **user_id**: UUID (FK -> User/System)
- **event_metadata**: JSONB
- **created_at**: Timestamp

**4. Case Evidence Link**
A many-to-many junction linking Cases to the immutable Evidence/Observation store.
- **id**: UUID
- **case_id**: UUID (FK -> Case)
- **evidence_id**: UUID (FK -> Evidence/Observation)
- **linked_by**: UUID (FK -> User/System)
- **linked_at**: Timestamp

**5. Case Tag**
For categorization and rule-based filtering.
- **id**: UUID
- **case_id**: UUID (FK -> Case)
- **tag_name**: String
- **added_by**: UUID (FK -> User/System)

**6. Case Watcher**
Users who receive notifications for case updates but do not own the case.
- **case_id**: UUID (FK -> Case)
- **user_id**: UUID (FK -> User)
- **added_at**: Timestamp

**7. Case Relationship**
Links related cases together (e.g., Parent/Child or Duplicate).
- **source_case_id**: UUID (FK -> Case)
- **target_case_id**: UUID (FK -> Case)
- **relationship_type**: Enum (Parent, Child, Duplicate, Related)

## 2. Ownership and Boundaries
- A Case *owns* its Timeline, Comments, Assignments, Tags, and Watchers. If a Case is (soft) deleted, these entities are cascadingly archived.
- A Case *references* Evidence and Observations. It does NOT own them. Deleting a Case must never delete Evidence.
- System Actions (e.g., Policy Engine creating a case) use a reserved `SYSTEM_UUID` for the `created_by` or `user_id` fields.
