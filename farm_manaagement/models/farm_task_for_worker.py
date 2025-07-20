from odoo import fields, api, models
import datetime


class WorkerTask(models.Model):
    _name = "worker.task"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "task_name"
    _description = "Provide The Workertask"

    task_name = fields.Char(string="Task Name")
    # project_name = fields.Many2one('project.project',string="Project")
    # project = fields.Many2one('project.project',string="project Name")
    deadline = fields.Datetime(string="Deadline")
    # tags = fields.Many2many('project.tags',string="Tags")
    user_ids = fields.Many2one('hr.employee', string='Assignees', required=True)
    user_id = fields.Many2one('hr.employee', string="Assignees", required=True)
    worker_name = fields.Many2one('hr.employee', string="Worker Name", required=True)
    task_date = fields.Date(string="Task Date", related='timesheet_ids.task_date')
    task_hourse = fields.Float(string="Task Hourse",related='timesheet_ids.hourse_spend')
    # project_id = fields.One2many('projct.extra','project_ids',string="Project Task")
    assigned_date = fields.Datetime(string="Assigning Date")
    last_stage_update = fields.Datetime(string="Last Stage Update")
    task_no = fields.Char(string="Sequence")
    email_cc = fields.Char(string="Email CC")
    working_hours_open = fields.Float(string="Hours")
    working_days_open = fields.Char(string="Total Days")
    description = fields.Text(string="Description")
    timesheet_ids = fields.One2many('farm.timesheet', 'timesheet_id', string="Time")
    work_ids = fields.One2many('farm.sub.task', 'task_id', string="Crop Name")
    remaining_hours = fields.Float("Remaining Hours", compute='_compute_remaining_hours', store=True, readonly=True)
    subtask_effective_hours = fields.Float("Sub-tasks Hours Spent", store=True)
    initially_planned_hours = fields.Float(string="Initially Planned Hours")
    effective_hours = fields.Float(string="Total Hours Spent", compute='_compute_effective_hours', compute_sudo=True,
                                   store=True)
    progress = fields.Float("Progress", compute='_compute_progress_hours', store=True, group_operator="avg",
                            help="Display progress of current task.")
    state = fields.Selection([('confirm', 'Confirm'), ('draft', 'Draft'), ('finished', 'Finished')], string="State")
    # depend_id = fields.Many2many('worker.task',string="Depends")
    priority = fields.Selection([('clear', 'Clear'), ('normal', 'Normal')
                                 ], copy=False, required=True)
    max_rate = fields.Integer(string="Max Rate", default=100)
    activity_state = fields.Integer(string="Activity State")

    user_id = fields.Many2one('res.users', string="User")

    @api.depends('effective_hours', 'subtask_effective_hours', 'initially_planned_hours')
    def _compute_remaining_hours(self):
        for task in self:
            task.remaining_hours = task.initially_planned_hours - task.effective_hours - task.subtask_effective_hours

    @api.onchange('assigned_date', 'deadline', 'working_days_open')
    def _compute_days(self):
        if self.assigned_date and self.deadline:
            for rec in self:
                s_date = rec.assigned_date
                e_date = rec.deadline
                rec.working_days_open = str((e_date - s_date).days) + " " + "Days"

    @api.depends('timesheet_ids.hourse_spend')
    def _compute_effective_hours(self):
        if not any(self._ids):
            for task in self:
                task.effective_hours = round(sum(task.timesheet_ids.mapped('hourse_spend')), 2)
            return
        timesheet_read_group = self.env['farm.timesheet'].read_group([('timesheet_id', 'in', self.ids)],
                                                                     ['hourse_spend', 'timesheet_id'], ['timesheet_id'])
        timesheets_per_task = {res['timesheet_id'][0]: res['hourse_spend'] for res in timesheet_read_group}
        for task in self:
            task.effective_hours = round(timesheets_per_task.get(task.id, 0.0), 2)

    @api.depends('effective_hours', 'subtask_effective_hours', 'initially_planned_hours')
    def _compute_progress_hours(self):
        for task in self:
            if (task.initially_planned_hours > 0.0):
                task_total_hours = task.effective_hours + task.subtask_effective_hours
                if task_total_hours > task.initially_planned_hours:
                    task.progress = 100
                else:
                    task.progress = round(100.0 * task_total_hours / task.initially_planned_hours, 2)
            else:
                task.progress = 0.0

    def action_draft(self):
        self.state = 'draft'

    def action_confirm(self):
        self.state = 'confirm'

    def action_finish(self):
        self.state = 'finished'


class CreateKanban(models.Model):
    _name = "project.create"
    _description = "Create The Kanban"

    task_name = fields.Char(string="Task Name", required=True)
    worker_name = fields.Many2one('hr.employee', string="Worker Name", required=True)
    user_id = fields.Many2one('hr.employee', string="Assignees", required=True)
    assigned_date = fields.Datetime(string="Assigning Date")


# SubTask Fiels

class SubTaskLine(models.Model):
    _name = "farm.sub.task"
    _description = "Crop Name Line"

    task_id = fields.Many2one('worker.task', string="Farming")
    title = fields.Char(string="Title")
    assigned = fields.Many2one('hr.employee', string="Assignees")
    deadline = fields.Date(string="Deadline")
    stage = fields.Many2one('project.task.type', string="Stage")


class TimeSheetManage(models.Model):
    _name = 'farm.timesheet'
    _description = 'Timesheet Mangement'

    timesheet_id = fields.Many2one('worker.task', string="Timesheet")
    task_name = fields.Many2one('worker.task', string="Task Name")
    task_date = fields.Date(string="Date")
    worker_name = fields.Many2one('hr.employee', string="Employee")
    description = fields.Char(string="Description")
    hourse_spend = fields.Float(string="Hours Spend")

# @api.onchange('assigned_date', 'last_stage_update', 'working_hours_open')
# def calculate_timer(self):
# 	for record in self:
# 	  if record.working_hours_open is set:
# 	      start = record.assigned_date
# 	      end = record.last_stage_update
# 	      difference = last_stage_update - assigned_date
# 	      difference_in_seconds = difference.total_seconds()
# 	      record ['working_hours_open'] = difference_in_seconds / 3600.0")
# 	last_stage_update = fields.Datetime(string="Last Stage Update")
