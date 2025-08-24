from django.utils.translation import gettext_lazy as _


PROVINCE_CHOICES = [
    ('Tehran', _('Tehran')),
    ('Alborz', _('Alborz')),
    ('Fars', _('Fars')),
    ('Khorasan_Razavi', _('Khorasan Razavi')),
    ('Kermanshah', _('Kermanshah')),
    ('Isfahan', _('Isfahan')),
    ('Yazd', _('Yazd')),
    ('Hamedan', _('Hamedan')),
    ('Kerman', _('Kerman')),
    ('Khuzestan', _('Khuzestan')),
    ('Gilan', _('Gilan')),
    ('Mazandaran', _('Mazandaran')),
    ('Zanjan', _('Zanjan')),
    ('Golestan', _('Golestan')),
    ('Bushehr', _('Bushehr')),
    ('Semnan', _('Semnan')),
    ('Ardebil', _('Ardebil')),
    ('Qazvin', _('Qazvin')),
    ('Qom', _('Qom')),
    ('South_Khorasan', _('South Khorasan')),
    ('North_Khorasan', _('North Khorasan')),
    ('Markazi', _('Markazi')),
    ('Kohgiluyeh_Boyerahmad', _('Kohgiluyeh and Boyerahmad')),
    ('Chaharmahal_Bakhtiari', _('Chaharmahal and Bakhtiari')),
    ('Ilam', _('Ilam')),
    ('West_Azerbaijan', _('West Azerbaijan')),
    ('East_Azerbaijan', _('East Azerbaijan')),
    ('Lorestan', _('Lorestan')),
    ('Sistan_Baluchestan', _('Sistan and Baluchestan')),
    ('Hormozgan', _('Hormozgan')),
]

ORDER_STATUS = [
    ('pending', _('Pending')),
    ('processing', _('Processing')),
    ('shipped', _('Shipped')),
    ('delivered', _('Delivered')),
    ('cancelled', _('Cancelled')),
    ('returned', _('Returned')),
]
