# purchase_fast_receive/__manifest__.py
{
    'name': 'Purchase Fast Receive',
    'version': '1.0',
    'summary': 'Tek tıkla satın alma siparişi onayla ve ürünleri depoya al',
    'category': 'Purchases',
    'author': 'Senin İsmin',
    'depends': ['purchase', 'stock'],
    'data': [
        'views/purchase_order_view.xml',
    ],
    'installable': True,
    'application': False,
}
