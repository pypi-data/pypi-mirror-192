import mccd

test_case = 1
fits_table_pos = 2

config_file_path = '/Users/tliaudat/Documents/PhD/github/' + \
    'cosmostat_official/mccd/tests/hidden_tests/test_config_MCCD.ini'
# config_file_path = '/Users/tliaudat/Documents/PhD/github' + \
#   '/cosmostat_official/mccd/config_MCCD.ini'

if test_case == 1:
    # Test fit
    run_mccd_instance = mccd.auxiliary_fun.RunMCCD(
        config_file_path,
        fits_table_pos=fits_table_pos,
    )
    run_mccd_instance.fit_MCCD_models()
elif test_case == 2:
    # Test validation
    run_mccd_instance = mccd.auxiliary_fun.RunMCCD(
        config_file_path,
        fits_table_pos=fits_table_pos,
    )
    run_mccd_instance.validate_MCCD_models()

elif test_case == 3:
    # Test fit and validation
    run_mccd_instance = mccd.auxiliary_fun.RunMCCD(
        config_file_path,
        fits_table_pos=fits_table_pos,
    )
    run_mccd_instance.run_MCCD()

print('Good bye!')
