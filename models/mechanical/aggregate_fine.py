from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
from datetime import timedelta
import math



class FineAggregate(models.Model):
    _name = "mechanical.fine.aggregate"
    _inherit = "lerm.eln"
    _rec_name = "name_aggregate"


    name_aggregate = fields.Char("Name",default="Fine Aggregate")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")

    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="Eln")

    # tests = fields.Many2many("mechanical.fine.aggregate.test",string="Tests")

    # Loose Bulk Density (LBD)

    loose_bulk_name = fields.Char("Name",default="Loose Bulk Density (LBD)")
    loose_bulk_visible = fields.Boolean("Loose Bulk Density (LBD) Visible",compute="_compute_visible")

    weight_empty_bucket = fields.Float(string="Weight of Empty Bucket in kg")
    volume_of_bucket = fields.Float(string="Volume of Bucket in cubic meter")
    sample_plus_bucket = fields.Float(string="[Sample Weight + Bucket  Weight] in kg")
    sample_weight = fields.Float(string="Sample Weight in kg",compute="_compute_sample_weight")
    loose_bulk_density = fields.Float(string="Loose Bulk Density in kg per cubic meter",compute="_compute_loose_bulk_density")


    @api.depends('sample_plus_bucket', 'weight_empty_bucket')
    def _compute_sample_weight(self):
        for record in self:
            record.sample_weight = record.sample_plus_bucket - record.weight_empty_bucket

    

    @api.depends('sample_weight', 'volume_of_bucket')
    def _compute_loose_bulk_density(self):
        for record in self:
            if record.volume_of_bucket:
                record.loose_bulk_density = record.sample_weight / record.volume_of_bucket
            else:
                record.loose_bulk_density = 0.0


     # Rodded Bulk Density (RBD)
    rodded_bulk_name = fields.Char("Name",default="Rodded Bulk Density (RBD)")
    rodded_bulk_visible = fields.Boolean("Loose Bulk Density (LBD) Visible",compute="_compute_visible")

    weight_empty_bucket1 = fields.Float(string="Weight of Empty Bucket in kg")
    volume_of_bucket1 = fields.Float(string="Volume of Bucket in cubic meter")
    sample_plus_bucket1 = fields.Float(string="[Sample Weight + Bucket  Weight] in kg")
    sample_weight1 = fields.Float(string="Sample Weight in kg",compute="_compute_sample_weight1")
    rodded_bulk_density1 = fields.Float(string="Rodded Bulk Density in kg per cubic meter",compute="_compute_rodded_bulk_density")


    @api.depends('sample_plus_bucket1', 'weight_empty_bucket1')
    def _compute_sample_weight1(self):
        for record in self:
            record.sample_weight1 = record.sample_plus_bucket1 - record.weight_empty_bucket1


    @api.depends('sample_weight1', 'volume_of_bucket1')
    def _compute_rodded_bulk_density(self):
        for record in self:
            if record.volume_of_bucket1:
                record.rodded_bulk_density1 = record.sample_weight1 / record.volume_of_bucket1
            else:
                record.rodded_bulk_density1 = 0.0


 
    # Specific Gravity

    specific_gravity_name = fields.Char("Name",default="Specific Gravity")
    specific_gravity_visible = fields.Boolean("Specific Gravity Visible",compute="_compute_visible")

    wt_of_empty_pycnometer = fields.Integer(string="Weight of empty Pycnometer in gms")
    wt_of_pycnometer = fields.Integer(string="Weight of Pycnometer with full of water in gms")
    wt_of_pycnometer_surface_dry = fields.Integer(string="Weight of Pycnometer + Saturated surface dry Aggregate in gms")
    wt_of_pycnometer_surface_dry_water = fields.Integer(string="Weight of Pycnometer + Saturated surface dry Aggregate + Water in gms")
    wt_of_saturated_surface_dry = fields.Integer(string="Weight of Saturated surface dry Aggregate in gms",compute='_compute_wt_of_saturated_surface_dry')
    wt_of_oven_dried = fields.Integer(string="Weight of Oven dried Aggregate in gms")
    volume_of_water = fields.Integer(string="Volume of water displaced by saturated surface dry aggregate",compute="_compute_volume_of_water")
    specific_gravity = fields.Float(string="SPECIFIC GRAVITY", compute="_compute_specific_gravity")
    water_absorption = fields.Float(string="Water Absorption %",compute="_compute_water_absorption")



    @api.depends('wt_of_pycnometer_surface_dry', 'wt_of_empty_pycnometer')
    def _compute_wt_of_saturated_surface_dry(self):
        for line in self:
            line.wt_of_saturated_surface_dry = line.wt_of_pycnometer_surface_dry - line.wt_of_empty_pycnometer


    @api.depends('wt_of_pycnometer', 'wt_of_empty_pycnometer', 'wt_of_pycnometer_surface_dry', 'wt_of_pycnometer_surface_dry_water')
    def _compute_volume_of_water(self):
        for line in self:
            volume_of_water = (line.wt_of_pycnometer - line.wt_of_empty_pycnometer) - (line.wt_of_pycnometer_surface_dry_water - line.wt_of_pycnometer_surface_dry)
            line.volume_of_water = volume_of_water

    @api.depends('wt_of_oven_dried', 'volume_of_water')
    def _compute_specific_gravity(self):
        for line in self:
            if line.volume_of_water:
                line.specific_gravity = line.wt_of_oven_dried / line.volume_of_water
            else:
                line.specific_gravity = 0.0


    @api.depends('wt_of_saturated_surface_dry', 'wt_of_oven_dried')
    def _compute_water_absorption(self):
        for line in self:
            if line.wt_of_oven_dried:
                line.water_absorption = (line.wt_of_saturated_surface_dry - line.wt_of_oven_dried) / line.wt_of_oven_dried * 100
            else:
                line.water_absorption = 0.0



    # Water Absorption

    water_absorption_name = fields.Char("Name",default="Water Absorption")
    water_absorption_visible = fields.Boolean("Water Absorption Visible",compute="_compute_visible")

    wt_of_empty_pycnometer1 = fields.Integer(string="Weight of empty Pycnometer in gms")
    wt_of_pycnometer1 = fields.Integer(string="Weight of Pycnometer with full of water in gms")
    wt_of_pycnometer_surface_dry1 = fields.Integer(string="Weight of Pycnometer + Saturated surface dry Aggregate in gms")
    wt_of_pycnometer_surface_dry_water1 = fields.Integer(string="Weight of Pycnometer + Saturated surface dry Aggregate + Water in gms")
    wt_of_saturated_surface_dry1 = fields.Integer(string="Weight of Saturated surface dry Aggregate in gms",compute='_compute_wt_of_saturated_surface_dry1')
    wt_of_oven_dried1 = fields.Integer(string="Weight of Oven dried Aggregate in gms")
    volume_of_water1 = fields.Integer(string="Volume of water displaced by saturated surface dry aggregate",compute="_compute_volume_of_water1")
    specific_gravity1 = fields.Float(string="SPECIFIC GRAVITY", compute="_compute_specific_gravity1")
    water_absorption1 = fields.Float(string="Water Absorption %",compute="_compute_water_absorption1")



    @api.depends('wt_of_pycnometer_surface_dry1', 'wt_of_empty_pycnometer1')
    def _compute_wt_of_saturated_surface_dry1(self):
        for line in self:
            line.wt_of_saturated_surface_dry1 = line.wt_of_pycnometer_surface_dry1 - line.wt_of_empty_pycnometer1


    @api.depends('wt_of_pycnometer1', 'wt_of_empty_pycnometer1', 'wt_of_pycnometer_surface_dry1', 'wt_of_pycnometer_surface_dry_water1')
    def _compute_volume_of_water1(self):
        for line in self:
            volume_of_water1 = (line.wt_of_pycnometer1 - line.wt_of_empty_pycnometer1) - (line.wt_of_pycnometer_surface_dry_water1 - line.wt_of_pycnometer_surface_dry1)
            line.volume_of_water1 = volume_of_water1

    @api.depends('wt_of_oven_dried1', 'volume_of_water1')
    def _compute_specific_gravity1(self):
        for line in self:
            if line.volume_of_water1:
                line.specific_gravity1 = line.wt_of_oven_dried1 / line.volume_of_water1
            else:
                line.specific_gravity1 = 0.0


    @api.depends('wt_of_saturated_surface_dry1', 'wt_of_oven_dried1')
    def _compute_water_absorption1(self):
        for line in self:
            if line.wt_of_oven_dried1:
                line.water_absorption1 = (line.wt_of_saturated_surface_dry1 - line.wt_of_oven_dried1) / line.wt_of_oven_dried1 * 100
            else:
                line.water_absorption1 = 0.0



    # Sieve Analysis 
    sieve_analysis_name = fields.Char("Name",default="Sieve Analysis")
    sieve_visible = fields.Boolean("Sieve Analysis Visible",compute="_compute_visible")

    sieve_analysis_child_lines = fields.One2many('mechanical.sieve.analysis.line','parent_id',string="Parameter")
    total_sieve_analysis = fields.Integer(string="Total",compute="_compute_total_sieve")
    # cumulative = fields.Float(string="Cumulative",compute="_compute_cumulative")


    def calculate_sieve(self): 
        for record in self:
            for line in record.sieve_analysis_child_lines:
                print("Rows",str(line.percent_retained))
                previous_line = line.serial_no - 1
                if previous_line == 0:
                    if line.percent_retained == 0:
                        # print("Percent retained 0",line.percent_retained)
                        line.write({'cumulative_retained': line.percent_retained})
                        line.write({'passing_percent': 100 })
                    else:
                        # print("Percent retained else",line.percent_retained)
                        line.write({'cumulative_retained': line.percent_retained})
                        line.write({'passing_percent': 100 -line.percent_retained})
                else:
                    previous_line_record = self.env['mechanical.sieve.analysis.line'].search([("serial_no", "=", previous_line),("parent_id","=",self.id)]).cumulative_retained
                    line.write({'cumulative_retained': previous_line_record + line.percent_retained})
                    line.write({'passing_percent': 100-(previous_line_record + line.percent_retained)})
                    print("Previous Cumulative",previous_line_record)
                    

 

    @api.depends('sieve_analysis_child_lines.wt_retained')
    def _compute_total_sieve(self):
        for record in self:
            print("recordd",record)
            record.total_sieve_analysis = sum(record.sieve_analysis_child_lines.mapped('wt_retained'))



    # Soundness Na2SO4
    soundness_na2so4_name = fields.Char("Name",default="Soundness Na2SO4")
    soundness_na2so4_visible = fields.Boolean("Soundness Na2SO4 Visible",compute="_compute_visible")

    soundness_na2so4_child_lines = fields.One2many('mechanical.soundnesss.na2so4.line','parent_id',string="Parameter")
    total_na2so4 = fields.Integer(string="Total",compute="_compute_total_na2so4")
    soundness_na2so4 = fields.Float(string="Soundness",compute="_compute_soundness_na2so4")
    

    @api.depends('soundness_na2so4_child_lines.weight_before_test')
    def _compute_total_na2so4(self):
        for record in self:
            record.total_na2so4 = sum(record.soundness_na2so4_child_lines.mapped('weight_before_test'))
    

    @api.depends('soundness_na2so4_child_lines.cumulative_loss_percent')
    def _compute_soundness_na2so4(self):
        for record in self:
            record.soundness_na2so4 = sum(record.soundness_na2so4_child_lines.mapped('cumulative_loss_percent'))


    # Soundness MgSO4
    soundness_mgso4_name = fields.Char("Name",default="Soundness MgSO4")
    soundness_mgso4_visible = fields.Boolean("Soundness MgSO4 Visible",compute="_compute_visible")

    soundness_mgso4_child_lines = fields.One2many('mechanical.soundnesss.mgso4.line','parent_id',string="Parameter")
    total_mgso4 = fields.Integer(string="Total",compute="_compute_total_mgso4")
    soundness_mgso4 = fields.Float(string="Soundness",compute="_compute_soundness_mgso4")
    
    

    @api.depends('soundness_mgso4_child_lines.weight_before_test')
    def _compute_total_mgso4(self):
        for record in self:
            record.total_mgso4 = sum(record.soundness_mgso4_child_lines.mapped('weight_before_test'))
    

    @api.depends('soundness_mgso4_child_lines.cumulative_loss_percent')
    def _compute_soundness_mgso4(self):
        for record in self:
            record.soundness_mgso4 = sum(record.soundness_mgso4_child_lines.mapped('cumulative_loss_percent'))


      # Deleterious Content

    name_finer75 = fields.Char("Name",default="Finer than 75 micron")
    finer75_visible = fields.Boolean("Finer than 75 micron Visible",compute="_compute_visible")

    wt_sample_finer75 = fields.Float("Weight of Sample in gms")
    wt_dry_sample_finer75 = fields.Float("Weight of dry sample after retained in 75 microns")
    material_finer75 = fields.Float("Material finer than 75 micron in %",compute="_compute_finer75")

    @api.depends('wt_sample_finer75','wt_dry_sample_finer75')
    def _compute_finer75(self):
        for record in self:
            if record.wt_sample_finer75 != 0:
                record.material_finer75 = (record.wt_sample_finer75 - record.wt_dry_sample_finer75)/record.wt_sample_finer75 * 100
            else:
                record.material_finer75 = 0

    
    name_clay_lumps = fields.Char("Name",default="Deleterious content (Clay Lumps)")
    clay_lump_visible = fields.Boolean("Clay Lump Visible",compute="_compute_visible")

    wt_sample_clay_lumps = fields.Float("Weight of Sample in gms")
    wt_dry_sample_clay_lumps = fields.Float("Weight of sample after Removal of Clay Lumps")
    clay_lumps_percent = fields.Float("Clay Lumps in %",compute="_compute_clay_lumps")

    @api.depends('wt_sample_clay_lumps','wt_dry_sample_clay_lumps')
    def _compute_clay_lumps(self):
        for record in self:
            if record.wt_sample_clay_lumps != 0:
                record.clay_lumps_percent = (record.wt_sample_clay_lumps - record.wt_dry_sample_clay_lumps)/record.wt_sample_clay_lumps * 100
            else:
                record.clay_lumps_percent = 0


    name_light_weight = fields.Char("Name",default="Deleterious content (Light weight Particles)")
    light_weight_visible = fields.Boolean("Light Weight Visible",compute="_compute_visible")

    wt_sample_light_weight = fields.Float("Weight of Sample in gms")
    wt_dry_sample_light_weight = fields.Float("Weight of Decanted sample (Light weight particle)")
    light_weight_percent = fields.Float("Light Weight Particle in %",compute="_compute_light_weight")

    @api.depends('wt_sample_light_weight','wt_dry_sample_light_weight')
    def _compute_light_weight(self):
        for record in self:
            if record.wt_sample_light_weight != 0:
                record.light_weight_percent = record.wt_dry_sample_light_weight / record.wt_sample_light_weight * 100
            else:
                record.light_weight_percent = 0



    # Moisture Content

    moisture_content_name = fields.Char("Name",default="Moisture Content")
    moisture_content_visible = fields.Boolean("Moisture Content Visible",compute="_compute_visible")
    
    wt_in_container = fields.Integer(string="Me = weight in g of container filled up to the mark with water")
    wt_in_sample = fields.Integer(string="Ms = weight in g of the sample")
    wt_in_sample_and_container = fields.Integer(string="M = weight in g of the sample and container filled to the mark with water")
    vs = fields.Integer(string="Vs = (Me + Ms) - M",compute="_compute_vs")
    md = fields.Float(string="Md = Specific Gravity")
    vd = fields.Integer(string="Vd = Ms / Md",compute="_compute_vd")
    vdd = fields.Float(string="Vd = (Vs-Vd) / (Ms-Vd)*100",compute="_compute_vdd")


    @api.depends('wt_in_container', 'wt_in_sample', 'wt_in_sample_and_container')
    def _compute_vs(self):
        for record in self:
            record.vs = record.wt_in_container + record.wt_in_sample - record.wt_in_sample_and_container


    @api.depends('wt_in_sample', 'md')
    def _compute_vd(self):
        for record in self:
            if record.md != 0:  # Avoid division by zero
                record.vd = record.wt_in_sample / record.md
            else:
                record.vd = 0.0



    @api.depends('vs', 'vd', 'wt_in_sample')
    def _compute_vdd(self):
        for record in self:
            if record.wt_in_sample != record.vd:  # Avoid division by zero
                record.vdd = ((record.vs - record.vd) / (record.wt_in_sample - record.vd)) * 100
            else:
                record.vdd = 0.0


     ### Compute Visible
    @api.depends('sample_parameters')
    def _compute_visible(self):
        
        for record in self:
            record.loose_bulk_visible = False
            record.rodded_bulk_visible = False
            record.specific_gravity_visible = False
            record.water_absorption_visible = False
            record.sieve_visible = False
            record.soundness_na2so4_visible = False
            record.soundness_mgso4_visible = False

            record.finer75_visible = False
            record.clay_lump_visible = False
            record.light_weight_visible = False
            record.moisture_content_visible = False


            for sample in record.sample_parameters:
                print("Internal Ids",sample.internal_id)
                if sample.internal_id == "a90cdbd7-3fa3-4b83-ae31-9d281767188c":
                    record.loose_bulk_visible = True

                if sample.internal_id == "769b7052-d658-4d14-a5cc-c21dbedeb760":
                    record.rodded_bulk_visible = True

                if sample.internal_id == "7f3b339f-4d39-4c11-94c3-7029e238b76b":
                    record.specific_gravity_visible = True

                if sample.internal_id == "f8088f5b-226c-42ce-a78a-572391879ab4":
                    record.water_absorption_visible = True

                if sample.internal_id == "318d72a1-7188-4086-b132-62b50e63f5d1":
                    record.sieve_visible = True

                if sample.internal_id == "7b921a25-4dc4-4752-a247-d8a223ffbec0":
                    record.soundness_na2so4_visible = True

                if sample.internal_id == "a0e7aaf3-68ff-4e75-830d-91ae04c98f32":
                    record.soundness_mgso4_visible = True


                if sample.internal_id == "237ca3ca-3db7-4782-b863-1dc33be92bc2":
                    record.finer75_visible = True

                if sample.internal_id == "02d32c6b-9881-4152-9e79-9a660e2dda39":
                    record.clay_lump_visible = True

                if sample.internal_id == "c0340cb7-3f4a-4c15-a453-d63694b71f1d":
                    record.light_weight_visible = True

                if sample.internal_id == "d77f5a84-a7b2-47c9-852a-1289ac09ef23":
                    record.moisture_content_visible = True












   






    # ### Compute Visible
    # @api.depends('tests')
    # def _compute_visible(self):
    #     loose_bulk_test = self.env['mechanical.fine.aggregate.test'].search([('name', '=', 'Loose Bulk Density (LBD)')])
    #     rodded_bulk_test = self.env['mechanical.fine.aggregate.test'].search([('name', '=', 'Rodded Bulk Density (RBD)')])
    #     specific_gravity_test = self.env['mechanical.fine.aggregate.test'].search([('name', '=', 'Specific Gravity')])
    #     water_absorption_test = self.env['mechanical.fine.aggregate.test'].search([('name', '=', 'Water Absorption')])
    #     sieve_analysis_test = self.env['mechanical.fine.aggregate.test'].search([('name', '=', 'Sieve Analysis')])
    #     soundness_na2so4_test = self.env['mechanical.fine.aggregate.test'].search([('name', '=', 'Soundness Na2SO4')])
    #     soundness_mgso4_test = self.env['mechanical.fine.aggregate.test'].search([('name', '=', 'Soundness MgSO4')])
    #     finer75_test = self.env['mechanical.fine.aggregate.test'].search([('name', '=', 'Finer than 75 micron')])
    #     clay_lump_test = self.env['mechanical.fine.aggregate.test'].search([('name', '=', 'Deleterious content (Clay Lumps)')])
    #     light_weight_test = self.env['mechanical.fine.aggregate.test'].search([('name', '=', 'Deleterious content (Light weight Particles)')])
    #     moisture_content_test = self.env['mechanical.fine.aggregate.test'].search([('name', '=', 'Moisture Content')])
       
        
    #     for record in self:
    #         record.loose_bulk_visible = False
    #         record.rodded_bulk_visible = False
    #         record.specific_gravity_visible = False
    #         record.water_absorption_visible = False
    #         record.sieve_visible = False
    #         record.soundness_na2so4_visible = False
    #         record.soundness_mgso4_visible = False
    #         record.finer75_visible = False
    #         record.clay_lump_visible = False
    #         record.light_weight_visible = False
    #         record.moisture_content_visible = False
           
           
            
    #         if loose_bulk_test in record.tests:
    #             record.loose_bulk_visible = True

    #         if rodded_bulk_test in record.tests:
    #             record.rodded_bulk_visible = True

    #         if specific_gravity_test in record.tests:
    #             record.specific_gravity_visible = True

    #         if water_absorption_test in record.tests:
    #             record.water_absorption_visible = True

    #         if sieve_analysis_test in record.tests:
    #             record.sieve_visible = True

    #         if soundness_na2so4_test in record.tests:
    #             record.soundness_na2so4_visible = True

    #         if soundness_mgso4_test in record.tests:
    #             record.soundness_mgso4_visible = True

    #         if finer75_test in record.tests:
    #             record.finer75_visible = True

    #         if clay_lump_test in record.tests:
    #             record.clay_lump_visible = True
            
    #         if light_weight_test in record.tests:
    #             record.light_weight_visible = True

    #         if moisture_content_test in record.tests:
    #             record.moisture_content_visible = True

           


            




               


    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(FineAggregate, self).create(vals)
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
        record = self.env['mechanical.fine.aggregate'].browse(self.ids[0])
        field_values = {}
        for field_name, field in record._fields.items():
            field_value = record[field_name]
            field_values[field_name] = field_value

        return field_values




