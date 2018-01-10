EVAN = 'Evan'
CHALIE = 'Chalie'
JOHN = 'John'
BARRY = 'Barry'
SERVICE = 'Service'
JAKE = 'Jake'
COREY = 'Corey'
CHRIS = 'Chris'
SUB = 'Sub'

NOTAPP = 'NA'
ANGIESLIST = 'AL'
CONTRACTOR = 'CO'
GOOGLE = 'GO'
OLDCUST = 'OC'
OTHER = 'OT'
RECCO = 'RC'
REALTOR = 'RE'
WEBSITE = 'WS'
YELP = 'YL'

SOURCE_CHOICES = (
    (NOTAPP, 'Not Applicable'),
    (ANGIESLIST, 'Angie\'s List'),
    (CONTRACTOR, 'Contractor'),
    (GOOGLE, 'Google'),
    (OLDCUST, 'Old Customer'),
    (OTHER, 'Other'),
    (RECCO, 'Recco'),
    (REALTOR, 'Realtor'),
    (WEBSITE, 'Website'),
    (YELP, 'Yelp'),
)


LEAD_ASSIGNED_CHOICES = (
    (EVAN, 'Evan'),
    (CHALIE, 'Chalie'),
    (JOHN, 'John'),
    (BARRY, 'Barry'),
    (SERVICE, 'Service'),
)

JOB_ASSIGNED_CHOICES = (
    (EVAN, 'Evan'),
    (CHALIE, 'Chalie'),
    (JOHN, 'John'),
    (BARRY, 'Barry'),
    (SERVICE, 'Service'),
    (JAKE, 'Jake'),
    (COREY, 'Corey'),
    (CHRIS, 'Chris'),
    (SUB, 'Sub'),
)


t0810 = '8:00-10:00'
t0911 = '9:00-11:00'
t1012 = '10:00-12:00'
t1113 = '11:00-1:00'
t1214 = '12:00-2:00'
t1315 = '1:00-3:00'
t1416 = '2:00-4:00'

TIME_SLOTS = (
    (t0810, u'8-10'),
    (t0911, u'9-11'),
    (t1012, u'10-12'),
    (t1113, u'11-1'),
    (t1214, u'12-2'),
    (t1315, u'1-3'),
    (t1416, u'2-4')
)



estimate = 'Estimate'
service = 'Service'
inspection = 'Inspection'

TITLES = {
    (estimate,'Estimate'),
    (service,'Service'),
    (inspection,'Inspection')
}
