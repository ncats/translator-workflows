## IN ORDER TO ACCURATELY AND RESPONSIBLY USE GREEN TEAM’S CLINICAL DATA SERVICE, YOU MUST READ THE ENTIRE TEXT BELOW.

## SUMMARY OF KEY POINTS:
1. Fully identified patient data comprise data on ~160,000 patients with an ‘asthma-like’ phenotype. The data can be used for scientific inference, but caveats pertain to multiple aspects of the data, including geocodes. IRB approval is required for access.

2. HuSH+ (HIPAA Safe Harbor Plus) patient data comprise deidentified data on ~16,000 patients with an ‘asthma-like’ phenotype. The data can be used to a limited extent for scientific inference, but critical caveats pertain to the data. A fully executed DUA is required for access.

  a. Any inferences based on date/time and location (geocode) CANNOT be made using the HuSH+ patient data because dates/times have been shifted and geocodes were randomly assigned.

  b. All other inferences MUST consider date/time and location as potentially hidden covariates.

3. ICEES (Integrated Clinical and Environmental Exposures Service) provides access to deidentified data on all patients with an ‘asthma-like’ phenotype. The data can be used to a limited extent for scientific inference, but critical caveats pertain to the data. There are no restrictions on data access.

  a. All feature variables have been binned or recoded, and the underlying integrated feature tables have been designed to present either patient- or visit-level data over specific 'study' periods (currently defined as calendar years).

  b. All inferences must be made in respect to the binning strategy, 'study' design, and type of integrated feature table.

**We kindly request that Translator team members provide proper attribution for any products (e.g., manuscripts, podium presentations, software) derived from work related to Green Team's clinical datasets. Attribution should include acknowledgement of the funder (National Center for Advancing Translational Sciences [NCATS], Biomedical Data Translator Program awards, OT3TR002020 and OT2TR002514), the North Carolina Translational and Clinical Sciences (NC TraCS) Institute (NCATS, Center for Translational Science Award, UL1TR002489), UNC Hospitals and Health Care System, and all Green Team members who contributed to the work.**

## Green Team Clinical Data Service: Fully Identified Patient Data, HuSH+ Patient Data, ICEES

For the NCATS Biomedical Translator project, Green Team has created three sets of patient data: (1) **fully identified patient data**; (2) **HuSH+ (HIPAA Safe Harbor Plus) patient data**; and (3)**ICEES (Integrated Clinical and Environmental Exposures Service)**.

## Fully Identified Patient Dataset

The **fully identified patient dataset** is comprised of real observational data on ~160,000 patients with an ‘asthma-like’ phenotype (defined below) from UNC Health Care System’s Carolina Data Warehouse for Health (CDWH). As such, the data can be used for clinical interpretation, scientific inference, and discovery. Important caveats are listed below.

*1.	Geocodes represent patient home location in Feb 2016; discussions are underway with the CDWH Oversight Commmittee regarding a more regular batch upload and treatment of historical data.*

*2.	age_in_years_num variable is entered by the provider at each visit and thus is not as reliable as calculating age from birth date and date of visit.*

*3.	Medications include both administered and prescribed.*

*4.	Medications are not standardized, so all possible formulations, generic/brand names, dosages, and doses are represented.*

*5.	CDWH data are structured using the i2b2 data model, and certain variables are lost or transformed when EPIC EMR data are pulled into i2b2, for example:*

  *a. location variable (outpatient, inpatient, ED, ED to inpatient) does not always include data on initial admissions to ED and later transfers to inpatient ward;* and

  *b. parental_smoking_status variable has been dropped.*

*Access to the fully identified patient dataset requries CITI Training and an IRB-approved protocol.*

## HuSH+ Patient Dataset

The **HuSH+ patient dataset** is comprised of real observational data on ~16,000 hypothetical patients with an asthma-like phenotype (defined below). The HuSH+ dataset was created using the fully identified patient dataset, but it is completely compliant with §164.514(b) of [HIPAA, 'Safe Harbor' method for patient de-identification of medical records](https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification). Specifically, the HuSH+ patient dataset has achieved HIPAA compliance through the following operations.

*1.	Real patient identifiers (including geocodes) were replaced with random patient identifiers.*

*2.	Dates (including birth dates) were shifted by a random number of days (maximum of 50 days), with all dates for a given patient shifted by the same number of days.*

*3.	Patients aged >89 years were removed from the dataset, per HIPAA guidelines on Protected Health Information.*

The resultant HuSH+ dataset is thus comprised of hypothetical patients with fictional drug exposures and health outcomes, but the data are representative of the types of relationships expected to be observed within real observational patient data sets. Because the HuSH+ data are only representative of hypothetical patients, drug exposures, and health outcomes, the data can not be used for clinical interpretation. The HuSH+ data can be used for scientific inference and discovery, although important caveats must be considered. The main considerations when working with HuSH+ data outlined below.

*1.	Any inferences based on date/time and location (geocode) CANNOT be made using the HuSH+ patient data.*

*2.	All other inferences MUST consider date/time and location as potentially hidden covariates.*

*Access to the HuSH+ patient dataset requires a fully executed DUA.*

## ICEES

**ICEES** offers access to real observational clinical data on all patients in the CDWH with an asthma-like phenotype (defined below). The data additionally contain data derived from several public databases on chemical exposures (e.g., airborne pollutants) and sociological exposures (e.g., estimated household income). The exposures data have been integrated with the clinical data at the patient and visit level. Like the HuSH+ dataset, the ICEES clinical data were derived from the fully identified patient dataset, but the data have been 'binned' or recoded in order to protect patient privacy while also providing open access to the data via a Translator API and maintaining compliance with §164.514(b) of [HIPAA, 'Safe Harbor' method for patient de-identification of medical records](https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification).

