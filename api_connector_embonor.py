import pandas as pd
from API.embonor_api import EmbonorAPI
from datetime import datetime
import sys

API_CONTROL_FILE = 'call_control.xlsx'

def loading_config_info():
    df_api_control = pd.read_excel(API_CONTROL_FILE, dtype=str, header=0).fillna('')
    return df_api_control


def sanitizing_df_api_control(df_api_control):

    df_api_control = df_api_control[~df_api_control.index.duplicated(keep='first')]
    df_api_control.columns = [column.strip() for column in df_api_control.columns]
    for column in df_api_control.columns[1:]:
        df_api_control[column] = df_api_control[column].str.strip().str.lower()
    
    df_api_control['key_index'] = df_api_control['CALL']
    df_api_control.set_index(['key_index'], inplace=True)

    return df_api_control


def slicing_to_be_processed_calls(df_api_control):

    to_be_dropped = df_api_control[df_api_control['TO_BE_PROCESSED'] != 'y'].index
    df_api_control.drop(to_be_dropped, inplace=True)

    return df_api_control


def creating_dicts(df_api_control):

    dict_of_call_parameters = {}

    #We are using as parameteres just values from the second column of the control file
    columns_to_be_checked = df_api_control.columns[2:] 

    for api_call_type in df_api_control.index:
        list_of_values_of_call = df_api_control.loc[api_call_type].to_list()[2:]
        dict_of_call_parameters[api_call_type] = dict(zip(columns_to_be_checked, list_of_values_of_call))
    
    return dict_of_call_parameters


def writing_files(file_name, api_response):

    final_file_name = f'{file_name}_{datetime.today().strftime("%Y%m%d_%H%M%S")}.csv'
    pd.DataFrame(api_response).to_csv(final_file_name, sep=';', index=False)

    return True


def main():
    
    try:
        df_api_control = loading_config_info()
        df_api_control = sanitizing_df_api_control(df_api_control)
        df_api_control = slicing_to_be_processed_calls(df_api_control)
        dict_of_call_parameters = creating_dicts(df_api_control)
        api_connector = EmbonorAPI()
    except Exception as error:
        print(error)
        sys.exit(1)

    for call_type, params in dict_of_call_parameters.items():
        try:
            string_api = f'{call_type}?inicio={params["START_DATE"]}&termino={params["END_DATE"]}'
            response = api_connector.call_api(string_api)

            writing_files(call_type, response)
        except Exception as error:
            print(error)
    input('Finished\n')

if __name__ == '__main__':
    main()