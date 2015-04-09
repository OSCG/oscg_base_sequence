# -*- encoding: utf-8 -*-
#2）序号前缀的变量，增加year_acc和month_acc变量，该二变量将从Context中取得seq_month，取seq_month的前4位作为年，后二位作为月。
{
    'name': 'Month Sequence',
    'version': '1.0',
    "category" : "Hidden",
    'description': """
In order to facilitate the work of the financial sector, we increased the number management capabilities to manage the work of the usual financial year, so let financial management usually becomes more clear.    1）在系统的Sequence (ir.sequence)基础上，添加按日重置序号（Sequence By Date），和按月取序号（Month Sequence）的功能。
It adds two functions under Settings——>Technical——>Sequence & Identifiers——>Sequence.
    1.In the system of Sequence (in.sequence), based on the number added daily reset (Sequence By Date), and a monthly take numbers function(Month Sequence)
    2.Variable number prefix, and increased year_acc and month _cc variables, the two variables will get seq_month Context, the first of four taking seq_month as years, after a two as months.
    3.You are free to manage the year of Accounting, make your financial work more clear.
    """,
    'author': 'OSCG',
    'depends': ['base'],
    'init_xml': [],
    'update_xml': ['oscg_sequence.xml','security/ir.model.access.csv'],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
