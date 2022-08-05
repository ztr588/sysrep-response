import random
import datetime
import main as test_script

def main():
    valid_count = 0
    for x in range(100):
        valid = False
        annual_gwp = random.randint(7000, 14000)
        print(f'Annual GWP: {annual_gwp}')
        effective_date = datetime.datetime(random.randint(2021,2022),random.randint(1,7), random.randint(1,27))
        print(f'Effective Date: {effective_date}')
        exp_days_add = random.randint(270,364)
        rpt_days_add = random.randint(90, exp_days_add)
        expiration_date = effective_date + datetime.timedelta(days=exp_days_add)
        print(f'Expiration Date: {expiration_date}')
        report_date = effective_date + datetime.timedelta(days=rpt_days_add)
        print(f'Report Date: {report_date}')
        # state = ['IL','TN'][random.randint(0,1)]
        # print(f'State: {state}')
        tst_tot_gwp, tst_earned_gwp, tst_unearned_gwp = test_script.get_gwps(report_date, effective_date, expiration_date, annual_gwp)
        #difference between the parts and the whole must be less than $0.01
        valid = abs((tst_earned_gwp + tst_unearned_gwp) - tst_tot_gwp) < 0.01
        print(f'{tst_earned_gwp} + {tst_unearned_gwp} = {tst_tot_gwp}: {valid}. Difference: {(tst_earned_gwp + tst_unearned_gwp) - tst_tot_gwp}')
        if valid:
            valid_count = valid_count + 1
    print(f'Total valid: {valid_count}')
    print(f'Overall result {"PASS" if valid_count == 100 else "FAIL"}')



if __name__ == "__main__":
    main()