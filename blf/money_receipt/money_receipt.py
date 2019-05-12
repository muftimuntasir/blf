# Author Mufti Muntasir Ahmed 11-05-2019


from openerp.osv import osv, fields
from openerp import SUPERUSER_ID, api
from openerp.tools.translate import _
from datetime import datetime



class  MoneyReceipt(osv.osv):
    _name = 'money.receipt'
    _description = "Money Receipt List"

    _columns = {
        'date': fields.datetime('Date', required=True, select=True, copy=False),
        'description': fields.char('Received With Thanks From'),
        'cash_po': fields.char('Cash/P.O./D.D. No'),
        'deposit_to': fields.many2one('account.account', 'Deposit To', required=True),
        'towards_to': fields.many2one('account.account', 'Towards To', required=True),
        'amount': fields.float('Amount', required=True),
        'create_date': fields.datetime('Creation Date', readonly=True, select=True,
                                       help="Date on which Receipt is created."),

        'date_confirm': fields.datetime('Confirmation Date', readonly=True, select=True,
                                    help="Date on which sales order is confirmed.", copy=False),
        'user_id': fields.many2one('res.users', 'Assigned to', select=True, track_visibility='onchange'),

        'state': fields.selection([
            ('pending', 'Pending'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),

        ], 'Status', readonly=True, copy=False, help="Gives the status of the Money Receipt", select=True),

    }

    _defaults = {
        'user_id': lambda obj, cr, uid, context: uid,
        'state': 'pending',

    }


    def make_confirm(self, cr, uid, ids, context=None):

        id_list = ids

        for element in id_list:
            ids = [element]

            if ids is not None:
                cr.execute("update money_receipt set state='done' where id=%s", (ids))
                cr.commit()

        return 'True'

    def make_cancel(self, cr, uid, ids, context=None):
        id_list = ids
        for element in id_list:
            ids = [element]

            if ids is not None:
                cr.execute("update money_receipt set state='cancel' where id=%s", (ids))
                cr.commit()

        return 'True'

    def write(self, cr, uid, ids, vals, context=None):
        cr.execute("select state from  money_receipt where id=%s", (ids))
        result_list = cr.fetchall()

        for item in result_list:
            if str(item[0]) == 'done' or str(item[0]) == 'cancel':
                raise osv.except_osv(_('Message'), _("Sorry You Can not Edit it. Because it is already confirmed/Cancelled."))
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = super(MoneyReceipt, self).write(cr, uid, ids, vals, context=context)
        return res

