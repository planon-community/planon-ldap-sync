#! /bin/env python3

import os
import ldap
import yaml
import zeep

# Open settings YAML file
with open ("./settings.yaml") as settings_file:
    settings = yaml.safe_load(settings_file)

# Set baseURL for the instance set in the setting YAML file
baseURL = "https://" + settings['instance'] + ".planoncloud.com/nyx/services/"

# Get secrets from provided environment variables
ldap_username = os.environ['LDAPUSER']
ldap_password = os.environ['LDAPPWD']

planon_username = os.environ['PLANONUSER']
planon_password = os.environ['PLANONPWD']

token = zeep.Client(baseURL + 'PlanonSession?wsdl').service.login(planon_username, planon_password) 

# Query LDAP for current membership
ldap_connection = ldap.initialize(settings['ldap'])
ldap_connection.simple_bind_s(ldap_username, ldap_password)

for group in settings['groups']:
    group_filter = f"(&(objectClass=GROUP)(distinguishedName={group['source']}))"
    group_result = ldap_connection.search_s(settings['ldapBaseDN'], ldap.SCOPE_SUBTREE, group_filter)

    # Setup the new WSDL client for accountGroups
    accountgroupClient = zeep.Client(baseURL + 'AccountGroup?wsdl')

    # Determine the namespace for accountGroups
    group_namespace = list(accountgroupClient.namespaces.keys())[list(accountgroupClient.namespaces.values()).index(f"http://accountgroup.{settings['webservice']}.ws/xsd")]
    groupFilter = accountgroupClient.get_type(f"{group_namespace}:AccountGroupFilter")(accountgroupClient.get_type('ns0:FieldFilter')('PnName', group['destination'], 'equals'))
    accountGroupId = accountgroupClient.service.find(token, groupFilter)[0]

    if group_result[0][1]['member']:
        for member in group_result[0][1]['member']:
            user_filter = f"(&(objectClass=USER)(distinguishedName={member.decode('utf-8')}))"
            user_result = ldap_connection.search_s(settings['ldapBaseDN'], ldap.SCOPE_SUBTREE, user_filter)

            # Setup the new WSDL client for accounts
            accountClient = zeep.Client(baseURL + 'Account?wsdl')

            # Determine namespace for accounts
            account_namespace = list(accountClient.namespaces.keys())[list(accountClient.namespaces.values()).index(f"http://account.{settings['webservice']}.ws/xsd")]
            accountFilter = accountClient.get_type(f"{account_namespace}:AccountFilter")(accountClient.get_type('ns1:FieldFilter')('Accountname', user_result[0][1]['sAMAccountName'][0].decode('utf-8'), 'equals'))
            accountId = accountClient.service.find(token, accountFilter)[0]

            # Add group account link
            print(f"Adding {user_result[0][1]['sAMAccountName'][0].decode('utf-8')} to {group['destination']}\r")
            accountgroupClient.service.connectToAccountGroupAccount(token, accountGroupId, accountId)
