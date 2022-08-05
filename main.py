import pandas as pd
import numpy as np

def read_file() -> pd.DataFrame:
    df = pd.read_excel('input_data.xlsx')
    return df

# Munging functions
# To be continually enhanced as new anomalies arise    
def clean_datetime(raw_value):
    clean_value = np.NaN
    try: 
        clean_value = pd.to_datetime(raw_value)
    except ValueError:
        if isinstance(raw_value, str):
            raw_value = raw_value.replace('O','0').replace('o','0')
            try:
                clean_value = pd.to_datetime(raw_value)
            except ValueError:
                print(f'Cannot parse {raw_value}')
    except:
        print('parse error')
    return clean_value

def clean_int(raw_value):
    clean_value = np.NaN
    try: 
        clean_value = int(raw_value)
    except ValueError:
        if isinstance(raw_value, str):
            raw_value = raw_value.replace('O','0').replace('o','0')
            try:
                clean_value = int(raw_value)
            except ValueError:
                print(f'Cannot parse {raw_value}')
    except:
        print('parse error')
    return clean_value

#Computer tax rates
def get_tax_rate(state):
    state_rates = {'IL': .0251, 'TN': .01766, }
    return state_rates[state]

#Calculates 
def get_gwps(report_date, effective_date, expiration_date, annual_gwp):
    daily_gwp = annual_gwp/365
    effective_days = (expiration_date - effective_date).days
    days_effective = (report_date - effective_date).days if report_date < expiration_date else effective_days
    days_remaining = effective_days - days_effective
    return daily_gwp*effective_days, daily_gwp*days_effective, daily_gwp*days_remaining

#Write to new file
def write_new_file(aggregated_data_frame: pd.DataFrame, report_date: str):
    aggregated_data_frame.to_excel(f'aggregated_report-{report_date}.xlsx')
    return

def main():
    report_date = '2022-08-01'
    df = read_file()
    # your processing here
    #Add Report Date, in datetime format
    df['Report Date'] = pd.to_datetime('8/1/2022')
    #Validate/clean existing date fields, ensure in datetime format
    df['Effective Date'] = df['Effective Date'].apply(clean_datetime)
    df['Expiration Date'] = df['Expiration Date'].apply(clean_datetime)
    #Validate/clean existing amts. Currently treats ammounts as whole numbers.
    df['Annual GWP'] = df['Annual GWP'].apply(clean_int)
    df[['Pro-rata GWP','Earned Premium','Unearned Premium']] = df[['Report Date','Effective Date','Expiration Date','Annual GWP']].apply(lambda x: get_gwps(*x), axis=1, result_type='expand')
    df['Tax'] = df.apply(lambda x: x['Pro-rata GWP']*get_tax_rate(x['State']), axis=1)
    df = df.groupby(['Company Name','Report Date']) \
        .agg({'VIN':'count','Annual GWP':'sum','Pro-rata GWP':'sum','Earned Premium':'sum','Unearned Premium':'sum','Tax':'sum'}) \
        .reset_index() \
        .rename(columns={'VIN':'Total Count of Vehicles (VINs)', 'Annual GWP':'Total Annual GWP','Pro-rata GWP':'Total Pro-Rata GWP','Earned Premium':'Total Earned Premium','Unearned Premium':'Total Unearned Premium','Tax':'Total Taxes'})
        #.round(2) <-- Uncomment if figures to be presented in whole cents
    #Above to provide full precision, for internal use. If full cent-expression, required uncomment rounding line.
    write_new_file(df, report_date)
    return

if __name__ == "__main__":
    main()