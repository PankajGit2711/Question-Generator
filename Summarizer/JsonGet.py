import requests
# r = requests.get('http://ec2-13-234-155-85.ap-south-1.compute.amazonaws.com:8081/api/all')
# data = r.json()
# for i in data:
#     final_data = i['command']
#     print(final_data)

payload = "something or nothing"
post_r = requests.post('http://ec2-13-234-155-85.ap-south-1.compute.amazonaws.com:8081/api/insert?' + 'command='+payload)
posted_r = post_r.json()
print(post_r.text)
