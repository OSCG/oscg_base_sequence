# -*- coding: utf-8 -*-

import time
from openerp import tools
from datetime import datetime
from openerp.osv import fields, osv
from openerp.tools.translate import _
import logging
from openerp.tools import ustr
from openerp import SUPERUSER_ID


_logger = logging.getLogger(__name__)

class sequence_select_year(osv.osv_memory):
    _name = "sequence.select.year"
    _columns = {
        'year':fields.selection([('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), 
        ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'),
        ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), 
        ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030'), ('2031', '2031'),
        ('2032', '2032'), ('2033', '2033'), ('2034', '2034'), ('2035', '2035'), ('2036', '2036'), ('2037', '2037'),
        ('2038', '2038'), ('2039', '2039'), ('2040', '2040'), ('2041', '2041'), ('2042', '2042'), ('2043', '2043'), 
        ('2044', '2044'), ('2045', '2045'), ('2046', '2046'), ('2047', '2047'), ('2048', '2048'), ('2049', '2049'), 
        ('2050', '2050')],'Year'),
    }

    def create_sequence_month(self, cr, uid, ids, context=None):
        year = self.read(cr,uid,ids,['year'])[0]['year']
        active_model = context.get('active_model','')
        active_id = context.get('active_id',False)
        if active_model and active_id:
            model_obj = self.pool.get(active_model).browse(cr,uid,active_id)
            for ms in model_obj.month_sequences:
                if ms.month and ms.month[:4] == year:
                    raise osv.except_osv(_('Warning'), _('This year has been generated sequence!'))
            result = []
            for i in range(1,13):
                if i < 10:result.append((0,0,{'month':'%s0%s'%(year,i),'next_number':1}))
                else:result.append((0,0,{'month':'%s%s'%(year,i),'next_number':1}))
            self.pool.get(active_model).write(cr,uid,active_id,{'month_sequences':result})
        return {'type': 'ir.actions.act_window_close'}

class month_sequence(osv.osv):
    _name = "month.sequence"
    _columns = {
        'month':fields.char('Month',size=64,readonly=True),
        'next_number':fields.integer('Next Number'),
        'sequence_id':fields.many2one('ir.sequence','Sequence'),
    }
    _defaults = {
        'next_number':1,
    }

class ir_sequence(osv.osv):
    _inherit = "ir.sequence"
    _columns = {
        'by_date':fields.boolean('Sequence By Date'),
        'latest_date':fields.date('Latest Date'),
        'by_month':fields.boolean('Month Sequence'),
        'month_sequences':fields.one2many('month.sequence','sequence_id','Month Sequence'),
    }
    _defaults={
        'latest_date':time.strftime('%Y-%m-%d')
    }
    def _next(self, cr, uid, seq_ids, context=None):
        if context is None:context = {}
        if not seq_ids:
            return False
        seq_obj = self.browse(cr,uid,seq_ids[0])
        if seq_obj.by_date and seq_obj.latest_date != time.strftime('%Y-%m-%d'):
            self.write(cr,SUPERUSER_ID,seq_ids,{'number_next':1,'latest_date':time.strftime('%Y-%m-%d')})
            return super(ir_sequence,self)._next(cr, uid, seq_ids, context=context)
        if seq_obj.by_month and not context.get('seq_month',False):
            raise osv.except_osv(_('Warning'), _('No Month Sequence Key：seq_month!'))
        if seq_obj.by_month and context.get('seq_month',False):
            force_company = context.get('force_company')
            if not force_company:
                force_company = self.pool.get('res.users').browse(cr, uid, uid).company_id.id
            sequences = self.read(cr, uid, seq_ids, ['name','company_id','implementation','prefix','suffix','padding'])
            preferred_sequences = [s for s in sequences if s['company_id'] and s['company_id'][0] == force_company ]
            seq = preferred_sequences[0] if preferred_sequences else sequences[0]
            for m in seq_obj.month_sequences:
                if m.month == context['seq_month']:
                    seq['number_next'] = m.next_number
                    self.pool.get('month.sequence').write(cr,SUPERUSER_ID,m.id, {'next_number':m.next_number+seq_obj.number_increment})
                    break
            if not seq.get('number_next',False):
                raise osv.except_osv(_('Warning'), _('No month of Month Sequence Key value %s!'%context['seq_month']))
            d = self._interpolation_dict()
            d["year_acc"] = context['seq_month'][:4]
            d["month_acc"] = context['seq_month'][4:]
            try:
                interpolated_prefix = self._interpolate(seq['prefix'], d)
                interpolated_suffix = self._interpolate(seq['suffix'], d)
            except ValueError:
                raise osv.except_osv(_('Warning'), _('Invalid prefix or suffix for sequence \'%s\'') % (seq.get('name')))
            return interpolated_prefix + '%%0%sd' % seq['padding'] % seq['number_next'] + interpolated_suffix
        return super(ir_sequence,self)._next(cr, uid, seq_ids, context=context)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
