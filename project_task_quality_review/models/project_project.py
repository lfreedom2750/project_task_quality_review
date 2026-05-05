from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    quality_inspector_id = fields.Many2one(
        comodel_name="res.users",
        string="Quality Inspector",
        tracking=True,
        help="The user responsible for reviewing tasks in this project before they are marked as Done.",
    )