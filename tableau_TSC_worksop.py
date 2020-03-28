#install Tableau server client for python
    #pip install tableauserverclient


#Tableau server accesstoken : iMUgahYuSiqXXisFrBPr+A==:biVQjxSOJW6LbiCkQG5djkwDqEAoLOAY


import tableauserverclient as TSC
#pandas for Data frame capabilities
import pandas as pd
#PIL for handeling Image files
from PIL import Image
#array
from array import array
#io to read bytes image data types
import io
#parse all the required arguments -- specific to a tableau server
import argparse
#get password on the run
import getpass
#working with file directories
import os

#set up authentication RR Deveoper account
server = TSC.Server('https://10ax.online.tableau.com')
server.use_server_version()
tableau_auth = TSC.TableauAuth('thulasiramvanniya@gmail.com', 'Sairam@2903', 'thulasiramdev938591')

server.auth.sign_in(tableau_auth)


#set up authentication RR Deveoper account
server = TSC.Server('https://10ax.online.tableau.com')
#if SSL Security fails use the uncomment the below line to make ssl certificate verification off
# server.add_http_options({'verify': False})
server.use_server_version()
tableau_auth = TSC.TableauAuth('siva.dhanush.007@gmail.com', 'Developer_123', 'vizsivadev749967')
#sign-in to server
server.auth.sign_in(tableau_auth)

site_id = server.sites.get_by_id(server.site_id).content_url

request_options = TSC.RequestOptions()
all_projects = list(TSC.Pager(server.projects, request_options))
all_workbooks = list(TSC.Pager(server.workbooks, request_options))
all_views = list(TSC.Pager(server.views, request_options))
all_users = list(TSC.Pager(server.users, request_options))

# #create a new project
# with server.auth.sign_in(tableau_auth):
#     new_proj = TSC.ProjectItem("second_project", "from python script")
#     new_proj = server.projects.create(new_proj)


#get tableau projects ID and Name
id = []
val = []

with server.auth.sign_in(tableau_auth):
    for proj in TSC.Pager(server.projects):
        print(proj.id, proj.name)
        id.append(proj.id)
        val.append(proj.name)

df = pd.DataFrame.from_dict({'Project_ID': id, 'Project_Val': val})


#get tableau workbook details
proj_id = []
proj_name = []
wb_id = []
wb_name = []

with server.auth.sign_in(tableau_auth):
    for workbook in TSC.Pager(server.workbooks):
        proj_id.append( workbook.project_id)
        proj_name.append(workbook.project_name)
        wb_id.append(workbook.id)
        wb_name.append(workbook.name)

wb_proj_df = pd.DataFrame.from_dict({'project_id': proj_id,
                                    'project_name' : proj_name,
                                    'workbook_id' : wb_id,
                                    'workbook_name' : wb_name})

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


###################
server.workbooks.populate_views(workbook_info[0])
print([view.name for view in test_wb.views],
[view.project_id for view in test_wb.views])

#get tableau workbook details with views
proj_id = []
proj_name = []
wb_id = []
wb_name = []
vw_id = []
vw_name = []
owner_id = []
owner_name = []

with server.auth.sign_in(tableau_auth):
    for view in TSC.Pager(server.views):
        print(view.id,
            view.name,
            view.workbook_id,
            view.project_id)


with server.auth.sign_in(tableau_auth):
    for view in TSC.Pager(server.views):
        print(view.id,
            view.name)


with server.auth.sign_in(tableau_auth):
    all_views, pagination_item = server.views.get()
    print([view.name for view in all_views])

with server.auth.sign_in(tableau_auth):
    all_views, pagination_item = server.views.get() 
    view_item = [view for view in all_views]   


for wb in range(len(workbook_info)): 
    server.workbooks.populate_views(workbook_info[wb])
    for view in workbook_info[wb].views:
        server.views.populate_preview_image(view)
        with open('C:/Users/sivkumar/Documents/Project MOM/RR/Tableau/{}.png'.format(view.name), 'wb') as f:
            f.write(view.preview_image)


for wb in range(len(workbook_info)):
    server.workbooks.populate_preview_image(workbook_info[wb])
    with open('C:/Users/sivkumar/Documents/Project MOM/RR/Tableau/{}.png'.format(workbook_info[wb].name),'wb') as f:
        f.write(workbook_info[wb].preview_image)

