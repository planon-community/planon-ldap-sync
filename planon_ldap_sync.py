#! /bin/env python3

import os
import ldap
import yaml
import zeep

# Open settings YAML file
with open ("./settings.yaml") as settings_file:
    settings = yaml.safe_load(settings_file)

# Get secrets from provided environment variables
ldap_username = os.environ['LDAP_USER']
ldap_password = os.environ['LDAP_PWD']

planon_username = os.environ['PLANON_USER']
planon_password = os.environ['PLANON_PWD']

# Query LDAP for current membership
ldap_connection = ldap.initialize(settings['ldap'])
ldap_connection.simple_bind_s(ldap_username, ldap_password)

for environment in settings:
    # Set baseURL for the instance set in the setting YAML file
    baseURL = f"https://{environment['instance']}/nyx/services/"
    
    token = zeep.Client(baseURL + 'PlanonSession?wsdl').service.login(planon_username, planon_password)

    group_client = zeep.Client(f'{baseURL}AccountGroup?wsdl')
    user_client = zeep.Client(f'{baseURL}Account?wsdl')

    for group in environment['groups']:
        group_filter = f"(&(objectClass=GROUP)(distinguishedName={group['source']}))"
        group_result = ldap_connection.search_s(environment['ldapBaseDN'], ldap.SCOPE_SUBTREE, group_filter)

