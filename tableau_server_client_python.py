#install Tableau server client for python

#pip install tableauserverclient

import tableauserverclient as TSC

#set up authentication
server = TSC.Server('https://10ax.online.tableau.com')
server.use_server_version()
tableau_auth = TSC.TableauAuth('siva.dhanush.007@gmail.com', 'sridevis007', 'vizsivadev749967')

#test environment link
server = TSC.Server('http://10.159.131.6:8000/')
server.use_server_version()
tableau_auth = TSC.TableauAuth('admin', 'Deloitte@1234', 'vnpt_b6')

#create a new project
# with server.auth.sign_in(tableau_auth):
#     new_proj = TSC.ProjectItem("second_project", "from python script")
#     new_proj = server.projects.create(new_proj)

#publish the workbook
with server.auth.sign_in(tableau_auth):
    new_workbook = TSC.WorkbookItem(name='telstra', project_id='6aaaffea-5f78-4184-915e-fa626a7487ad')
    work_book_publish_mode = TSC.Server.PublishMode.Overwrite
    new_workbook_msg = server.workbooks.publish(new_workbook, "C:/Users/sivkumar/Documents/Project MOM/Telstra/telstra.twbx", work_book_publish_mode)
    print("Telstra Workbook Published with WB ID : {}".format(new_workbook_msg.id))

#get tableau projects ID and Name
with server.auth.sign_in(tableau_auth):
    for proj in TSC.Pager(server.projects):
        print(proj.id, proj.name)

#find the schedulers available
with server.auth.sign_in(tableau_auth):
    for sche in TSC.Pager(server.schedules):
        print(sche.name)

#find the Data sources available
with server.auth.sign_in(tableau_auth):
    for data_source in TSC.Pager(server.datasources):
        print(data_source.name)

#get server info
s_info = server.server_info.get()
print(s_info.product_version)
print(s_info.rest_api_version)
print(s_info._build_number)



