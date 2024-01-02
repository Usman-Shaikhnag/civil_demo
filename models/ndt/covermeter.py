from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math

class CoverMeter(models.Model):
    _name = "ndt.cover.meter"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Cover Meter")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('ndt.cover.meter.line','parent_id',string="Parameter")
    average = fields.Float(string='Average', digits=(16, 2), compute='_compute_average')
    average_min = fields.Float(string='Average Min', digits=(16, 2), compute='_compute_average')
    average_max = fields.Float(string='Average Max', digits=(16, 2), compute='_compute_average')

    #just Testing will remove later
    parameters = fields.Many2many('lerm.parameter.master',string="Parameters")


    @api.depends('child_lines.cover')
    def _compute_average(self):
        for record in self:
            total_cover = sum(record.child_lines.mapped('cover'))
            num_records = len(record.child_lines)

            if num_records > 0:
                record.average = total_cover / num_records
                cover_values = record.child_lines.mapped('cover')
                record.average_min = min(cover_values)
                record.average_max = max(cover_values)
            else:
                record.average = 0.0
                record.average_min = 0.0
                record.average_max = 0.0



    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(CoverMeter, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        return record

class CrackDepthLine(models.Model):
    _name = "ndt.cover.meter.line"
    parent_id = fields.Many2one('ndt.cover.meter',string="Parent Id")
    member = fields.Char(string="Element Type")
    location = fields.Char(string="Location")
    level = fields.Char(string="Level")
    cover = fields.Float(string='Cover in mm',digits=(16, 2))
    


                


