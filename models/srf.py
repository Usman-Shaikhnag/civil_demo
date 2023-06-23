from odoo import api, fields, models
from odoo.exceptions import UserError

class Discipline(models.Model):
    _name = "lerm_civil.discipline"
    _description = "Lerm Discipline"
    _rec_name = 'discipline'

    discipline = fields.Char(string="Discipline", required=True)
    hod = fields.Many2one('res.users',string="Head of Department")

    def __str__(self):
        return self.discipline

class Group(models.Model):
    _name = "lerm_civil.group"
    _description = "Lerm Group"
    _rec_name = 'group'

    discipline = fields.Many2one('lerm_civil.discipline', string="Discipline", required=True)
    group = fields.Char(string="Group", required=True)


    def __str__(self):
        return self.group
    

class TestMethod(models.Model):
    _name = "lerm_civil.test_method"
    _description = "Lerm Test Method"
    _rec_name = 'test_method'

    test_method = fields.Char(string="Test Method", required=True)


    def __str__(self):
        return self.test_method


class SrfForm(models.Model):
    _name = "lerm.civil.srf"
    _description = "SRF"
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'srf_id'

    srf_id = fields.Char(string="SRF ID" , readonly=True)
    kes_number = fields.Char(string="KES No" , readonly=True)
    # job_no = fields.Char(string="Job NO.")
    srf_date = fields.Date(string="SRF Date")
    job_date = fields.Date(string="JOB Date")
    customer = fields.Many2one('res.partner',string="Customer")
    billing_customer = fields.Many2one('res.partner',string="Billing Customer")
    contact_person = fields.Many2one('res.partner',string="Contact Person")
    client = fields.Char("Client")
    site_address = fields.Many2one('res.partner',string="Site Address")
    name_work = fields.Many2one('res.partner.project',string="Name of Work")
    client_refrence = fields.Char(string="Client Reference Letter")
    samples = fields.One2many('lerm.srf.sample' , 'srf_id' , string="Samples")
    contact_other_ids = fields.Many2many('res.partner',string="Other Ids",compute="compute_other_ids")
    contact_contact_ids = fields.Many2many('res.partner',string="Contact Ids",compute="compute_contact_ids")
    contact_site_ids = fields.Many2many('res.partner',string="Site Ids",compute="compute_site_ids")
    attachment = fields.Binary(string="Attachment")
    attachment_name = fields.Char(string="Attachment Name")
    state = fields.Selection([
        ('1-draft', 'Draft'),
        ('2-confirm', 'Confirm')
    ], string='State', default='1-draft')
    sample_count = fields.Integer(string="Sample Count", compute='compute_sample_count')
    eln_count = fields.Integer(string="ELN Count", compute='compute_eln_count')
    sample_range_table = fields.One2many('sample.range.line','srf_id',string="Sample Range")
    

    def action_srf_sent_mail(self):

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new'
        }


    def sample_count_button(self):
        return {
        'name': 'Sample',
        'domain': [('srf_id', '=', self.id)],
        'view_type': 'form',
        'res_model': 'lerm.srf.sample',
        'view_id': False,
        'view_mode': 'tree,form',
        'type': 'ir.actions.act_window'
    }
    def compute_eln_count(self):
        count = self.env['lerm.eln'].search_count([('srf_id', '=', self.id)])
        self.eln_count = count

    @api.onchange('customer')
    def compute_client(self):
        for record in self:
            if record.customer:
                self.client = self.env['res.partner'].search([("id","=",self.customer.id)]).consultant



    def eln_count_button(self):
        return {
        'name': 'ELN',
        'domain': [('srf_id', '=', self.id)],
        'view_type': 'form',
        'res_model': 'lerm.eln',
        'view_id': False,
        'view_mode': 'tree,form',
        'type': 'ir.actions.act_window'
    }
    def compute_sample_count(self):
        count = self.env['lerm.srf.sample'].search_count([('srf_id', '=', self.id)])
        self.sample_count = count

    def confirm_srf(self):
        srf_ids=[]

        for record in self.sample_range_table:
            sam_next_number = self.env['ir.sequence'].search([('code','=','lerm.srf.sample')]).number_next_actual
            kes_next_number = self.env['ir.sequence'].search([('code','=','lerm.srf.sample.kes')]).number_next_actual
            
            sample_range = "SAM/"+str(sam_next_number)+"-"+str(sam_next_number+record.sample_qty-1)
            kes_range = "KES/"+str(kes_next_number)+"-"+str(kes_next_number+record.sample_qty-1)
            record.write({'sample_range': sample_range , 'kes_range': kes_range })
            samples = self.env['lerm.srf.sample'].search([('sample_range_id','=',record.id)])
            # import wdb ; wdb.set_trace()
            for sample in samples:
                sample_id = self.env['ir.sequence'].next_by_code('lerm.srf.sample') or 'New'
                kes_no = self.env['ir.sequence'].next_by_code('lerm.srf.sample.kes') or 'New'
                sample.write({'sample_no':sample_id,'kes_no':kes_no,'status':'2-confirmed'})
                self.env.cr.commit()




        # for record in self.samples:
        #     # if vals.get('sample_no', 'New') == 'New' and vals.get('kes_no', 'New') == 'New':
        #     sample_id = self.env['ir.sequence'].next_by_code('lerm.srf.sample') or 'New'
        #     kes_no = self.env['ir.sequence'].next_by_code('lerm.srf.sample.kes') or 'New'
        #     # res = super(LermSampleForm, self).create(vals)
        #     #     return res
        #     record.write({'status':'2-confirmed','sample_no':sample_id,'kes_no':kes_no})
        #     srf_ids.append(sample_id)
        #     if len(srf_ids) == 1:
        #         srfidstring = srf_ids[0]
        #     else:
        #         srfidstring = str(srf_ids[0])+'/'+str(srf_ids[-1])
            
        # Extracting the numbers from the original string
        # numbers = srfidstring.split("/")

        # # Formatting the numbers in the desired format
        # formatted_numbers = "-".join([f"{int(num):05d}" for num in numbers])

        # Creating the modified string
        # import wdb; wdb.set_trace()
        first_sample_range = self.sample_range_table[0].kes_range
        last_sample_range = self.sample_range_table[-1].kes_range  
        first_samplerange_slash_index = first_sample_range.find("/")
        srffirstnumber_str = first_sample_range[first_samplerange_slash_index+1:first_sample_range.find("-")]
        last_sample_range_index = last_sample_range.find("-")
        srf_last_number = last_sample_range[last_sample_range_index+1:]

      
        modified_srf_id = f"SRF/"+srffirstnumber_str+"-"+srf_last_number
        modified_kes_number = f"KES/DUS"
        self.write({'srf_id': modified_srf_id})
        self.write({'kes_number': modified_kes_number})
        self.write({'state': '2-confirm'})
        # for record in self:

    # name_of_work = fields.Many2one('res.partner.project',string='Name of Work')

    @api.depends('customer')
    def compute_contact_ids(self):
        for record in self:
            contact_ids = self.env['res.partner'].search([('parent_id', '=', record.customer.id),('type','=','contact')])
            record.contact_contact_ids = contact_ids

    @api.depends('customer')
    def compute_other_ids(self):
        for record in self:
            contact_ids = self.env['res.partner'].search([('parent_id', '=', record.customer.id),('type','=','other')])
            record.contact_other_ids = contact_ids

    @api.depends('customer')
    def compute_site_ids(self):
        for record in self:
            contact_ids = self.env['res.partner'].search([('parent_id', '=', record.customer.id),('type','=','delivery')])
            record.contact_site_ids = contact_ids
    
    def open_sample_add_wizard(self):

        samples = self.env["lerm.srf.sample"].search([("srf_id","=",self.id)])
        # print("Samples "+ str(samples))


        action = self.env.ref('lerm_civil.srf_sample_wizard_form')
        if len(samples) > 0:
            print(samples[0].material_id.id , 'error')
            discipline_id = samples[-1].discipline_id.id
            material_id = samples[-1].material_id.id
            group_id = samples[-1].group_id.id
            alias = samples[-1].alias
            brand = samples[-1].brand
            size_id = samples[-1].size_id.id
            grade_id = samples[-1].grade_id.id
            sample_received_date = samples[-1].sample_received_date
            location = samples[-1].location
            sample_condition = samples[-1].sample_condition
            sample_reject_reason = samples[-1].sample_reject_reason
            witness = samples[-1].witness
            scope = samples[-1].scope
            sample_description = samples[-1].sample_description
            sample_received_date = self.srf_date

            return {
            'name': "Add Sample",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.srf.sample.wizard',
            'view_id': action.id,
            'target': 'new',
            'context': {
            # 'default_discipline_id' : discipline_id,
            'default_material_id' : material_id,
            'default_alias':alias,
            'default_brand':brand,
            'default_size_id':size_id,
            'default_grade_id':grade_id,
            'default_sample_received_date': sample_received_date,
            'default_location':location,
            'default_sample_condition':sample_condition,
            'default_sample_reject_reason':sample_reject_reason,
            'default_witness':witness,
            'default_scope':scope,
            'default_sample_description':sample_description,
            'default_group_id':group_id,
            'default_sample_received_date':sample_received_date
            }
        }
        else:
            return {
            'name': "Add Sample",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.srf.sample.wizard',
            'view_id': action.id,
            'target': 'new'
            }


    def open_new_sample_add_wizard(self):
        samples = self.env["lerm.srf.sample"].search([("srf_id","=",self.id)])
        action = self.env.ref('lerm_civil.srf_sample_wizard_form')
        return {
            'name': "Add Sample",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.srf.sample.wizard',
            'view_id': action.id,
            'target': 'new',
            'context':{
                'default_customer_id': self.customer.id,
                'default_sample_received_date':self.srf_date
            }
            }