server.views.populate_image(view_item[0])
server.views.populate_preview_image(view_item[0].image)


with server.auth.sign_in(tableau_auth):
    # Step 2: Query for the view that we want an image of
    req_option = TSC.RequestOptions()
    req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                        TSC.RequestOptions.Operator.Equals, 'Obesity'))
    all_views, pagination_item = server.views.get(req_option)
    if not all_views:
        raise LookupError("View with the specified name was not found.")
    view_item = all_views[0]

    max_age = 5
    if not max_age:
        max_age = 1

    image_req_option = TSC.ImageRequestOptions(imageresolution=TSC.ImageRequestOptions.Resolution.High,
                                                maxage=max_age)
    server.views.populate_image(view_item, image_req_option)

    with open('C:/Users/sivkumar/Documents/Project MOM/RR/Tableau/view_preview_image.png', "wb") as image_file:
        image_file.write(view_item.image)

    print("View image saved to {0}".format('C:/Users/sivkumar/Documents/Project MOM/RR/Tableau/view_preview_image.png'))


"""<script type='text/javascript' src='https://10ax.online.tableau.com/javascripts/api/viz_v1.js'></script>
<div class='tableauPlaceholder' style='width: 1600px; height: 877px;'><object class='tableauViz' width='1600'
        height='877' style='display:none;'>
        <param name='host_url' value='https%3A%2F%2F10ax.online.tableau.com%2F' />
        <param name='embed_code_version' value='3' />
        <param name='site_root' value='&#47;t&#47;vizsivadev749967' />
        <param name='name' value='{}&#47;{}' />
        <param name='tabs' value='no' />
        <param name='toolbar' value='yes' />
        <param name='showAppBanner' value='false' /></object>
</div>""".format(workbook_info [0].name, all_views [0].name)

#view image from a data frame
# df.iloc[0]['vw_image']

# df.iloc[15]['embed_code'].replace('\n', '')


#populating the Images for Workbook and views
#image of a view
server.views.populate_image(all_views[0])
pic = Image.open(io.BytesIO(all_views[0].image))
pic.show()

#thumbnail of a workbook
server.workbooks.populate_preview_image(workbook_info[0])
wb_pic = Image.open(io.BytesIO(workbook_info[0].preview_image))

python .\tableau_TSC_using_args.py -s 'https://10ax.online.tableau.com' -u 'siva.dhanush.007@gmail.com' -si 'vizsivadev749967'


str(datetime.now().day)+'_'+str(datetime.now().month)+'_'+str(datetime.now().year)

os.mkdir()
os.chdir('C:/Users/sivkumar/Documents/Project MOM/RR/Tableau/')
os.path.join

#create the folder for each work book and populate with the work book images

for wb in range(len(all_workbooks)):
    os.mkdir(os.path.join(os.getcwd(),all_workbooks[wb].name))
    server.workbooks.populate_preview_image(all_workbooks[wb])
    with open(os.path.join(os.getcwd(),all_workbooks[wb].name,'{}.png'.format(all_workbooks[wb].name)),'wb') as f:
        f.write(all_workbooks[wb].preview_image)


try:
    os.mkdir(os.path.join(os.environ.get('HOMEDRIVE'),os.environ.get('HOMEPATH'),'Documents','Tableau'))
except Exception as e:
    print(e)
    os.chdir(os.path.join(os.environ.get('HOMEDRIVE'),os.environ.get('HOMEPATH'),'Documents','Tableau'))
    print(os.getcwd())
else:
    os.chdir(os.path.join(os.environ.get('HOMEDRIVE'),os.environ.get('HOMEPATH'),'Documents','Tableau'))
    print(os.getcwd())
finally:
    for wb in range(len(all_workbooks)):
        os.mkdir(os.path.join(os.getcwd(),all_workbooks[wb].name))
        server.workbooks.populate_preview_image(all_workbooks[wb])
        with open(os.path.join(os.getcwd(),all_workbooks[wb].name,'{}.png'.format(all_workbooks[wb].name)),'wb') as f:
            f.write(all_workbooks[wb].preview_image)
            f.close()

os.rmdir()
os.