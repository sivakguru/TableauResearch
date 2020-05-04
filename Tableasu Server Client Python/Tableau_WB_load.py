#To load the workbook in to the Respective project folders

#import necessary packages

#for Tableau server client API
import tableauserverclient as TSC
#working with file directories
import os
#To read the JSON Properties file
import json
#parse the argument
import argparse
#for time module and sleep
import time

#get the JSON file name

parser = argparse.ArgumentParser(description='Get the JSON file with the required Tableau attributes')
parser.add_argument('--filename', '-fn', required=True, help='file name')
args = parser.parse_args()

print('\nLoading the properties.json file...!')
#loading the parameters from JSON file
with open(args.filename) as data:
    try:
        detail = json.load(data)
    except json.JSONDecodeError as e:
        print(e)
    else:
        server_url = 'https://' + detail['server_name']
        username = detail['username']
        site_id = detail['site_id']
        password = detail['password']
        print('\nPropertises file loaded...!')

#server authentication
server = TSC.Server(server_url)
server.use_server_version()
tableau_auth = TSC.TableauAuth(username, password, site_id=site_id)

#get the directory address and make it as current working directory
cwd = detail['cwd']
#For each workbook, Create Folders for Preview images (.png) format
try:
    os.mkdir(cwd)
except Exception as e:
    print(e)
    os.chdir(cwd)
    print('\nCurrent working directory set to : {}'.format(cwd))
else:
    os.chdir(cwd)
    print('\nCurrent working directory set to : {}'.format(cwd))

print('\nSigning in to the server : {}'.format(server_url))
#server sign-in
server.auth.sign_in(tableau_auth)

print('\nCollecting the existing project info...!')
#collecting the existing project information
request_options = TSC.RequestOptions()
all_projects = list(TSC.Pager(server.projects, request_options))

#Traversing through the CWD to get the project names and workbook file names
file_path = {}
for t in os.listdir(os.getcwd()):
    file_name = []
    if os.path.isdir(t):
        for t1 in os.scandir(t):
            if t1.name.endswith(".twbx"):
                file_path[t] = file_name
                file_name.append([os.path.join(os.getcwd(),t,t1.name),os.path.splitext(t1.name)[0]])

#display the project name and workbook name for confirmation
print('--Projectname--\t--workbookname---')
for k, v in file_path.items():
    print(k)
    for val in range(len(v)):
        for value in range(len(v[val])):
            print('\t','\t',v[val][1])

#confirmation input to load the workbook
n=1
while n < 5:
    try:
        print('\nCan we proceed to load the workbooks ?')
        input_value = input("enter 'Y' for (YES) and 'N' for (NO) :")
        if input_value != 'Y':
            if input_value != 'N':
                raise ValueError
    except ValueError:
        print('\nEnter proper Input..!')
        n += 1
        continue
    else:
        if input_value == 'Y':
            print('\nLets load the workbook..!')
            break
        else:
            #if no then exiting the program clearing all the memory
            print('\nexiting the program..!')
            time.sleep(2)
            os._exit(0)

#traversing throught the project and workbook list
for k, v in file_path.items():
    #creating new project item
    new_project = TSC.ProjectItem(k, description=k)
    try:
        #create new project    
        new_proj_details = server.projects.create(new_project)
    except Exception as e:
        #capturing the error on project name already exists
        print(e)
        #find the project name and delete the project and create new project
        for i in range(len(all_projects)):
            if all_projects[i].name == k:
                server.projects.delete(all_projects[i].id)
                new_proj_details = server.projects.create(new_project)
                print('Created Project {}'.format(new_proj_details.name))
    else:
        #publish the workbooks in the project created
        print('Created Project {}'.format(new_proj_details.name))
        for val in range(len(v)):
            new_workbook = TSC.WorkbookItem(name=v[val][1], project_id=new_proj_details.id, show_tabs=True)
            workbook_publish_mode = TSC.Server.PublishMode.Overwrite
            new_workbook_details = server.workbooks.publish(new_workbook, v[val][0], mode=workbook_publish_mode)
            print("workbook name {} published..!".format(new_workbook_details.name))