class AggregateFineTest(models.Model):
    _name = "mechanical.fine.aggregate.test"
    _rec_name = "name"
    name = fields.Char("Name")



class SieveAnalysisLine(models.Model):
    _name = "mechanical.sieve.analysis.line"
    parent_id = fields.Many2one('mechanical.fine.aggregate', string="Parent Id")
    
    serial_no = fields.Integer(string="Sr. No", readonly=True, copy=False, default=1)
    sieve_size = fields.Char(string="IS Sieve Size")
    wt_retained = fields.Float(string="Wt. Retained in gms")
    percent_retained = fields.Float(string='% Retained', compute="_compute_percent_retained")
    cumulative_retained = fields.Float(string="Cum. Retained %", compute="_compute_cumulative_retained", store=True)
    passing_percent = fields.Float(string="Passing %")



    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('serial_no'))
                vals['serial_no'] = max_serial_no + 1

        return super(SieveAnalysisLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.serial_no = index + 1

    def write(self, vals):
        # Handle row deletions and adjust serial numbers
        if 'parent_id' in vals or 'wt_retained' in vals:
            for record in self:
                if record.parent_id and record.parent_id == vals.get('parent_id') and 'wt_retained' in vals:
                    record.percent_retained = vals['wt_retained'] / record.parent_id.total * 100 if record.parent_id.total else 0

            new_self = super(SieveAnalysisLine, self).write(vals)

            if 'wt_retained' in vals:
                for record in self:
                    record.parent_id._compute_total()

            return new_self

        return super(SieveAnalysisLine, self).write(vals)

    def unlink(self):
        # Get the parent_id before the deletion
        parent_id = self[0].parent_id

        res = super(SieveAnalysisLine, self).unlink()

        if parent_id:
            parent_id.sieve_analysis_child_lines._reorder_serial_numbers()

        return res


    @api.depends('wt_retained', 'parent_id.total_sieve_analysis')
    def _compute_percent_retained(self):
        for record in self:
            try:
                record.percent_retained = record.wt_retained / self.parent_id.total_sieve_analysis * 100
            except ZeroDivisionError:
                record.percent_retained = 0


    @api.depends('cumulative_retained')
    def _compute_cum_retained(self):
        self.cumulative_retained=0
        


    def get_previous_record(self):
        for record in self:
            # import wdb; wdb.set_trace()
            sorted_lines = sorted(record.parent_id.sieve_analysis_child_lines, key=lambda r: r.id)
            # index = sorted_lines.index(record)
            # print("Working")


class SoundnessNa2Line(models.Model):
    _name = "mechanical.soundnesss.na2so4.line"
    parent_id = fields.Many2one('mechanical.fine.aggregate', string="Parent Id")
    
    sieve_size_passing = fields.Char(string="Sieve Size Passing")
    sieve_size_retained = fields.Char(string="Sieve Size Retained")
    weight_before_test = fields.Float(string="Weight of test fraction before test in gm.")
    weight_after_test = fields.Float(string="Weight of test feaction Passing Finer Sieve After test")
    grading_original_sample = fields.Float(string="Grading of Original sample in %", compute="_compute_grading")
    passing_percent = fields.Float(string="Percentage Passing Finer Sieve After test (Percentage Loss)",compute="_compute_passing_percent")
    cumulative_loss_percent = fields.Float(string="Commulative percentage Loss",compute="_compute_cumulative1")
    
    @api.depends('parent_id.total_na2so4','weight_before_test')
    def _compute_grading(self):
        for record in self:
            try:
                record.grading_original_sample = (record.weight_before_test/record.parent_id.total_na2so4)*100
            except ZeroDivisionError:
                record.grading_original_sample = 0

    @api.depends('weight_before_test','weight_after_test')
    def _compute_passing_percent(self):
        for record in self:
            try:
                record.passing_percent = (record.weight_after_test / record.weight_before_test)*100
            except:
                record.passing_percent = 0

    @api.depends('weight_after_test', 'parent_id.total_na2so4')
    def _compute_cumulative1(self):
        for record in self:
            try:
                record.cumulative_loss_percent = (record.weight_after_test / record.parent_id.total_na2so4) * 100
            except:
                record.cumulative_loss_percent = 0


class SoundnessMgLine(models.Model):
    _name = "mechanical.soundnesss.mgso4.line"
    parent_id = fields.Many2one('mechanical.fine.aggregate', string="Parent Id")
    
    sieve_size_passing = fields.Char(string="Sieve Size Passing")
    sieve_size_retained = fields.Char(string="Sieve Size Retained")
    weight_before_test = fields.Float(string="Weight of test fraction before test in gm.")
    weight_after_test = fields.Float(string="Weight of test feaction Passing Finer Sieve After test")
    grading_original_sample = fields.Float(string="Grading of Original sample in %", compute="_compute_grading")
    passing_percent = fields.Float(string="Percentage Passing Finer Sieve After test (Percentage Loss)",compute="_compute_passing_percent")
    cumulative_loss_percent = fields.Float(string="Commulative percentage Loss",compute="_compute_cumulative")
    
    @api.depends('parent_id.total_mgso4','weight_before_test')
    def _compute_grading(self):
        for record in self:
            try:
                record.grading_original_sample = (record.weight_before_test/record.parent_id.total_mgso4)*100
            except ZeroDivisionError:
                record.grading_original_sample = 0

    @api.depends('weight_before_test','weight_after_test')
    def _compute_passing_percent(self):
        for record in self:
            try:
                record.passing_percent = (record.weight_after_test / record.weight_before_test)*100
            except:
                record.passing_percent = 0

    @api.depends('weight_after_test', 'parent_id.total_mgso4')
    def _compute_cumulative(self):
        for record in self:
            try:
                record.cumulative_loss_percent = (record.weight_after_test / record.parent_id.total_mgso4) * 100
            except:
                record.cumulative_loss_percent = 0





