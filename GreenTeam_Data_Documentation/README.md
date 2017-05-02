## Green Team Clinical Data Service API
The Green Team’s Clinical Data Service API provides defined access to clinical data on ~16,000 ‘HuSH+’ patients with an ‘asthma-like’ phenotype. Users can select input parameters, and the service returns select output based on the input parameters. The input parameters are: age (or range) in years of patient(s) at time of data set creation; sex; race; and location or type of visit (inpatient, outpatient, emergency). Based on the input parameters, the service returns the following output parameters: a list of patients by ID, current age, birth date, sex, race, and latitude/longitude location; an array of dates of encounters, types of encounter, and medications prescribed/administered at each encounter; and an array of dates of diagnoses and diagnostic ICD codes.

*Importantly, users must understand the definition of ‘HuSH+’ patient data and the limitations of the data in order to appropriately use the clinical service API and accurately interpret the output.*

For the NCATS Biomedical Translator project, the Green Team has created two sets of patient data: (1) **‘real-world’ patient data**; and (2) **'HuSH+’ (HIPAA Safe Harbor Plus) patient data**.

The ‘real-world’ patient data set is comprised of real observational data on ~160,000 patients with an ‘asthma-like’ phenotype (defined below) from UNC Health Care System’s Carolina Data Warehouse for Health (CDWH). As such, the data can be used for clinical interpretation, scientific inference, and discovery.

In contrast, the ‘HuSH+’ patient data set is comprised of clinical and administrative data on ~16,000 hypothetical patients. The HuSH+ data set was created using the real patient data set, but it is completely compliant with §164.514(b) of HIPAA, 'Safe Harbor' method for patient de-identification of medical records (https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification). Specifically, the HuSH+ patient data set has had: 
1.	*real patient identifiers (including geocodes) replaced with random patient identifiers*;
2.	*dates (including birth dates) shifted by a random number of days (maximum of 50 days), with all dates for a given patient shifted by the same number of days*; and
3.	*patients who are currently aged >89 years have been removed from the data set, per HIPAA guidelines on Protected Health Information*.

An additional caveat is that the *age_in_years_num* variable (accessible in the full data set, but not the clinical service API) contains provider-entered data on patient age at each encounter and, as such, is subject to error.

The resultant HuSH+ data set is thus comprised of hypothetical patients with fictional drug exposures and health outcomes, but the data are representative of the types of relationships expected to be observed within real observational patient data sets. Because the HuSH+ data are only representative of hypothetical patients, drug exposures, and health outcomes, the data cannot be used for clinical interpretation, nor scientific inference nor discovery.

As noted, the real patient data set from which the HuSH+ patient data set was created is derived from UNC’s CDWH and contains clinical and administrative data on all patients with an ‘asthma-like’ phenotype. Patients with an asthma-like phenotype were identified as follows:[1]
1.	Patients with a diagnostic code of ‘asthma’ and prescribed or administered medications that are typically used to treat asthma;
2.	Patients with a diagnostic code for a respiratory condition other than asthma and prescribed or administered medications that are typically used to treat asthma;
3.	Patients with a diagnostic code for a respiratory condition other than asthma and prescribed tests or procedures that are typically used to diagnosis asthma; or
4.	Patients with a diagnostic code for a respiratory condition other than asthma and frequent ED visits with albuterol nebulizer administered.

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