ICEES is designed to offer four basic functionalities (also see [slide deck](https://drive.google.com/open?id=12TgOZMFkWQLMhjZeN4RVzdxvlt1VYcO8)).

*1. Cohort discovery: users define a cohort using any number of defined feature variables as input parameters, and the service returns a sample size.*

*2. Feature-rich cohort discovery: users select a predefined cohort as the input parameter, and the service returns a profile of that cohort in terms of the available feature variables.*

*3. Hypothesis-driven 2 x 2 feature associations: users select a predefined cohort and two feature variables, and the service returns a 2 x 2 feature table with a corresponding Chi Square statistic and P value.*

*4. Exploratory 1 X N feature associations: users select a predefined cohort and a feature variable of interest, and the service returns a 1 x N feature table with corrected Chi Square statistics and associated P values.*

ICEES can be used for scientific inference and discovery, although important caveats must be considered. The main considerations when working with ICEES are outlined below.

*1. All feature variables have been binned or recoded (see [templates](https://drive.google.com/open?id=12TgOZMFkWQLMhjZeN4RVzdxvlt1VYcO8)).*

*2. The integrated feature tables are designed for different 'study' periods (currently defined as calendar years).*

*3. The integrated feature tables are designed to provide access to either patient-level data or visit-level data.*

*4. All inferences must be made with respect to the binning strategy, 'study' design, and type of integrated feature table.* 

*Access to ICEES is open to all Translator team members and is not subject to regulatory constraints.*

**[ICEES API](https://icees.renci.org/apidocs/)**

## Green Team's Asthma-like Cohort

**Asthma-like cohort**: All three clinical datasets that Green Team has created to support the Translator program are derived from UNC’s CDWH. At present, the clinical datasets are restricted to patients with an ‘asthma-like’ phenotype, although we are expanding ICEES to include additional patient cohorts (e.g., pain, obesity, diabetes, drug-induced liver injury).

Patients with an asthma-like phenotype were defined as follows:[1]

*1.	Patients with a diagnostic code of ‘asthma’ and prescribed or administered medications that are typically used to treat asthma;*

*2.	Patients with a diagnostic code for a respiratory condition other than asthma and prescribed or administered medications that are typically used to treat asthma;*

*3.	Patients with a diagnostic code for a respiratory condition other than asthma and prescribed tests or procedures that are typically used to diagnosis asthma; or*

*4.	Patients with a diagnostic code for a respiratory condition other than asthma and frequent ED visits with albuterol nebulizer administered.*

## General Comments on Regulatory Constraints and Acknowledgements

**Note that Green Team's clinical datasets are subject to various regulatory constraints, depending on the specific dataset. The fully identified patient dataset is available only to IRB-approved members of Green Team. The HuSH+ patient dataset is available to Translator team members via a fully executed, institutional Data Use Agreement. ICEES is open to all Translator team members via Green Team's ICEES API; ICEES is not subject to any additional regulatory constraints.**

**We kindly request that Translator team members provide proper attribution for any products (e.g., manuscripts, podium presentations, software) derived from work related to Green Team's clinical datasets. Attribution should include acknowledgement of the funder (National Center for Advancing Translational Sciences [NCATS], Biomedical Data Translator Program awards, OT3TR002020 and OT2TR002514), the North Carolina Translational and Clinical Sciences (NC TraCS) Institute (NCATS, Center for Translational Science Award, UL1TR002489), UNC Hospitals and Health Care System, and all Green Team members who contributed to the work.**


___

[1]The following codes and parameters were used to identify patients with an ‘asthma-like’ phenotype:

**Diagnostic codes for asthma and asthma-like conditions**
ICD9	493.%	asthma
ICD10	J45.%	asthma
ICD9	464.%	croup
ICD10	J05.%	croup
ICD9	496.%	reactive airway
ICD10	J44.%	reactive airway
ICD10	J66.%	reactive airway
ICD9	786.%	cough
ICD10	R05.%	cough
ICD9	481.%	pneumonia
ICD9	482.%	pneumonia
ICD9	483.%	pneumonia
ICD9	484.%	pneumonia
ICD9	485.%	pneumonia
ICD9	486.%	pneumonia
ICD10	J12.%	pneumonia
ICD10	J13.%	pneumonia
ICD10	J14.%	pneumonia
ICD10	J15.%	pneumonia
ICD10	J16.%	pneumonia
ICD10	J17.%	pneumonia
ICD10	J18.%	pneumonia

**Tests and procedures for asthma and asthma-like conditions**
CPT	94010	spirometry
CPT	94070	multiple spirometry
CPT	95070	methacholine challenge test
CPT	94620	simple exercise stress test
CPT	94621	complex exercise stress test
CPT	31624	bronchoscopy
CPT	94375	flow-volume loop
CPT	94060	spirometry (pre/post bronchodilator test)
CPT	94070	bronchospasm provocation
CPT	95070	inhalation bronchial challenge
CPT	94664	bronchodilator administration
CPT	94620	pulmonary stress test
CPT	95027	airborne allergen panel

**Medications prescribed for patients with asthma-like phenotype**
MEDCTN		prednisone
MEDCTN		fluticasone
MEDCTN		mometasone
MEDCTN		budesonide
MEDCTN		beclomethasone
MEDCTN		ciclesonide
MEDCTN		flunisolide
MEDCTN		albuterol
MEDCTN		metaproterenol
MEDCTN		diphenydramine
MEDCTN		fexofenadine
MEDCTN		cetirizine
MEDCTN		ipratropium
MEDCTN		salmeterol
MEDCTN		arformoterol
MEDCTN		formoterol
MEDCTN		indacaterol
MEDCTN		theophylline
MEDCTN		omalizumab
MEDCTN		mepolizumab
