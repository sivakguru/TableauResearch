#Tableau Server Info RR

#install Tableau server client for python
    #pip install tableauserverclient

import tableauserverclient as TSC
import pandas as pd
from PIL import Image
from array import array
import io

#set up authentication RR Deveoper account
server = TSC.Server('https://10ax.online.tableau.com')
server.use_server_version()
tableau_auth = TSC.TableauAuth('thulasiramvanniya@gmail.com', 'Sairam@2903', 'thulasiramdev938591')
tableau_auth = TSC.TableauAuth('siva.dhanush.007@gmail.com', 'sridevis007', 'vizsivadev749967')
#sign-in to server
server.auth.sign_in(tableau_auth)

request_options = TSC.RequestOptions()
all_workbooks = list(TSC.Pager(server.workbooks, request_options))
all_views = list(TSC.Pager(server.views, request_options))
all_users = list(TSC.Pager(server.users, request_options))

#find the user name using Owner ID
if all_workbooks[0].owner_id == all_users[0].id:
    print(all_users[0].name)

#find the user name for all the workbooks using the owner ID
for wb in range(len(all_workbooks)):
    for usr in range(len(all_users)):
        if all_workbooks[wb].owner_id == all_users[usr].id:
            print(all_workbooks[wb].name, all_users[usr].name)

#get workbook items by ID
test_wb = server.workbooks.get_by_id(all_workbooks[0].id)
#get all workbook items with pagination details
test_wb = server.workbooks.get()

#load all workbook items by using workbook ID
workbook_info = []
for wb in range(len(all_workbooks)):
    workbook_info.append(server.workbooks.get_by_id(all_workbooks[wb].id))

###################
server.workbooks.populate_views(workbook_info[0])
print([view.name for view in test_wb.views],
[view.project_id for view in test_wb.views])

#############
vw_id = []
vw_name = []
wb_id = []
wb_name = []
proj_id = []
proj_name = []
owner_id = []
owner_name = []
vw_image = []

for wb in range(len(workbook_info)): 
    server.workbooks.populate_views(workbook_info[wb])
    for view in workbook_info[wb].views:
        wb_id.append(workbook_info[wb].id)
        wb_name.append(workbook_info[wb].name)
        proj_id.append(workbook_info[wb].project_id)
        proj_name.append(workbook_info[wb].project_name)
        owner_id.append(workbook_info[wb].owner_id)
        for usr in range(len(all_users)):
            if all_workbooks[wb].owner_id == all_users[usr].id:
                owner_name.append(all_users[usr].name)
        vw_id.append(view.id)
        vw_name.append(view.name)
        server.views.populate_image(view)
        vw_image.append(Image.open(io.BytesIO(view.image)))

df = pd.DataFrame.from_dict({'proj_id' : proj_id,
'proj_name' : proj_name,
'wb_id': wb_id,
'wb_name' : wb_name,
'vw_id' : vw_id,
'vw_name' : vw_name,
'owner_id' : owner_id,
'owner_name' : owner_name,
'vw_image' : vw_image})

#view image from a data frame
df.iloc[0]['vw_image']


#populating the Images for Workbook and views
#image of a view
server.views.populate_image(all_views[0])
pic = Image.open(io.BytesIO(all_views[0].image))
pic.show()

#thumbnail of a workbook
server.workbooks.populate_preview_image(workbook_info[0])
wb_pic = Image.open(io.BytesIO(workbook_info[0].preview_image))


