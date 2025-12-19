import yaml
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import sys
import pickle
import dill
import os
import numpy as np

def read_yaml_file(file_path:str)->dict:
    """Reads a YAML file and returns its contents as a dictionary.

    Args:
        file_path (str): The path to the YAML file.
    Returns:
        dict: The contents of the YAML file as a dictionary.
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_numpy_array_data(file_path: str, array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e

def save_object(file_path:str, obj:object)->None:
    """Saves a Python object to a file using dill serialization.

    Args:
        file_path (str): The path to the file where the object will be saved.
        obj (object): The Python object to be saved.
    """
    try:
        logging.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise NetworkSecurityException(e, sys)



def load_object(file_path:str)->object:
    """Loads a Python object from a file using dill serialization.

    Args:
        file_path (str): The path to the file from which the object will be loaded.
    Returns:
        object: The Python object loaded from the file.
    """
    try:
        logging.info("Entered the load_object method of utils")
        with open(file_path, 'rb') as file_obj:
            obj = pickle.load(file_obj)
        logging.info("Exited the load_object method of utils")
        return obj
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def load_numpy_array_data(file_path: str) -> np.array:
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e