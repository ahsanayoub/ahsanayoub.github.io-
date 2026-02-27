"""initial schema

Revision ID: 20260227_0001
Revises:
Create Date: 2026-02-27 00:00:00
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260227_0001"
down_revision = None
branch_labels = None
depends_on = None


user_role = sa.Enum("Admin", "Recruiter", "HiringManager", name="user_role")
employment_type = sa.Enum("FullTime", "PartTime", "Contract", "Temporary", "Intern", name="employment_type")
requisition_status = sa.Enum("Draft", "Open", "OnHold", "Closed", "Cancelled", name="requisition_status")
application_status = sa.Enum(
    "Applied", "Screening", "Interview", "Offer", "Hired", "Rejected", "Withdrawn", name="application_status"
)
interview_recommendation = sa.Enum("StrongYes", "Yes", "No", "StrongNo", name="interview_recommendation")
offer_status = sa.Enum("Draft", "Extended", "Accepted", "Rejected", "Expired", name="offer_status")


def upgrade() -> None:
    bind = op.get_bind()
    user_role.create(bind, checkfirst=True)
    employment_type.create(bind, checkfirst=True)
    requisition_status.create(bind, checkfirst=True)
    application_status.create(bind, checkfirst=True)
    interview_recommendation.create(bind, checkfirst=True)
    offer_status.create(bind, checkfirst=True)

    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=False)
    op.create_index("ix_users_organization_id", "users", ["organization_id"], unique=False)
    op.create_index("ix_users_role", "users", ["role"], unique=False)

    op.create_table(
        "candidates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("current_company", sa.String(length=255), nullable=True),
        sa.Column("current_title", sa.String(length=255), nullable=True),
        sa.Column("years_experience", sa.Integer(), nullable=True),
        sa.Column("resume_file_name", sa.String(length=255), nullable=True),
        sa.Column("resume_file_url", sa.String(length=500), nullable=True),
        sa.Column("resume_uploaded_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("parsed_data", sa.JSON(), nullable=True),
        sa.Column("parsed_skills", sa.JSON(), nullable=True),
        sa.Column("parsed_education", sa.JSON(), nullable=True),
        sa.Column("parsed_experience", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_candidates_email", "candidates", ["email"], unique=False)
    op.create_index("ix_candidates_organization_id", "candidates", ["organization_id"], unique=False)

    op.create_table(
        "requisitions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("hiring_manager_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("department", sa.String(length=255), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=False),
        sa.Column("employment_type", employment_type, nullable=False),
        sa.Column("required_skills", sa.JSON(), nullable=False),
        sa.Column("status", requisition_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_requisitions_department", "requisitions", ["department"], unique=False)
    op.create_index("ix_requisitions_location", "requisitions", ["location"], unique=False)
    op.create_index("ix_requisitions_organization_id", "requisitions", ["organization_id"], unique=False)
    op.create_index("ix_requisitions_status", "requisitions", ["status"], unique=False)
    op.create_index("ix_requisitions_title", "requisitions", ["title"], unique=False)

    op.create_table(
        "applications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("candidate_id", sa.Integer(), sa.ForeignKey("candidates.id"), nullable=False),
        sa.Column("requisition_id", sa.Integer(), sa.ForeignKey("requisitions.id"), nullable=False),
        sa.Column("status", application_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("candidate_id", "requisition_id", name="uq_applications_candidate_requisition"),
    )
    op.create_index("ix_applications_status", "applications", ["status"], unique=False)

    op.create_table(
        "application_status_audits",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("application_id", sa.Integer(), sa.ForeignKey("applications.id"), nullable=False),
        sa.Column("from_status", application_status, nullable=True),
        sa.Column("to_status", application_status, nullable=False),
        sa.Column("changed_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("changed_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_application_status_audits_application_id", "application_status_audits", ["application_id"], unique=False)

    op.create_table(
        "interview_stages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("requisition_id", sa.Integer(), sa.ForeignKey("requisitions.id"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("stage_order", sa.Integer(), nullable=False),
        sa.Column("is_required", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_interview_stages_requisition_id", "interview_stages", ["requisition_id"], unique=False)
    op.create_index("ix_interview_stages_stage_order", "interview_stages", ["stage_order"], unique=False)

    op.create_table(
        "interview_feedback",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("application_id", sa.Integer(), sa.ForeignKey("applications.id"), nullable=False),
        sa.Column("interview_stage_id", sa.Integer(), sa.ForeignKey("interview_stages.id"), nullable=False),
        sa.Column("interviewer_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("comments", sa.String(length=4000), nullable=True),
        sa.Column("recommendation", interview_recommendation, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_interview_feedback_application_id", "interview_feedback", ["application_id"], unique=False)
    op.create_index("ix_interview_feedback_interview_stage_id", "interview_feedback", ["interview_stage_id"], unique=False)

    op.create_table(
        "offers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("application_id", sa.Integer(), sa.ForeignKey("applications.id"), nullable=False, unique=True),
        sa.Column("base_salary", sa.Numeric(12, 2), nullable=False),
        sa.Column("bonus", sa.Numeric(12, 2), nullable=True),
        sa.Column("equity", sa.Numeric(12, 2), nullable=True),
        sa.Column("status", offer_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_offers_application_id", "offers", ["application_id"], unique=False)
    op.create_index("ix_offers_status", "offers", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_offers_status", table_name="offers")
    op.drop_index("ix_offers_application_id", table_name="offers")
    op.drop_table("offers")

    op.drop_index("ix_interview_feedback_interview_stage_id", table_name="interview_feedback")
    op.drop_index("ix_interview_feedback_application_id", table_name="interview_feedback")
    op.drop_table("interview_feedback")

    op.drop_index("ix_interview_stages_stage_order", table_name="interview_stages")
    op.drop_index("ix_interview_stages_requisition_id", table_name="interview_stages")
    op.drop_table("interview_stages")

    op.drop_index("ix_application_status_audits_application_id", table_name="application_status_audits")
    op.drop_table("application_status_audits")

    op.drop_index("ix_applications_status", table_name="applications")
    op.drop_table("applications")

    op.drop_index("ix_requisitions_title", table_name="requisitions")
    op.drop_index("ix_requisitions_status", table_name="requisitions")
    op.drop_index("ix_requisitions_organization_id", table_name="requisitions")
    op.drop_index("ix_requisitions_location", table_name="requisitions")
    op.drop_index("ix_requisitions_department", table_name="requisitions")
    op.drop_table("requisitions")

    op.drop_index("ix_candidates_organization_id", table_name="candidates")
    op.drop_index("ix_candidates_email", table_name="candidates")
    op.drop_table("candidates")

    op.drop_index("ix_users_role", table_name="users")
    op.drop_index("ix_users_organization_id", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

    op.drop_table("organizations")

    bind = op.get_bind()
    offer_status.drop(bind, checkfirst=True)
    interview_recommendation.drop(bind, checkfirst=True)
    application_status.drop(bind, checkfirst=True)
    requisition_status.drop(bind, checkfirst=True)
    employment_type.drop(bind, checkfirst=True)
    user_role.drop(bind, checkfirst=True)
