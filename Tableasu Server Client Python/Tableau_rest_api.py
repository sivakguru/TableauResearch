import requests
from pprint import pprint
import xml.etree.ElementTree as ET
import logging

payload = '''
<tsRequest>
	<credentials name="siva.dhanush.007@gmail.com" password="sridevis007">
		<site contentUrl="vizsivadev749967" />
	</credentials>
</tsRequest>
'''

res = requests.post('https://10ax.online.tableau.com/api/3.4/auth/signin', data=payload)
res_xml = ET.fromstring(res.content)

cred_obj = res_xml[0]
token = cred_obj.attrib['token']
site_obj = res_xml[0][0]
site_id = site_obj.attrib['id']
auth = dict(
    token = token,
    site=site_id
)
res1 = 0