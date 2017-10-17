## IN ORDER TO ACCURATELY AND RESPONSIBLY USE GREEN TEAM’S CLINICAL DATA SERVICE, YOU MUST READ THE ENTIRE TEXT BELOW.

## SUMMARY OF KEY POINTS:
1. Real-world patient data comprise data on ~160,000 patients with an ‘asthma-like’ phenotype; the data can be used for scientific inference, but caveats pertain to multiple aspects of the data, including geocodes; IRB approval is required for access

2. HuSH+ patient data comprise hypothetical data on ~16,000 patients with an ‘asthma-like’ phenotype; the data can be used to a limited extent for scientific inference, but critical caveats pertain; a fully executed DUA is required for access

a. Any inferences based on date/time and location (geocode) CANNOT be made using the HuSH+ patient data; and

b. All other inferences MUST consider date/time and location as potentially hidden covariates.

## Green Team Clinical Data Service: Real-world Patient Data vs HuSH+ Patient Data

The Green Team’s Clinical Data Service API provides defined access to clinical data on ~16,000 ‘HuSH+’ patients with an ‘asthma-like’ phenotype. Users can select input parameters, and the service returns select output based on the input parameters. The input parameters are: sex; race; and location or type of visit (inpatient, outpatient, emergency). Based on the input parameters, the service returns the following output parameters: a list of patients by ID, birth date, sex, race, latitude/longitude location of primary residence; an array of diagnostic ICD code, dates of encounters and location of encounters, medications prescribed/administered at each encounter; and dates of diagnoses and diagnostic ICD codes.

Importantly, users must understand the definition of ‘HuSH+’ patient data and the limitations of the data in order to appropriately use the clinical service API and accurately interpret the output.

For the NCATS Biomedical Translator project, the Green Team has created two sets of patient data: (1) **‘real-world’ patient data**; and (2) **'HuSH+’ (HIPAA Safe Harbor Plus) patient data**.

The **‘real-world’ patient data set** is comprised of real observational data on ~160,000 patients with an ‘asthma-like’ phenotype (defined below) from UNC Health Care System’s Carolina Data Warehouse for Health (CDWH). As such, the data can be used for clinical interpretation, scientific inference, and discovery. Important caveats include:

*1.	Geocodes represent patient home location in Feb 2016; discussion are underway with CDWH regarding a more regular batch upload and treatment of historical data;*

*2.	age_in_years_num variable is entered by provider at each visit and thus is not as reliable as calculating age from birth date and date of visit;*

*3.	Medications include both administered and prescribed;*

*4.	Medications are not standardized, so all possible formulations, generic/brand names, dosages, and doses are represented; and*

*5.	CDWH data are structured using the i2b2 data model, and certain variables are lost or transformed when EPIC EMR data are pulled into i2b2, for example:*

*a. location variable (clinic, ED, inpatient) treats ED visits as inpatient visits if a patient first admits to the ED and is later transferred to the inpatient ward;* and

*b. parental_smoking_status variable has been dropped.*

The **‘HuSH+’ patient data set** is comprised of clinical and administrative data on ~16,000 hypothetical patients. The HuSH+ data set was created using the real patient data set, but it is completely compliant with §164.514(b) of [HIPAA, 'Safe Harbor' method for patient de-identification of medical records](https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification). Specifically, the HuSH+ patient data set has had:

*1.	real patient identifiers (including geocodes) replaced with random patient identifiers;*

*2.	dates (including birth dates) shifted by a random number of days (maximum of 50 days), with all dates for a given patient shifted by the same number of days; and*

*3.	patients who are currently aged >89 years have been removed from the data set, per HIPAA guidelines on Protected Health Information.*

The resultant HuSH+ data set is thus comprised of hypothetical patients with fictional drug exposures and health outcomes, but the data are representative of the types of relationships expected to be observed within real observational patient data sets. Because the HuSH+ data are only representative of hypothetical patients, drug exposures, and health outcomes, the data cannot be used for clinical interpretation, nor true scientific inference nor true discovery. Thus, the main considerations when working with HuSH+ data are:

*1.	Any inferences based on date/time and location (geocode) CANNOT be made using the HuSH+ patient data; and*

*2.	All other inferences MUST consider date/time and location as potentially hidden covariates.*

As noted, the real patient data set from which the HuSH+ patient data set was created is derived from UNC’s CDWH and contains clinical and administrative data on all patients with an ‘asthma-like’ phenotype. Patients with an asthma-like phenotype were identified as follows:[1]

*1.	Patients with a diagnostic code of ‘asthma’ and prescribed or administered medications that are typically used to treat asthma;*

*2.	Patients with a diagnostic code for a respiratory condition other than asthma and prescribed or administered medications that are typically used to treat asthma;*

*3.	Patients with a diagnostic code for a respiratory condition other than asthma and prescribed tests or procedures that are typically used to diagnosis asthma; or*

*4.	Patients with a diagnostic code for a respiratory condition other than asthma and frequent ED visits with albuterol nebulizer administered.*

*Note that the real CDWH patient data set is available only to IRB-approved members of the Green Team; however, the HuSH+ patient data set is open to all Translator team members via the Green Team’s clinical service API and a signed and fully executed Data Use Agreement.*


___

[1]The following codes and parameters were used to identify patients with an ‘asthma-like’ phenotype:

**Diagnostic codes for asthma and asthma-like conditions**
ICD9	493.%	asthma
ICD10	345.%	asthma
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
IC9	485.%	pneumonia
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
