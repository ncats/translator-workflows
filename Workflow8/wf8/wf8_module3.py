"""Wrapper object to call the ddot api"""

import os
import requests
from time import sleep
import pandas as pd
from uuid import uuid4

from config_mod3 import PATHS


class DDOT_Client(object): 

    DDOT_API = PATHS['ddot-api-url'] 

    def __init__(self, filename, verbose=False):
        """Constructs the DDOT_caller object from file
        
        Parameters
        ----------
        filename : str
            System path to the file to be sent to DDOT server. 
            The file is expected to have 3 columns with no headers
            and no indices. The first two columns represent the node
            names and the third column represent the similarity score 
            between the nodes
        """

        if os.path.isfile(filename): 
            self.dataframe_path = filename
            self.verbose = verbose

        else: 
            raise ValueError("filename is not a valid path!")

    @classmethod 
    def from_dataframe(cls, dataframe, verbose=False):
        """Constructs the DDOT_caller object from pandas DataFrame

        Parameters
        ----------
        dataframe : pd.DataFrame
            Three column file dataframe. Header and indices are ignored. 
            The first two columns represent the node name and the third
            column is the similarity score between the two nodes (edge
            weight). 
        verbose : bool
            Determines whether the status will be output to standard out
        """

        if not isinstance(dataframe, pd.DataFrame): 
            raise ValueError("dataframe must be a pandas DataFrame!") 
        
        self.dataframe = dataframe
        filename = self._save_dataframe(dataframe) 

        return cls(filename, verbose=verbose)

        
    def _save_dataframe(self, dataframe, path=''):
        """Writes a dataframe to a temporary file and returns the path

        Parameters
        ---------- 
        dataframe : pd.DataFrame 
            See __init__ for requirements of dataframe 
        """
        
        tmp_file = os.path.join(path, str(uuid4())) 
        dataframe.to_csv(tmp_file, sep='\t', header=None, index=None)

        return tmp_file


    def call(self, alpha=0.05, beta=0.5, ndexname='MyOntology'): 
        """Calls the ddot API

        Parameters
        ----------
        alpha : float 
            Controls the depth of the hierarchy 
        beta : float 
            Controls the breadth of the hierarchy
        ndexname : str
            The name of the hierarchy designated in NDEx 
        """

        self.request = requests.post(
            self.DDOT_API, 
            data={
                'alpha': alpha, 
                'beta': beta, 
                'ndexname': ndexname, 
            }, 
            files={'interactionfile': open(self.dataframe_path, "rb")}

        )

        if self.request.status_code == 202: 
            self.location = self.request.headers['Location'] 

        else:  
            raise RuntimeError("DDOT API call failed! Check ddot api website for more details on error code: %s" % self.request.status_code)

        return self


    def get_job_status(self): 
        """Gets CliXO job status""" 

        if not hasattr(self, "request"): 
            return "Unsubmitted"

        else: 
            r = requests.get(self.location)
            
            return r.json()['status'] 

    
    def wait_for_hiview_url(self): 
        """Continuously polls the DDOT server for job status
        
        If the API call is sucessful, the hiview url will be found as an 
        attribute called `hiview_url`.

        """ 

        if not hasattr(self, "request"): 
            raise ValueError("No request attribute found. Please use the `call` method first!")

        count = 1
        while True: 
            if self.get_job_status() != "done": 
                sleep(count) 
                count += 1
                
            else:
                r = requests.get(self.location)
                self.hiview_url = r.json()['result']['hiviewurl']

                if self.hiview_url: 
                    return self.hiview_url 

                else: 
                    raise RuntimeError("DDOT job run failed! Error code: %s" % r.status_code) 

                break 

        