class CreateSampleWizard(models.TransientModel):
    _name = 'create.srf.sample.wizard'
    
    srf_id = fields.Many2one('lerm.civil.srf' , string="Srf Id")
    sample_id = fields.Char(string="Sample Id")
    casting = fields.Boolean(string="Casting")
    discipline_id = fields.Many2one('lerm_civil.discipline',string="Discipline")
    group_id = fields.Many2one('lerm_civil.group',string="Group")
    material_id = fields.Many2one('product.template',string="Material")
    brand = fields.Char(string="Brand")
    size_id = fields.Many2one('lerm.size.line',string="Size")
    size_ids = fields.Many2many('lerm.size.line',string="Size")
    grade_id = fields.Many2one('lerm.grade.line',string="Grade")
    grade_ids = fields.Many2many('lerm.grade.line',string="Grades")
    # qty_id = fields.Many2one('lerm.qty.line',string="Quantity")
    # qty_id = fields.Integer(string="Sample Quantity")
    sample_qty = fields.Integer(string="Sample Quantity",default=1)
    received_by_id = fields.Many2one('res.users',string="Received By",default=lambda self: self.env.user)
    sample_received_date = fields.Date(string="Sample Received Date")
    sample_condition = fields.Selection([
        ('satisfactory', 'Satisfactory'),
        ('non_satisfactory', 'Non-Satisfactory'),
    ], string='Sample Condition', default='satisfactory')
    location = fields.Char(string="Location")
    sample_reject_reason = fields.Char(string="Sample Reject Reason")
    witness = fields.Char(string="Witness")
    scope = fields.Selection([
        ('nabl', 'NABL'),
        ('non_nabl', 'Non-NABL'),
    ], string='Scope', default='nabl')
    sample_description = fields.Text(string="Sample Description")
    group_ids = fields.Many2many('lerm_civil.group',string="Group Ids")
    material_ids = fields.Many2many('product.template',string="Material Ids")
    client_sample_id = fields.Char(string="Client Sample Id")
    # size_ids = fields.Many2many('lerm.size.line',string="Size Ids")
    # grade_ids = fields.Many2many('lerm.grade.line',string="Grade Ids")
    # qty_ids = fields.Many2many('lerm.qty.line',string="Qty Ids")
    days_casting = fields.Selection([
        ('3', '3 Days'),
        ('7', '7 Days'),
        ('14', '14 Days'),
        ('28', '28 Days'),
    ], string='Days of casting', default='3')
    date_casting = fields.Date(string="Date of Casting")
    customer_id = fields.Many2one('res.partner' , string="Customer")
    alias = fields.Char(string="Alias")
    parameters = fields.Many2many('lerm.parameter.master',string="Parameter")

    @api.onchange('material_id')
    def compute_grade(self):
        for record in self:
            if record.material_id:
                record.grade_ids = self.env['product.template'].search([('id','=', record.material_id.id)]).grade_table
    

    @api.onchange('material_id')
    def compute_size(self):
        for record in self:
            if record.material_id:
                record.size_ids = self.env['product.template'].search([('id','=', record.material_id.id)]).size_table

    @api.onchange('material_id')
    def compute_parameters(self):
        for record in self:
            if record.material_id:
                parameters_ids = []
                product_records = self.env['product.template'].search([('id','=', record.material_id.id)]).parameter_table1
                for rec in product_records:
                    parameters_ids.append(rec.id)
                domain = {'parameters': [('id', 'in', parameters_ids)]}
                return {'domain': domain}
            else:
                domain = {'parameters': [('id', 'in', [])]}
                return {'domain': domain}


    @api.onchange('discipline_id')
    def compute_group_ids(self):
        for record in self:
            group_ids = self.env['lerm_civil.group'].search([('discipline','=', record.discipline_id.id)])
            record.group_ids = group_ids

    @api.onchange('discipline_id' , 'group_id')
    def compute_material_ids(self):
        for record in self:
            if record.discipline_id and record.group_id:
                material_ids = self.env['product.template'].search([('discipline','=', record.discipline_id.id) , ('group','=', record.group_id.id)])
                record.material_ids = material_ids
            else:
                record.material_ids = None

    @api.onchange('material_id.alias' ,'customer_id', 'material_id')
    def onchange_material_id(self):
        for record in self:
            result = self.env['lerm.alias.line'].search([('customer', '=', record.customer_id.id),('product_id', '=', record.material_id.id)])
            print(result)
            record.alias = result.alias
       
   

    def add_sample(self):
        group_id =  self.group_id.id
        alias = self.alias
        material_id = self.material_id.id
        size_id = self.size_id.id
        brand = self.brand
        grade_id = self.grade_id.id
        sample_received_date = self.sample_received_date
        location = self.location
        sample_condition = self.sample_condition
        sample_reject_reason = self.sample_reject_reason
        witness = self.witness
        discipline_id = self.discipline_id.id
        scope = self.scope
        sample_description =self.sample_description
        parameters = self.parameters
        discipline_id = self.discipline_id
        casting = self.casting
        sample_qty = self.sample_qty
        client_sample_id = self.client_sample_id

        srf_ids = []
        #     for i in range(1, self.qty_id + 1):
        #         srf_number = str(i).zfill(4)  # Pad the number with leading zeros
        #         srf_id = f"SRF/{srf_number}-{str(self.qty_id).zfill(4)}"
        #         srf_ids.append(srf_id)

        if self.sample_qty > 0:

            sample_range = self.env['sample.range.line'].create({
                'srf_id': self.env.context.get('active_id'),
                'group_id':group_id,
                'alias':alias,
                'discipline_id': discipline_id,
                'material_id' : self.material_id.id,
                'size_id':size_id,
                'brand':brand,
                'grade_id':grade_id,
                'sample_received_date':sample_received_date,
                'location':location,
                'sample_condition':sample_condition,
                'sample_reject_reason':sample_reject_reason,
                'witness':witness,
                'scope':scope,
                'sample_description':sample_description,
                'parameters':parameters,
                'discipline_id':discipline_id.id,
                'casting':casting,
                'sample_qty':sample_qty,
                'client_sample_id':client_sample_id,
                'casting_date':self.date_casting
            })
            for i in range(self.sample_qty):
                self.env["lerm.srf.sample"].create({
                    'srf_id': self.env.context.get('active_id'),
                    'group_id':group_id,
                    'alias':alias,
                    'discipline_id': discipline_id,
                    'material_id' : self.material_id.id,
                    'size_id':size_id,
                    'brand':brand,
                    'grade_id':grade_id,
                    'sample_received_date':sample_received_date,
                    'location':location,
                    'sample_condition':sample_condition,
                    'sample_reject_reason':sample_reject_reason,
                    'witness':witness,
                    'scope':scope,
                    'sample_description':sample_description,
                    'parameters':parameters,
                    'discipline_id':discipline_id.id,
                    'casting':casting,
                    'sample_range_id':sample_range.id,
                    'client_sample_id':client_sample_id,
                    'casting_date':self.date_casting,
                    'days_casting':self.days_casting,
                    'casting':self.casting
                })

            

        


            print("Parameters "+ str(self.parameters))

            return {'type': 'ir.actions.act_window_close'}
        else:
            raise UserError("Sample Quantity Must be Greater Than Zero")

    def close_sample_wizard(self):
        return {'type': 'ir.actions.act_window_close'}

    
    class AllotSampleWizard(models.TransientModel):
        _name = "sample.allotment.wizard"

        technicians = fields.Many2one("res.users",string="Technicians")


        @api.onchange('technicians')
        def onchange_technicians(self):
            users = self.env.ref('lerm_civil.kes_technician_access_group').users
            ids = []
            for user_id in users:
                ids.append(user_id.id)
            print("IDS " + str(ids))
            return {'domain': {'technicians': [('id', 'in', ids)]}}
        

        # @api.one
        def allot_sample(self):
            # import wdb;wdb.set_trace()

            active_ids = self.env.context.get('active_ids')
            for id in active_ids:
                parameters = []
                parameters_result = []

                sample = self.env['lerm.srf.sample'].sudo().search([('id','=',id)])
                if sample.state == '1-allotment_pending':
                    for parameter in sample.parameters:
                        parameters.append((0,0,{'parameter':parameter.id ,'spreadsheet_template':parameter.spreadsheet_template.id}))
                        parameters_result.append((0,0,{'parameter':parameter.id,'unit': parameter.unit.id,'test_method':parameter.test_method.id}))
                    self.env['lerm.eln'].sudo().create({
                        'srf_id': sample.srf_id.id,
                        'srf_date':sample.srf_id.srf_date,
                        'kes_no':sample.kes_no,
                        'discipline':sample.discipline_id.id,
                        'group': sample.group_id.id,
                        'material': sample.material_id.id,
                        'witness_name': sample.witness,
                        'sample_id':sample.id,
                        'parameters':parameters,
                        'technician': self.technicians.id,
                        'parameters_result':parameters_result
                    })

                    sample.write({'state':'2-alloted' , 'technicians':self.technicians.id})
                else:
                    pass

         
            return {'type': 'ir.actions.act_window_close'}


        def close_allotment_wizard(self):
            return {'type': 'ir.actions.act_window_close'}


