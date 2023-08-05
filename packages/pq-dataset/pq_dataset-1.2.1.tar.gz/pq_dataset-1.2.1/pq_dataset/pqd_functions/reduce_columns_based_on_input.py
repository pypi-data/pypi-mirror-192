from typing import List
import pandas as pd
import logging

from pq_dataset.logging.DummyLogger import DummyLogger


def reduce_columns_based_on_input(df: pd.DataFrame,
                                  relevant_scopes: List[str] = [], 
                                  relevant_variables: List[str] = []
                                    )-> pd.DataFrame:

    def validate_inputs(existing_columns: List[str], 
                        relevant_scopes: List[str], 
                        relevant_variables: List[str] = []) -> None:
        
        for scope in relevant_scopes:
            nb_cols_with_scope = [col for col in existing_columns if col.startswith(scope)]
            
            if len(nb_cols_with_scope) == 0:
                logger.warning(f'No columns were found starting with {scope}. This indicates an error in the specification of relevant_scopes')
        
        if relevant_variables:
            for variable in relevant_variables:
                if not variable in existing_columns:
                    logger.warning(f'The variable {variable} was not found in dataset. This indicates an error in the specification of relevant_variables')
                    
        return None

    logger = logging.getLogger(__name__) if logging.getLogger().hasHandlers else DummyLogger()        
    logger.debug(f'Started reduce_columns_based_on_input')
            
    validate_inputs(df.columns, relevant_scopes, relevant_variables)
    
    # Only select the variable scopes defined in relevant_scopes
    relevant_cols: List[str] = [col for col in df.columns for scope in relevant_scopes if col.startswith(scope)]

    # Appending individual variables
    if relevant_variables:
        relevant_cols.extend(relevant_variables)

    # Reducing number of columns in dataframe
    df = df[[col for col in df.columns if col in relevant_cols]]
    
    return df