#Tableau Server Info RR

#install Tableau server client for python
    #pip install tableauserverclient

import tableauserverclient as TSC
import pandas as pd

#set up authentication RR Deveoper account
server = TSC.Server('https://10ax.online.tableau.com')
server.use_server_version()
tableau_auth = TSC.TableauAuth('thulasiramvanniya@gmail.com', 'Sairam@2903', 'thulasiramdev938591')

server.auth.sign_in(tableau_auth)

request_options = TSC.RequestOptions()
all_workbooks = list(TSC.Pager(server.workbooks, request_options))
# TSC.Pager(server.views, request_options)
all_views = list(TSC.Pager(server.views, request_options))

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


server.views.populate_preview_image(view_item)
with open('C:/Users/sivkumar/Documents/Project MOM/RR/Tableau/view_preview_image.png') as f:
	f.write(view_item.preview_image)

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