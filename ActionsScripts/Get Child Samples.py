# Import built-in libraries
import json

# Import Siemplify libraries
from SiemplifyAction import SiemplifyAction
from SiemplifyUtils import output_handler
from ScriptResult import EXECUTION_STATE_COMPLETED, EXECUTION_STATE_FAILED

# Import conntector related libraries
from Conf import VMRayConfig, INTEGRATION_NAME, GET_CHILD_SAMPLES_SCRIPT_NAME
from VMRayApiManager import VMRay


@output_handler
def main():
    siemplify = SiemplifyAction()
    siemplify.script_name = GET_CHILD_SAMPLES_SCRIPT_NAME
    
    siemplify.LOGGER.info("----------------- Main - Param Init -----------------")
    
    # Initializing integration parameters for Get Child Samples Action
    api_key = siemplify.extract_configuration_param(provider_name=INTEGRATION_NAME, 
                                                    param_name="API_KEY",
                                                    input_type=str,
                                                    is_mandatory=True,
                                                    print_value=False)
    url = siemplify.extract_configuration_param(provider_name=INTEGRATION_NAME,
                                                param_name="URL",
                                                input_type=str,
                                                is_mandatory=True,
                                                print_value=True)
    ssl_verify = siemplify.extract_configuration_param(provider_name=INTEGRATION_NAME, 
                                                       param_name="SSL_VERIFY",
                                                       input_type=bool,
                                                       is_mandatory=True,
                                                       print_value=True)
    
    # initializing action specific parameters for Get Child Samples Action
    sample_id = siemplify.extract_action_param(param_name="SAMPLE_ID",
                                                input_type=str,
                                                is_mandatory=True,
                                                print_value=True)

    VMRayConfig.API_KEY = api_key
    VMRayConfig.URL = url
    VMRayConfig.SSL_VERIFY = ssl_verify
    
    siemplify.LOGGER.info("----------------- Main - Started -----------------")
    
    # Initializing VMRay API Instance
    vmray = VMRay(siemplify.LOGGER, VMRayConfig)
    
    try:
        # Authenticating VMRay API
        vmray.authenticate()
        
        # Doing healtcheck for VMRay API endpoint
        vmray.healthcheck()
        
        # Retrieving child samples with given sample_id
        child_samples = vmray.get_child_samples(sample_id)
        
        # Checking child samples
        if child_samples is not None:
            
            # used to flag back to siemplify system, the action final status
            status = EXECUTION_STATE_COMPLETED  
        
            # human readable message, showed in UI as the action result
            output_message = "Child samples retrieved successfully for %s" % sample_id
        
            # Set a simple result value, used for playbook if\else and placeholders.
            result_value = True
            
            # Adding sample metadata to result json
            siemplify.result.add_result_json(json.dumps({"child_samples":child_samples}))
            
            siemplify.LOGGER.info("%s action finished successfully." % GET_CHILD_SAMPLES_SCRIPT_NAME)
        else:
            # used to flag back to siemplify system, the action final status
            status = EXECUTION_STATE_FAILED  
        
            # human readable message, showed in UI as the action result
            output_message = "No child sample for %s was found in VMRay database." % sample_id
        
            # Set a simple result value, used for playbook if\else and placeholders.
            result_value = False
            
            siemplify.LOGGER.info("%s action failed." % GET_CHILD_SAMPLES_SCRIPT_NAME)
    except Exception as err:
        # used to flag back to siemplify system, the action final status
        status = EXECUTION_STATE_FAILED
        
        # human readable message, showed in UI as the action result
        output_message = "No child sample for %s was found in VMRay database. Error: %s" % (sample_id, err)
        
        # Set a simple result value, used for playbook if\else and placeholders.
        result_value = False
        
        siemplify.LOGGER.error("%s action finished with error." % GET_CHILD_SAMPLES_SCRIPT_NAME)
        siemplify.LOGGER.exception(err)

    siemplify.LOGGER.info("----------------- Main - Finished -----------------")

    siemplify.LOGGER.info("\n  status: %s\n  result_value: %s\n  output_message: %s" % (status, result_value, output_message))
    siemplify.end(output_message, result_value, status)


if __name__ == "__main__":
    main()
