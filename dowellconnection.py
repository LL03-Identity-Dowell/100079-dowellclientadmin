import json
import requests

url = 'http://100002.pythonanywhere.com/'

def dowellconnection(cluster,platform,database,collection,document,team_member_ID,function_ID,command,field,update_field):

    data= json.dumps({
      "cluster": cluster,
      "platform": platform,
      "database": database,
      "collection": collection,
      "document": document,
      "team_member_ID": team_member_ID,
      "function_ID": function_ID,
      "command": command,
      "field": field,
      "update_field":update_field
       })
    headers = {'content-type': 'application/json'}
    response = requests.request('POST',url, headers=headers,data=data)
    return response.text
    if command=="fetch":
        response_data = response.json()
        return str(response_data[0])
    else:
        return response.text

# pfm={"platformcode":"FB"}
# pfm_response=dowellconnection("mstr","bangalore","mysql","platform_master","pfm_master","97654321","ABCDE","fetch",pfm,"nil")
# print(pfm_response)

# searchstring="ObjectId"+"("+"'"+"6139bd4969b0c91866e40551"+"'"+")"
# payload = json.dumps({
#   "cluster": "login",
#   "database": "login",
#   "collection": "registration",
#   "document": "registration",
#   "team_member_ID": "10004545",
#   "command": "fetch",
#   "function_ID": "ABCDE",
#   "field": {
#     "Username":"Admin"
#   },
#   "update_field":"nil",
#   "platform": "bangalore"
# })
# headers = {
#   'Content-Type': 'application/json'
# }

# response = requests.request("POST", url, headers=headers, data=payload)
# print(response.text)