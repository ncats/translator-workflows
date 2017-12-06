#
# Example of two Swagger client mechanisms talking to Biolink
#
# This script executes one or both of the following Swagger mechanisms
#   swagger_codegen: https://github.com/swagger-api/swagger-codegen
#   Bravado: https://github.com/Yelp/bravado
#
# Setup:
#  pip install bravado
#  brew install swagger-codegen (MacOSX only)
#
# Validation Tools:
#  The following site is useful in debugging issues with swagger.json:
#   http://bigstickcarpet.com/swagger-parser/www/index.html
#
#
# The variables useBravado and useSwaggerCodegen control which is exercised.
#
# In the case of Bravado, there is the option of validating the swagger.json
# However, the current version of swagger.json has some validation errors,
# so this is disabled by default.
#
# The Bravado example assumes that the swagger.json file has been loaded locally,
# mostly so that I could correct validation errors in it. It is also possible
# to have these clients pull the swagger.json directly from the API endpoint.
#

import pprint

useSwaggerCodegen = True
useBravado = True
useBravadoRemote = True

host = "https://api.monarchinitiative.org/api"
gene_id = "NCBIGene:6469"

if useSwaggerCodegen:
    # biolink_client is generated from swagger_codegen via the following:
    #   swagger-codegen generate \
    #       --verbose \
    #       -i swagger.json \
    #       -l python \
    #       -o ./biolink_client \
    #       -c ./swagger-conf.json
    #   cd biolink_client
    #   python setup.py install
    #   cd ..

    import biolink_client
    from biolink_client.api_client import ApiClient
    from biolink_client.rest import ApiException

    print("\n\nuseSwaggerCodegen\n\n")
    client = ApiClient(host=host)

    #
    # Setting the Content-Type is necessary because the Biolink server
    # rejects request with Content-Type: application/json (the swagger_codegen default)
    #
    client.set_default_header('Content-Type', 'text/plain')
    api_instance = biolink_client.BioentityApi(client)

    try:
        api_response = api_instance.get_gene_interactions(gene_id)
        print('swagger_codegen result')
        print(api_response)
    except ApiException as e:
        print("Exception when calling Biolink->get_gene_interactions: %s\n" % e)



if useBravado:
    print("\n\nuseBravado\n\n")
    import json
    from bravado.client import SwaggerClient

    from bravado.requests_client import RequestsClient
    from bravado.client import SwaggerClient

    bravado_config = {
        'validate_swagger_spec': True,
        'validate_requests': False,
        'validate_responses': False,
        'use_models': False,
        'also_return_response': False
    }

    if useBravadoRemote:
        bravado_config['validate_swagger_spec'] = False
        client = SwaggerClient.from_url(
                    host + '/swagger.json',
                    config=bravado_config)

    else:
        from bravado_core.spec import Spec

        # Load local swagger.json, but adjust it to point at correct host
        spec_dict = json.load(open('swagger.json'))
        spec_dict['host'] = 'api.monarchinitiative.org'
        client = SwaggerClient.from_spec(
                    spec_dict,
                    config=bravado_config)


    try:
        result = client.bioentity.get_gene_interactions(id=gene_id).result()
        print('Bravado result')
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(result)

    except Exception as e:
        print("Exception when calling client.bioentity.get_gene_interactions: %s\n" % e)


# import requests
# # Or alternatively without the swagger client
# req = requests.get('{}/bioentity/gene/{}/interactions/'.format(host, gene_id))
# response = req.json()
# print(response)

