## ‘Endotype’ API*

[Endotype API](http://translator.ncats.io)

**Note that we are using the term ‘endotype’ very loosely. Specifically, we are viewing ‘endotype’ as a combination of ‘phenotype’ (external, observed features), ‘endotype’ (internal, not observed features), and likely clinical outcomes (as determined by initial model M0 = recursive partitioning and decision trees). In this sense, a more appropriate term, perhaps, is ‘feature set’ or 'feature vector'.**

**Input**	{
 
 date_of_birth
 
 sex
 
 race

 model_type:
 
 visits: [
   
   {
   
   time
   
   lat
   
   lon
   
   visit_type:

    icd_codes

	exposures: [
      
      {
  	
	exposure_type
	
	value
	
	units

      }
      ...
    ]
   ...
 ]
}

**Output**	[

{


endotype_id       	: "E0"

endtotype_description: "..."
 
 endotype_evidence: "..."
 
 periods : [
 
 { start_time...end_time },
 
 { start_time...end_time },
 
 ...
 
 ]

}

...
]

**Inputs: Descriptions**

*Clinical data:* Please see [GreenTeam_Clinical_Data_Documentation](https://github.com/NCATS-Tangerine/cq-notebooks/tree/master/Green_CQs/GreenTeam_Clinical_Data_Documentation)

*date_of_birth* (e.g., 2017-10-04)

For HuSH+ data, patient date of birth is shifted by +/- 50 days

*sex*

Male (e.g., "M")

Female (e.g., "F)

Unknown*

*Excluded from R-part model

*race*

1 WHITE OR CAUCASIAN

2 BLACK OR AFRICAN AMERICAN

3 AMERICAN INDIAN OR ALASKA NATIVE

4 ASIAN

5 NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER

6 OTHER/HISPANIC

7 PATIENT REFUSED

8 UNKNOWN

9 OTHER RACE

*time*

time period of interest (e.g., "2017-10-04 21:12:29")

*lat, lon* (latitude, longitude or patient geocode for primary home residence)

lat (e.g., "20"),

lon (e.g., "20",

For HuSH+ data, patient geocode is random latitude, longitude

*visit_type*

INPATIENT

OUTPATIENT

EMERGENCY

*icd_codes*

ICD code(s) at date of visit (e.g., "ICD9:V12", "ICD10:J45")

*exposures*
	
	exposures_type (e.g., "pm25")
	
	units (e.g., "")
	
	value (e.g., "2")

PM2.5 or ozone exposures in relation to 7-day period before date of visit

Please see [GreenTeam_Socioenvironmental_Data_Documentation](https://github.com/NCATS-Tangerine/cq-notebooks/tree/master/Green_CQs/GreenTeam_Socioenvironmental_Data_Documentation)

*model_type*

M0 = General R-part model: Recursive partitioning and decision tree

post_ed ~ inout_cd + pre_ed + sex_cd + race_cd + age + icd + despm_yda + deso_7da

**Output: Descriptions**

Output identifies an opaque id for a class within the endotype classification scheme

The final output is a list of ‘endotypes’, their descriptions, evidence in support of the endotype assertions, and associated time intervals (e.g., all "string")

*Endotype classifications:*

Outcome variable: post_ed

Post_ED = 0, 1, 2, >2 ED or inpatient visits for asthma-like condition over year after current visit

Endotype 0: The patient(s) is predicted to have 0 ED/inpatient visits for respiratory events over the 12-month period after the visit

Endotype 1: The patient(s) is predicted to have 1 ED/inpatient visit for respiratory events over the 12-month period after the visit

Endotype 2: The patient(s) is predicted to have 2 ED/inpatient visits for respiratory events over the 12-month period after the visit

Endotype 3: The patient(s) is predicted to have >2 ED/inpatient visits for respiratory events over the 12-month period after the visit

**General R-part model M0:**

Recursive partitioning and decision trees

post_ed ~ age_at_visit + sex + race + visit_type + pre_ed + icd_codes + despm_yda + deso_7da

*Clinical data:* Please see [Green Team Clinical Data Documentation](https://github.com/NCATS-Tangerine/cq-notebooks/tree/master/Green_CQs/GreenTeam_Clinical_Data_Documentation)

