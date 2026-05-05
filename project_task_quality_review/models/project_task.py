from odoo import fields, models, _
from odoo.exceptions import ValidationError


READY_FOR_REVIEW_STAGE_NAME = "ready for review"
DONE_STAGE_NAME = "done"


class ProjectTask(models.Model):
    _inherit = "project.task"

    is_done = fields.Boolean(
        string="Quality Review Passed",
        default=False,
        copy=False,
        tracking=True,
        help="Set to True when the Quality Inspector approves the task.",
    )

    quality_inspected_date = fields.Datetime(
        string="Quality Inspected Date",
        readonly=True,
        copy=False,
        tracking=True,
        help="Timestamp of when the quality review was passed.",
    )

    quality_inspector_id = fields.Many2one(
        comodel_name="res.users",
        string="Quality Inspector",
        related="project_id.quality_inspector_id",
        store=True,
        readonly=True,
        help="Inherited from the related project.",
    )

    def _normalize_stage_name(self, stage):
        return (stage.name or "").strip().lower()

    def action_mark_review_passed(self):
        for task in self:
            task.write({
                "is_done": True,
                "quality_inspected_date": fields.Datetime.now(),
            })

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Quality Review Passed"),
                "message": _("The task has been approved by the Quality Inspector."),
                "type": "success",
                "sticky": False,
            },
        }

    def action_reset_review(self):
        for task in self:
            task.write({
                "is_done": False,
            })
        return True

    def write(self, vals):
        if "stage_id" not in vals:
            return super().write(vals)

        new_stage = self.env["project.task.type"].browse(vals["stage_id"])
        new_stage_name = self._normalize_stage_name(new_stage)

        for task in self:
            old_stage_name = task._normalize_stage_name(task.stage_id)

            if new_stage_name == DONE_STAGE_NAME and not task.is_done:
                raise ValidationError(_(
                    'Task "%s" cannot be moved to Done until the Quality Review has been passed.'
                ) % task.name)

            task_vals = vals.copy()

            if new_stage_name == READY_FOR_REVIEW_STAGE_NAME:
                inspector = task.project_id.quality_inspector_id
                if inspector and inspector not in task.user_ids:
                    task_vals["user_ids"] = [(4, inspector.id)]

            if old_stage_name == DONE_STAGE_NAME and new_stage_name != DONE_STAGE_NAME:
                task_vals.update({
                    "is_done": False,
                    "quality_inspected_date": False,
                })

            super(ProjectTask, task).write(task_vals)

        return True