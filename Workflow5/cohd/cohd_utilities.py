import numpy as np
from scipy.stats import poisson

def LnRatioConfInt(freq, ln_ratio, interval=0.99):
  # Convert ln_ratio back to ratio and calculate confidence intervals for the ratios
  return np.log(np.array(poisson.interval(interval, freq)) * np.exp(ln_ratio) / freq)
  
def PoissonSignificance1(x, interval=0.99):   
    # Helper function for determining if ln_ratio is significantly different from 0; apply to dataframe
    # 
    # Parameters
    # x: series
    # interval: confidence interval
    
    ci = LnRatioConfInt(x.observed_count, x.ln_ratio, interval)
    
    # Check if the confidence interval include 0
    return [ci, (ci[0] > 0) or (ci[1] < 0)]
  
def PoissonSignificance2(x, c_oc1, c_oc2, c_lr1, c_lr2, interval=0.99):   
    # Helper function for determining significance between two ln_ratios; apply to dataframe
    # 
    # Parameters
    # x: series
    # c_oc1: column name for observed_count of first variable
    # c_oc2: column name for observed_count of second variable
    # c_lr1: column name for ln_ratio of first variable
    # c_lr2: column name for ln_ratio of second variable
    # interval: confidence interval    
    
    # Use 99% confidence interval for stricter standards for multiple comparisons and somewhat compensate for variance in original co-occurrences in addition to Poisson randomization
    ci1 = LnRatioConfInt(x[c_oc1], x[c_lr1], interval)
    ci2 = LnRatioConfInt(x[c_oc2], x[c_lr2], interval)
    
    # Check if the ci2 overlap
    return [ci1, ci2, (ci1[0] > ci2[1]) or (ci2[0] > ci1[1])]
    
def FindConcept(x, name):
    # Helper function to find rows with concept_2_name including name 
    return x.concept_2_name.lower().find(name.lower()) >= 0 