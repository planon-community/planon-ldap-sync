#! /bin/env python3

import os

import logger

import ldap
import yaml
import zeep

log = logger.logging.getLogger(__name__)

# Open settings YAML file
with open ("./settings.yaml") as settings_file:
    settings = yaml.safe_load(settings_file)

# Get secrets from provided environment variables
ldap_username = os.environ['LDAP_USER']
ldap_password = os.environ['LDAP_PWD']

planon_username = os.environ['PLANON_USER']
planon_password = os.environ['PLANON_PWD']

for environment in settings:
    # Query LDAP for current membership
    ldap_connection = ldap.initialize(environment['ldap'])
    ldap_connection.simple_bind_s(ldap_username, ldap_password)

    # Set baseURL for the instance set in the setting YAML file
    baseURL = f"https://{environment['instance']}/nyx/services/"
    
    token = zeep.Client(baseURL + 'PlanonSession?wsdl').service.login(planon_username, planon_password)

    person_client = zeep.Client(f'{baseURL}Person?wsdl')
    group_client = zeep.Client(f'{baseURL}AccountGroup?wsdl')
    user_client = zeep.Client(f'{baseURL}Account?wsdl')

    for group in environment['groups']:
        group_filter = f"(&(objectClass=GROUP)(distinguishedName={group['source']}))"
        dn, group_result = ldap_connection.search_s(base=environment['ldapBaseDN'], scope=ldap.SCOPE_SUBTREE, filterstr=group_filter, )[0]

        if dn:
            log.debug(f"Found {group['source']} found in LDAP")

            if group_result['member']:
                for member in group_result['member']:
                    user_filter = f"(&(objectClass=USER)(distinguishedName={member.decode('utf-8')}))"
                    dn, user_result = ldap_connection.search_s(environment['ldapBaseDN'], ldap.SCOPE_SUBTREE, user_filter)[0]
            else:
                #TODO REMOVE ALL MEMBERS
                pass
        else:
            log.warn(f"Group {group['source']} not found in LDAP")

    ldap_connection.unbind()