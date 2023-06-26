from datetime import datetime
import requests

# removed data for privacy
api_key = 'REPLACE_WITH_API_KEY'
api_token = 'REPLACE_WITH_TOKEN'
member_id = 'REPLACE_WITH_ACCOUNT_ID'

# Make a GET request to the /members/{memberId}/organizations endpoint to get a list of all organizations that the member belongs to
response = requests.get(f'https://api.trello.com/1/members/{member_id}/organizations?key={api_key}&token={api_token}')

if response.status_code == 200:
    # Initialize an empty list to store the results
    orgs = []
    # Loop through each organization and check if its name matches the specified format
    for org in response.json():
        org_name = org['displayName']
        if 'Team Activity Jan-June' in org_name or 'Team Activity July-Dec' in org_name:
            org_id = org['id']
            org_year = int(org_name.split()[-1])
            org_type = 1 if 'Jan-June' in org_name else 2
            orgs.append({'name': org_name, 'id': org_id, 'year': org_year, 'type': org_type})
else:
    print("Failed to get organizations")

# Initialize an empty dictionary to store the workspace IDs
workspace_ids = {}

# Loop through each organization and add its ID to the workspace_ids dictionary
for org in orgs:
    year = org['year']
    org_type = org['type']
    org_id = org['id']
    if year not in workspace_ids:
        workspace_ids[year] = {}
    workspace_ids[year][org_type] = org_id

input_date = input_data['Event Date']

date_obj = datetime.strptime(input_date, '%d-%m-%Y')

#Replace 20 with the number of years you want to generate the data range for
for year in range(date_obj.year, date_obj.year + 20): 
    if year not in workspace_ids:
        continue  # Skip years that are not in the workspace_ids dictionary
    if date_obj.month <= 6:
        workspace_id = workspace_ids[year].get(1, 'Workspace ID not found for year and half-year')
    else:
        workspace_id = workspace_ids[year].get(2, 'Workspace ID not found for year and half-year')
    output = {'Workspace ID': workspace_id}
    break
else:
    output = {'Workspace ID': 'Date not in range.'}

return output