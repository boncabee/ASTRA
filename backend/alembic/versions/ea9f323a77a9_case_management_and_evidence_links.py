"""case management and evidence links

Revision ID: ea9f323a77a9
Revises: fc4fe36e4537
Create Date: 2026-06-16 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ea9f323a77a9'
down_revision = 'fc4fe36e4537'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enum types
    sa.Enum('DRAFT', 'OPEN', 'INVESTIGATING', 'MITIGATING', 'MONITORING', 'RESOLVED', 'CLOSED', 'CANCELLED', name='casestatus').create(op.get_bind())
    sa.Enum('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='casepriority').create(op.get_bind())
    sa.Enum('INFO', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='caseseverity').create(op.get_bind())
    sa.Enum('STATUS_CHANGE', 'ASSIGNMENT', 'CASE_CREATED', 'SYSTEM_ACTION', name='timelineeventtype').create(op.get_bind())

    # Create cases table
    op.create_table('cases',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', postgresql.ENUM('DRAFT', 'OPEN', 'INVESTIGATING', 'MITIGATING', 'MONITORING', 'RESOLVED', 'CLOSED', 'CANCELLED', name='casestatus', create_type=False), nullable=False),
        sa.Column('priority', postgresql.ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='casepriority', create_type=False), nullable=False),
        sa.Column('severity', postgresql.ENUM('INFO', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='caseseverity', create_type=False), nullable=False),
        sa.Column('assigned_to', sa.String(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cases_assigned_to'), 'cases', ['assigned_to'], unique=False)
    op.create_index(op.f('ix_cases_created_at'), 'cases', ['created_at'], unique=False)
    op.create_index(op.f('ix_cases_id'), 'cases', ['id'], unique=False)
    op.create_index(op.f('ix_cases_priority'), 'cases', ['priority'], unique=False)
    op.create_index(op.f('ix_cases_severity'), 'cases', ['severity'], unique=False)
    op.create_index(op.f('ix_cases_status'), 'cases', ['status'], unique=False)

    # Create case_assignments table
    op.create_table('case_assignments',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('case_id', sa.Uuid(), nullable=False),
        sa.Column('assigned_user_id', sa.String(), nullable=False),
        sa.Column('assigned_by', sa.String(), nullable=False),
        sa.Column('assigned_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_case_assignments_case_id'), 'case_assignments', ['case_id'], unique=False)
    op.create_index(op.f('ix_case_assignments_id'), 'case_assignments', ['id'], unique=False)

    # Create case_evidence_links table
    op.create_table('case_evidence_links',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('case_id', sa.Uuid(), nullable=False),
        sa.Column('evidence_id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ),
        sa.ForeignKeyConstraint(['evidence_id'], ['evidence.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('case_id', 'evidence_id', name='uq_case_evidence_link')
    )
    op.create_index(op.f('ix_case_evidence_case_id'), 'case_evidence_links', ['case_id'], unique=False)
    op.create_index(op.f('ix_case_evidence_evidence_id'), 'case_evidence_links', ['evidence_id'], unique=False)
    op.create_index(op.f('ix_case_evidence_links_id'), 'case_evidence_links', ['id'], unique=False)

    # Create case_timeline table
    op.create_table('case_timeline',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('case_id', sa.Uuid(), nullable=False),
        sa.Column('event_type', postgresql.ENUM('STATUS_CHANGE', 'ASSIGNMENT', 'CASE_CREATED', 'SYSTEM_ACTION', name='timelineeventtype', create_type=False), nullable=False),
        sa.Column('actor', sa.String(), nullable=False),
        sa.Column('event_metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_case_timeline_case_id'), 'case_timeline', ['case_id'], unique=False)
    op.create_index(op.f('ix_case_timeline_created_at'), 'case_timeline', ['created_at'], unique=False)
    op.create_index(op.f('ix_case_timeline_id'), 'case_timeline', ['id'], unique=False)


def downgrade() -> None:
    # Drop case_timeline
    op.drop_index(op.f('ix_case_timeline_id'), table_name='case_timeline')
    op.drop_index(op.f('ix_case_timeline_created_at'), table_name='case_timeline')
    op.drop_index(op.f('ix_case_timeline_case_id'), table_name='case_timeline')
    op.drop_table('case_timeline')

    # Drop case_evidence_links
    op.drop_index(op.f('ix_case_evidence_links_id'), table_name='case_evidence_links')
    op.drop_index(op.f('ix_case_evidence_evidence_id'), table_name='case_evidence_links')
    op.drop_index(op.f('ix_case_evidence_case_id'), table_name='case_evidence_links')
    op.drop_table('case_evidence_links')

    # Drop case_assignments
    op.drop_index(op.f('ix_case_assignments_id'), table_name='case_assignments')
    op.drop_index(op.f('ix_case_assignments_case_id'), table_name='case_assignments')
    op.drop_table('case_assignments')

    # Drop cases
    op.drop_index(op.f('ix_cases_status'), table_name='cases')
    op.drop_index(op.f('ix_cases_severity'), table_name='cases')
    op.drop_index(op.f('ix_cases_priority'), table_name='cases')
    op.drop_index(op.f('ix_cases_id'), table_name='cases')
    op.drop_index(op.f('ix_cases_created_at'), table_name='cases')
    op.drop_index(op.f('ix_cases_assigned_to'), table_name='cases')
    op.drop_table('cases')

    # Drop enums
    sa.Enum(name='timelineeventtype').drop(op.get_bind())
    sa.Enum(name='caseseverity').drop(op.get_bind())
    sa.Enum(name='casepriority').drop(op.get_bind())
    sa.Enum(name='casestatus').drop(op.get_bind())
