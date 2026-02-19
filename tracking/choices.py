OFFICE_CHOICES = (
    ('GO', 'Governors Office'),
    ('IU', 'Governors Office - Information Unit'),
    ('ITU', 'Governors Office - Information Technology Department'),
    ('LEDIPO', 'Governors Office - LEDIPO'),
    ('PNO', 'Provincial Nutrition Office'),
    ('POPCOM', 'Governors Office - POPCOM'),
    ('VGO', 'Vice Governors Office'),
    ('ACCOUNTING', 'Provincial Accounting Office'),
    ('ADMIN', 'Provincial Administrators Office'),
    ('PABEO', 'Provincial Agricultural and Biosystems Engineering Office'),
    ('PASO', 'Provincial Agricultural Services Office'),
    ('ASSESSOR', 'Provincial Assessor Office'),
    ('PBMO', 'Provincial Budget and Management Office'),
    ('PCDO', 'Provincial Cooperative Development Office'),
    ('PDRRMO', 'Provincial Disaster Risk Reduction and Management Office'),
    ('PEO-ADMIN', 'Provincial Engineers Office - Administrative'),
    ('PEO-MAINTENANCE', 'Provincial Engineers Office - Maintenance'),
    ('PENRO', 'Provincial Environment and Natural Resources Office'),
    ('PEPO', 'Provincial Equipment Pool Office'),
    ('PGSO', 'Provincial General Services Office'),
    ('PHO', 'Provincial Health Office'),
    ('PHRMDO', 'Provincial Human Resource Management Development Office'),
    ('PIASO', 'Provincial Internal Audit Services Office'),
    ('PLO', 'Provincial Legal Office'),
    ('PPDAO', 'Provincial Persons with Disability Affairs Office'),
    ('PPDO', 'Provincial Planning and Development Office'), 
    ('PPESO', 'Provincial Public Employment Service Office'),
    ('PSWDO', 'Provincial Social Welfare and Development Office'),
    ('TOURISM', 'Provincial Tourism Office'),
    ('TREASURER', 'Provincial Treasurers Office'),
    ('PVO', 'Provincial Veterinary Office'),
    ('PYDO', 'Provincial Youth Development Office'),
    ('SP-LEGISLATIVE', 'Sangguniang Panlalawigan - Legislative Services'),
    ('SP-SUPPORT', 'Sangguniang Panlalawigan - Support Services'),
)

STATUS_CHOICES = (
    ('PENDING', 'Pending'),
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'),
    ('FOR_REVIEW', 'For Review'),
    ('COMPLETED', 'Completed'),
    ('IN_PROGRESS', 'In Progress'),
    ('CANCELLED', 'Cancelled'),
)

ROLE_CHOICES = (
    ('HEAD', 'Office Head'),
    ('STAFF', 'Staff'),
    ('GOVERNOR', 'Governor'),
    ('EXECUTIVE', 'Executive'),
    ('ADMIN', 'Administrator'),
)

OFFICE_DICT = dict(OFFICE_CHOICES)
STATUS_DICT = dict(STATUS_CHOICES)
ROLE_DICT = dict(ROLE_CHOICES)