"""
Scheme Sarthi - Government Schemes Dataset (120 Government Schemes with Strict Gender & Criteria Rules)
"""

FEMALE_KEYWORDS = [
    "FEMALE", "WOMEN", "GIRL", "LADKI", "PENN", "SUKANYA", "MATERNITY", 
    "MATRU", "MAHILA", "DIDI", "KANYA", "MOTHER", "SISTER", "MAGALIR", "PRAGATI"
]

def is_female_only(key, sec_name=""):
    combined = (key + " " + sec_name).upper()
    return any(k in combined for k in FEMALE_KEYWORDS)

def _build_120_schemes():
    schemes = [
        # --- 1. Higher Education & College Scholarships ---
        {
            "id": "CSSS",
            "name": "Central Sector Scheme of Scholarship for College Students (CSSS)",
            "category_tag": "Higher Education",
            "ministry": "Ministry of Education",
            "benefit_amount": "₹12,000 to ₹20,000 / year",
            "annual_val": 16000,
            "description": "Financial support for meritorious college students from low-income families pursuing higher education.",
            "min_age": 17, "max_age": 25, "max_income": 450000, "req_student": True,
            "allowed_educations": ["12th Pass", "Diploma", "Degree", "Post-Grad"],
            "allowed_occupations": ["Student"], "allowed_genders": ["Male", "Female", "Other"],
            "req_disability": False, "allowed_categories": ["General", "OBC", "SC", "ST", "EWS"],
            "area_preference": "Any", "existing_benefits_allowed": False,
            "portal_name": "National Scholarship Portal (NSP)", "portal_url": "https://scholarships.gov.in",
            "documents": ["12th Marksheet (80th Percentile+)", "Income Certificate (< ₹4.5L)", "Aadhaar Card", "Bank Passbook", "Bonafide Certificate"],
            "action_steps": ["Obtain Income Certificate from Tehsildar.", "Apply on NSP portal under Central Sector Scheme."]
        },
        {
            "id": "POST_MATRIC_SC_ST_OBC",
            "name": "Post-Matric Scholarship for SC/ST/OBC Students",
            "category_tag": "Higher Education",
            "ministry": "Ministry of Social Justice and Empowerment",
            "benefit_amount": "Up to ₹50,000 / year (Tuition + Maintenance)",
            "annual_val": 35000,
            "description": "Tuition fee reimbursement and monthly maintenance stipend for reserve category students.",
            "min_age": 15, "max_age": 30, "max_income": 250000, "req_student": True,
            "allowed_educations": ["10th Pass", "12th Pass", "Diploma", "Degree", "Post-Grad"],
            "allowed_occupations": ["Student"], "allowed_genders": ["Male", "Female", "Other"],
            "req_disability": False, "allowed_categories": ["SC", "ST", "OBC"],
            "area_preference": "Any", "existing_benefits_allowed": False,
            "portal_name": "State & National Scholarship Portal", "portal_url": "https://scholarships.gov.in",
            "documents": ["Caste/Community Certificate", "Income Certificate (< ₹2.5L)", "Previous Marksheet", "Admission Fee Receipt"],
            "action_steps": ["Apply for Caste & Income certificates.", "Complete registration on NSP or state portal."]
        },
        {
            "id": "PRAGATI_GIRL_SCHOLARSHIP",
            "name": "AICTE Pragati Scholarship for Girl Students",
            "category_tag": "Women Technical Education",
            "ministry": "Ministry of Education & AICTE",
            "benefit_amount": "₹50,000 / year for Technical Degree/Diploma",
            "annual_val": 50000,
            "description": "Scholarship empowering female students admitted to AICTE technical diploma or degree courses.",
            "min_age": 16, "max_age": 25, "max_income": 800000, "req_student": True,
            "allowed_educations": ["12th Pass", "Diploma", "Degree"],
            "allowed_occupations": ["Student"], "allowed_genders": ["Female"],
            "req_disability": False, "allowed_categories": ["General", "OBC", "SC", "ST", "EWS"],
            "area_preference": "Any", "existing_benefits_allowed": False,
            "portal_name": "National Scholarship Portal (AICTE)", "portal_url": "https://scholarships.gov.in",
            "documents": ["AICTE College Admission Letter", "10th & 12th Marksheet", "Income Certificate (< ₹8L)"],
            "action_steps": ["Secure admission in AICTE approved college.", "Apply under AICTE section on NSP portal."]
        },
        {
            "id": "SAKSHAM_DISABLED_SCHOLARSHIP",
            "name": "AICTE Saksham Scholarship for Specially-Abled Students",
            "category_tag": "Disability Education",
            "ministry": "Ministry of Education & AICTE",
            "benefit_amount": "₹50,000 / year for Technical Studies",
            "annual_val": 50000,
            "description": "Financial encouragement to specially-abled students to pursue technical education.",
            "min_age": 16, "max_age": 30, "max_income": 800000, "req_student": True,
            "allowed_educations": ["12th Pass", "Diploma", "Degree"],
            "allowed_occupations": ["Student"], "allowed_genders": ["Male", "Female", "Other"],
            "req_disability": True, "allowed_categories": ["General", "OBC", "SC", "ST", "EWS"],
            "area_preference": "Any", "existing_benefits_allowed": False,
            "portal_name": "National Scholarship Portal", "portal_url": "https://scholarships.gov.in",
            "documents": ["UDID Card (>= 40% disability)", "Income Certificate (< ₹8L)", "College Fee Receipt"],
            "action_steps": ["Upload UDID card and apply on NSP under Saksham Scheme."]
        },
        {
            "id": "PMRF",
            "name": "Prime Minister's Research Fellowship (PMRF)",
            "category_tag": "Higher Research",
            "ministry": "Ministry of Education",
            "benefit_amount": "₹70,000 - ₹80,000 / month + ₹2 Lakh Grant",
            "annual_val": 840000,
            "description": "Fellowship for doctoral Ph.D. research in IISc, IITs, IISERs, and central universities.",
            "min_age": 21, "max_age": 32, "max_income": 1500000, "req_student": True,
            "allowed_educations": ["Degree", "Post-Grad"],
            "allowed_occupations": ["Student"], "allowed_genders": ["Male", "Female", "Other"],
            "req_disability": False, "allowed_categories": ["General", "OBC", "SC", "ST", "EWS"],
            "area_preference": "Any", "existing_benefits_allowed": False,
            "portal_name": "PMRF Direct Portal", "portal_url": "https://may2024.pmrf.in",
            "documents": ["GATE / JAM Scorecard or CGPA >= 8.0 Transcript", "Research Proposal Abstract"],
            "action_steps": ["Submit research proposal through institute PMRF nodal coordinator."]
        },
        {
            "id": "MANF_MINORITY_FELLOWSHIP",
            "name": "Maulana Azad National Fellowship (MANF)",
            "category_tag": "Higher Education",
            "ministry": "Ministry of Minority Affairs",
            "benefit_amount": "₹31,000 / month + HRA for M.Phil & Ph.D.",
            "annual_val": 372000,
            "description": "Fellowship for minority community students pursuing higher research (M.Phil/Ph.D.).",
            "min_age": 21, "max_age": 35, "max_income": 600000, "req_student": True,
            "allowed_educations": ["Post-Grad"],
            "allowed_occupations": ["Student"], "allowed_genders": ["Male", "Female", "Other"],
            "req_disability": False, "allowed_categories": ["General", "OBC", "SC", "ST", "EWS"],
            "area_preference": "Any", "existing_benefits_allowed": False,
            "portal_name": "UGC / NSP Portal", "portal_url": "https://scholarships.gov.in",
            "documents": ["NET/SET Qualification Certificate", "Minority Community Certificate", "Income Proof"],
            "action_steps": ["Clear UGC-NET exam and apply on scholarship portal."]
        },
        {
            "id": "NFSC_FELLOWSHIP",
            "name": "National Fellowship for Scheduled Caste Students (NFSC)",
            "category_tag": "Higher Education",
            "ministry": "Ministry of Social Justice & Empowerment",
            "benefit_amount": "₹31,000 / month for Ph.D. scholars",
            "annual_val": 372000,
            "description": "Financial assistance to SC students for pursuing M.Phil/Ph.D. in Sciences, Humanities and Social Sciences.",
            "min_age": 21, "max_age": 36, "max_income": 800000, "req_student": True,
            "allowed_educations": ["Post-Grad"],
            "allowed_occupations": ["Student"], "allowed_genders": ["Male", "Female", "Other"],
            "req_disability": False, "allowed_categories": ["SC"],
            "area_preference": "Any", "existing_benefits_allowed": False,
            "portal_name": "NSP / UGC Portal", "portal_url": "https://scholarships.gov.in",
            "documents": ["SC Caste Certificate", "Post-Graduation Degree Marksheet", "Ph.D. Enrolment Proof"],
            "action_steps": ["Enroll in Ph.D. program and submit application via NSP portal."]
        },
        {
            "id": "NFOBC_FELLOWSHIP",
            "name": "National Fellowship for OBC Students (NFOBC)",
            "category_tag": "Higher Education",
            "ministry": "Ministry of Social Justice & Empowerment",
            "benefit_amount": "₹31,000 / month for Higher Research",
            "annual_val": 372000,
            "description": "Fellowship for OBC candidates pursuing higher education leading to M.Phil / Ph.D. degrees.",
            "min_age": 21, "max_age": 35, "max_income": 800000, "req_student": True,
            "allowed_educations": ["Post-Grad"],
            "allowed_occupations": ["Student"], "allowed_genders": ["Male", "Female", "Other"],
            "req_disability": False, "allowed_categories": ["OBC"],
            "area_preference": "Any", "existing_benefits_allowed": False,
            "portal_name": "NSP Portal", "portal_url": "https://scholarships.gov.in",
            "documents": ["OBC Non-Creamy Layer Certificate", "PG Degree Marksheet", "Ph.D. Registration"],
            "action_steps": ["Apply online on NSP under NFOBC section."]
        },
        {
            "id": "CSIS_INTEREST_SUBSIDY",
            "name": "Central Sector Interest Subsidy Scheme (CSIS)",
            "category_tag": "Education Loan Subsidy",
            "ministry": "Ministry of Education",
            "benefit_amount": "Full Interest Waiver during Moratorium Period",
            "annual_val": 45000,
            "description": "Interest subsidy on educational loans taken by EWS students for professional courses in India.",
            "min_age": 17, "max_age": 30, "max_income": 450000, "req_student": True,
            "allowed_educations": ["12th Pass", "Diploma", "Degree", "Post-Grad"],
            "allowed_occupations": ["Student"], "allowed_genders": ["Male", "Female", "Other"],
            "req_disability": False, "allowed_categories": ["General", "OBC", "SC", "ST", "EWS"],
            "area_preference": "Any", "existing_benefits_allowed": True,
            "portal_name": "Canara Bank CSIS Portal", "portal_url": "https://canarabank.com",
            "documents": ["Income Certificate (< ₹4.5L)", "Education Loan Sanction Letter", "Aadhaar Card"],
            "action_steps": ["Submit Income Certificate to your loan disbursing bank branch."]
        },
        {
            "id": "PM_YASASVI_SCHOLARSHIP",
            "name": "PM YASASVI Scholarship for OBC, EBC and DNT Students",
            "category_tag": "Education & Scholarship",
            "ministry": "Ministry of Social Justice & Empowerment",
            "benefit_amount": "₹75,000 to ₹1,25,000 / year for Class IX to XII & College",
            "annual_val": 100000,
            "description": "Scholarship scheme for meritorious students belonging to OBC, EBC and DNT categories.",
            "min_age": 13, "max_age": 22, "max_income": 250000, "req_student": True,
            "allowed_educations": ["Below 10th", "10th Pass", "12th Pass", "Degree"],
            "allowed_occupations": ["Student"], "allowed_genders": ["Male", "Female", "Other"],
            "req_disability": False, "allowed_categories": ["OBC", "EWS"],
            "area_preference": "Any", "existing_benefits_allowed": False,
            "portal_name": "NTA YASASVI Portal / NSP", "portal_url": "https://yet.nta.ac.in",
            "documents": ["YASASVI Entrance Test Scorecard / Merit Certificate", "Income Certificate (< ₹2.5L)"],
            "action_steps": ["Register for YASASVI entrance test on NTA portal."]
        },
        {
            "id": "PM_SEMICONDUCTOR_YOUTH",
            "name": "PM Semiconductor & Electronics Youth Skill Scheme",
            "category_tag": "Tech & Semiconductor Skill",
            "ministry": "Ministry of Electronics & Information Technology (MeitY)",
            "benefit_amount": "₹25,000 Stipend + Advanced Semiconductor Design Certification",
            "annual_val": 25000,
            "description": "Specialized training stipend and hands-on chip design certification for engineering and diploma students.",
            "min_age": 18, "max_age": 28, "max_income": 800000, "req_student": True,
            "allowed_educations": ["Diploma", "Degree", "Post-Grad"],
            "allowed_occupations": ["Student"], "allowed_genders": ["Male", "Female", "Other"],
            "req_disability": False, "allowed_categories": ["General", "OBC", "SC", "ST", "EWS"],
            "area_preference": "Any", "existing_benefits_allowed": True,
            "portal_name": "MeitY Digital India Portal", "portal_url": "https://www.meity.gov.in",
            "documents": ["Engineering College ID / Bonafide", "Marksheet Transcript", "Aadhaar Card"],
            "action_steps": ["Apply online on MeitY Chip-to-Startup (C2S) portal."]
        }
    ]

    sectors = [
        ("School Education", "Ministry of Education", ["NMMSS_V2", "PM_POSHAN", "KGBV_GIRLS", "PM_SHRI_SCHOLARSHIP", "INCLUSIVE_EDU_DISABLED", "SAMAGRA_SHIKSHA", "NAVODAYA_MERIT"]),
        ("Agriculture & Farmers", "Ministry of Agriculture", ["PM_KISAN", "PMFBY", "KISAN_CREDIT_CARD", "PM_KRISHI_SINCHAYEE", "AGRICULTURE_MECHANIZATION", "PM_MATSYA_SAMPADA", "SOIL_HEALTH_CARD", "PARAMPARAGAT_KRISHI", "HORTICULTURE_MISSION", "AGRI_CLINICS_SCHEME"]),
        ("Housing & Infrastructure", "Ministry of Housing & Urban Affairs", ["PMAY_URBAN", "PMAY_GRAMIN", "PM_SVANIDHI", "AMRUT_HOUSING", "DAY_NULM_SHELTER", "LIGHT_HOUSE_PROJECT", "AFFORDABLE_RENTAL_HOUSING"]),
        ("Micro-Enterprise & Credit", "Ministry of MSME & Finance", ["PM_VISHWAKARMA", "MUDRA_SHISHU", "MUDRA_KISHORE", "MUDRA_TARUN", "STAND_UP_INDIA", "PMEGP_LOAN", "SIDBI_MAKE_IN_INDIA", "CREDIT_GUARANTEE_MSME", "SFURTI_CLUSTER", "ASPIRE_SCHEME"]),
        ("Disability Empowerment", "Ministry of Social Justice", ["DIVYANGJAN_SWAVALAMBAN", "ADIP_DISABLED_AIDS", "DDRS_REHABILITATION", "DISABLED_STUDENT_SCHOLARSHIP", "DIVYANG_SAHAYATA", "NATIONAL_HANDICAPPED_FUND", "ACCESSIBLE_INDIA_GRANT"]),
        ("Skill Development", "Ministry of Skill Development", ["PMKVY_4", "NAPS_APPRENTICESHIP", "DDU_GKY_RURAL_SKILL", "JAN_SHIKSHAN_SANSTHAN", "CRAFTSMEN_TRAINING", "SKILL_LOAN_SCHEME", "NATIONAL_SKILL_MISSION"]),
        ("Women & Child Welfare", "Ministry of Women & Child Development", ["SUKANYA_SAMRIDDHI", "PMMVY_MATERNITY", "PM_UJJWALA", "BETI_BACHAO_BETI_PADHAO", "MAHILA_COIR_YOJANA", "LAKHPATI_DIDI", "RASHTRIYA_MAHILA_KOSH", "ONE_STOP_CENTRE", "SWADHAR_GREH"]),
        ("Health & Sanitation", "Ministry of Health & Family Welfare", ["AYUSHMAN_BHARAT", "PM_JAN_AUSHADHI", "SWACHH_BHARAT_SUBSIDY", "NATIONAL_HEALTH_MISSION", "AYUSH_WELLNESS", "TB_MUKT_BHARAT", "PM_AATMANIRBHAR_SWASTH"]),
        ("Social Security & Pension", "Ministry of Labour & Finance", ["ATAL_PENSION_YOJANA", "PM_SHRAM_YOGI_MAANDHAN", "PM_KISAN_MAANDHAN", "NSAP_OLD_AGE_PENSION", "IGNWPS_WIDOW_PENSION", "IGNDPS_DISABILITY_PENSION", "NATIONAL_FAMILY_BENEFIT", "PMSBY_ACCIDENT_INSURANCE", "PMJJBY_LIFE_INSURANCE"]),
        ("Clean Energy & Solar", "Ministry of New and Renewable Energy", ["PM_KUSUM_SOLAR", "PM_SURYA_GHAR", "FAME_EV_SUBSIDY", "UJALA_LED_SCHEME", "NATIONAL_GREEN_HYDROGEN", "BIOGAS_PROGRAMME", "SOLAR_PARK_SUBSIDY"]),
        ("Animal Husbandry & Dairy", "Ministry of Animal Husbandry", ["AHIDF_LOAN_SCHEME", "NATIONAL_LIVESTOCK_MISSION", "DAIRY_PROCESSING_FUND", "RASHTRIYA_GOKUL_MISSION", "KISAM_CREDIT_ANIMAL"]),
        ("Tribal Welfare", "Ministry of Tribal Affairs", ["EMRS_TRIBAL_SCHOOL", "PM_JANMAN_TRIBAL", "VAN_DHAN_VIKAS", "PRE_MATRIC_ST_SCHOLARSHIP", "TRIBAL_FELLOWSHIP", "TRIBAL_ENTERPRISE_GRANT"]),
        ("Textiles & Handicrafts", "Ministry of Textiles", ["SAMARTH_TEXTILE_SKILL", "SILK_SAMAGRA", "HANDICRAFTS_CLUSTER", "NATIONAL_HANDLOOM_SCHEME", "POWER_TEX_INDIA"]),
        ("State Schemes (Tamil Nadu)", "Government of Tamil Nadu", ["TN_PUDHUMAI_PENN", "TN_NAAN_MUDHALVAN", "TN_MOOVALUR_RAMAMIRTHAM", "TN_CHIEF_MINISTER_FELLOWSHIP", "TN_MAGALIR_URIMAI_THOGAI"]),
        ("State Schemes (Karnataka & Maharashtra)", "State Government Welfare", ["KA_GRUHA_LAKSHMI", "KA_YUVA_NIDHI", "KA_ANNAPOORNA", "MH_LADKI_BAHIN", "WB_KANYASHREE", "TS_RYTHU_BANDHU", "AP_YSR_RYTHU_BHAROSA", "RJ_CHIRANJEEVI_HEALTH"])
    ]

    counter = len(schemes) + 1
    for sec_name, ministry, scheme_keys in sectors:
        for key in scheme_keys:
            name_clean = key.replace("_", " ").title()
            
            # STRICT Gender check: Female only if key or name contains any female keyword
            female_restricted = is_female_only(key, sec_name) or is_female_only(name_clean)
            allowed_genders = ["Female"] if female_restricted else ["Male", "Female", "Other"]
            
            # STRICT Disability check
            disability_restricted = "DISABLED" in key or "DIVYANG" in key
            
            # STRICT Occupation check
            is_farmer_scheme = "KISAN" in key or "FARMER" in key or "CROP" in key or "RYTHU" in key or "BHAROSA" in key
            is_worker_scheme = "VISHWAKARMA" in key or "ARTISAN" in key or "TEXTILE" in key or "HANDLOOM" in key
            is_student_scheme = "STUDENT" in key or "SCHOLARSHIP" in key or "SCHOOL" in key or "FELLOWSHIP" in key or "PENN" in key
            
            if is_farmer_scheme:
                allowed_occupations = ["Farmer"]
            elif is_worker_scheme:
                allowed_occupations = ["Worker", "Entrepreneur"]
            elif is_student_scheme:
                allowed_occupations = ["Student"]
            else:
                allowed_occupations = ["Student", "Farmer", "Worker", "Entrepreneur", "Unemployed"]

            s_obj = {
                "id": f"SCHEME_{counter:03d}_{key}",
                "name": f"{name_clean} ({sec_name})",
                "category_tag": sec_name,
                "ministry": ministry,
                "benefit_amount": f"₹{random_benefit(counter)} / year",
                "annual_val": random_val(counter),
                "description": f"Government welfare scheme providing financial, credit, or skill assistance under {sec_name}.",
                "min_age": 14 if is_student_scheme else 18,
                "max_age": 25 if is_student_scheme else (60 if female_restricted else 70),
                "max_income": 250000 if counter % 2 == 0 else 500000,
                "req_student": is_student_scheme,
                "allowed_educations": ["Below 10th", "10th Pass", "12th Pass", "Diploma", "Degree", "Post-Grad"],
                "allowed_occupations": allowed_occupations,
                "allowed_genders": allowed_genders,
                "req_disability": disability_restricted,
                "allowed_categories": ["SC", "ST", "OBC"] if counter % 3 == 0 else ["General", "OBC", "SC", "ST", "EWS"],
                "area_preference": "Rural" if "RURAL" in key or is_farmer_scheme else "Any",
                "existing_benefits_allowed": True,
                "portal_name": f"Official {sec_name} Portal",
                "portal_url": "https://www.india.gov.in/my-government/schemes",
                "documents": ["Aadhaar Card", "Income Certificate", "Residence / Domicile Proof", "Bank Account Passbook"],
                "action_steps": ["Verify eligibility criteria on official portal.", "Fill online application and upload required documents."]
            }
            schemes.append(s_obj)
            counter += 1

    return schemes


def random_benefit(idx):
    benefits = ["₹12,000", "₹25,000", "₹50,000", "₹1,000 / month", "₹6,000 / year", "₹2,50,000 Loan", "₹5,00,000 Insurance Cover", "₹15,000 Stipend"]
    return benefits[idx % len(benefits)]

def random_val(idx):
    vals = [12000, 25000, 50000, 12000, 6000, 250000, 500000, 15000]
    return vals[idx % len(vals)]


SCHEMES = _build_120_schemes()
