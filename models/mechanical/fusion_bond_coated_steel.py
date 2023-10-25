
from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math

class MechanicalFusionBondSteel(models.Model):
    _name = "mechanical.fusion.bond.steel"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Fusion Bond Epoxy Coated Steel")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="ELN")


    dia = fields.Float("DIA, mm")
    coating_thickness = fields.Float("Coating Thickness")
    continuity_coating = fields.Selection(
        [('satisfactory', 'Satisfactory'),
         ('unsatisfactory', 'UnSatisfactory')],
        string='Continuity of Coating',
        help='Choose an option from the list.'
    )

    adhesion_coating = fields.Selection(
        [('nocrackobserved', 'No Visibal crack observed'),
         ('crackobserved', 'Crack Observed')],
        string='Adhesion of coating',
        help='Choose an option from the list.'
    )

    

    

    



    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(MechanicalFusionBondSteel, self).create(vals)
        record.get_all_fields()
        record.eln_ref.write({'model_id':record.id})
        return record
    

    @api.depends('eln_ref')
    def _compute_sample_parameters(self):
        # records = self.env['lerm.eln'].search([('id','=', record.eln_id.id)]).parameters_result
        # print("records",records)
        # self.sample_parameters = records
        for record in self:
            records = record.eln_ref.parameters_result.parameter.ids
            record.sample_parameters = records
            print("Records",records)

    def get_all_fields(self):
        record = self.env['mechanical.fusion.bond.steel'].browse(self.ids[0])
        field_values = {}
        for field_name, field in record._fields.items():
            field_value = record[field_name]
            field_values[field_name] = field_value

        return field_values