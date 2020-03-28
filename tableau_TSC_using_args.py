#Tableau Server Info RR

#Tableau server accesstoken : iMUgahYuSiqXXisFrBPr+A==:biVQjxSOJW6LbiCkQG5djkwDqEAoLOAY

#install Tableau server client for python
    #pip install tableauserverclient

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

def main():
    parser = argparse.ArgumentParser(description='Get all the Tableau Site details, to populate the React.js framework')
    parser.add_argument('--server', '-s', required=True, help='Server Address')
    parser.add_argument('--username', '-u', required=True, help='User name')
    parser.add_argument('--site', '-si', required=True, help='Site ID')

    args = parser.parse_args()
    password = getpass.getpass("Password :")

    #server authentication
    server = TSC.Server(args.server)
    server.use_server_version()
    tableau_auth = TSC.TableauAuth(args.username, password, site_id=args.site)

    #server sign-in
    server.auth.sign_in(tableau_auth)

    #get all the pro, workbook, views and user Items from the site
    request_options = TSC.RequestOptions()
    all_projects = list(TSC.Pager(server.projects, request_options))
    all_workbooks = list(TSC.Pager(server.workbooks, request_options))
    all_views = list(TSC.Pager(server.views, request_options))
    all_users = list(TSC.Pager(server.users, request_options))
    #site name
    site_id = server.sites.get_by_id(server.site_id).content_url
    print('Collecting Details for Site : {}'.format(site_id))

    #make the Current working directory as C:\Users\<user name\Document\Tableau
    cwd = os.path.join(os.environ.get('HOMEDRIVE'),os.environ.get('HOMEPATH'),'Documents','Tableau')
    #For each workbook, Create Folders for Preview images (.png) format
    try:
        os.mkdir(cwd)
    except Exception as e:
        print(e)
        os.chdir(cwd)
        print('\nCurrent working directory changed to : {}'.format(cwd))
        print('\nAll the files and images will be stored in this location...!')
    else:
        os.chdir(cwd)
        print('\nCurrent working directory changed to : {}'.format(cwd))
        print('\nAll the files and images will be stored in this location...!')
    finally:
        print('''\nSaving all the workbook & related views thumbnail's in respective folders...!''')
        for wb in range(len(all_workbooks)):
            #projectname_workbookname
            proj_wb_name = all_workbooks[wb].project_name+'_'+all_workbooks[wb].name
            #views folder - thumbnail (.png) image of each workbook views
            wb_view = all_workbooks[wb].name+'_views'
            #create folder if the folder does not exist
            if not os.path.exists(os.path.join(cwd, proj_wb_name)):
                os.mkdir(os.path.join(cwd, proj_wb_name))
            if not os.path.exists(os.path.join(cwd, proj_wb_name, wb_view)):
                os.mkdir(os.path.join(cwd, proj_wb_name, wb_view))
            server.workbooks.populate_preview_image(all_workbooks[wb])
            server.workbooks.populate_views(all_workbooks[wb])
            with open(os.path.join(cwd,proj_wb_name,'{}.png'.format(all_workbooks[wb].name)),'wb') as f_wb:
                f_wb.write(all_workbooks[wb].preview_image)
                f_wb.close()
            for view in all_workbooks[wb].views:
                server.views.populate_preview_image(view)
                with open(os.path.join(cwd, proj_wb_name, wb_view,'{}.png'.format(view.name)), 'wb') as f_view:
                    f_view.write(view.preview_image)
                    f_view.close()

    #loop through Workbook Items and populate the data for Views under each workbook
    #each loop appends the data to the array
    print('\nCollecting all the UI related data to a Data Frame')
    vw_id = []
    vw_name = []
    wb_id = []
    wb_name = []
    wb_tags = []
    wb_create_dt = []
    wb_update_dt = []
    show_tabs = []
    proj_id = []
    proj_name = []
    is_default = []
    proj_desc = []
    owner_id = []
    owner_name = []
    vw_image = []
    embed_code = []

    for wb in range(len(all_workbooks)): 
        server.workbooks.populate_views(all_workbooks[wb])
        for view in all_workbooks[wb].views:
            wb_id.append(all_workbooks[wb].id)
            wb_name.append(all_workbooks[wb].name)
            wb_tags.append(all_workbooks[wb].tags)
            wb_create_dt.append(all_workbooks[wb].created_at)
            wb_update_dt.append(all_workbooks[wb].updated_at)
            show_tabs.append(all_workbooks[wb].show_tabs)
            proj_id.append(all_workbooks[wb].project_id)
            proj_name.append(all_workbooks[wb].project_name)
            for proj in range(len(all_projects)):
                if all_workbooks[wb].project_id == all_projects[proj].id:
                    is_default.append(all_projects[proj].is_default())
                    proj_desc.append(all_projects[proj].description)
            owner_id.append(all_workbooks[wb].owner_id)
            for usr in range(len(all_users)):
                if all_workbooks[wb].owner_id == all_users[usr].id:
                    owner_name.append(all_users[usr].name)
            vw_id.append(view.id)
            vw_name.append(view.name)
            server.views.populate_preview_image(view)
            vw_image.append(Image.open(io.BytesIO(view.preview_image)))
            embed_code.append("""<script type='text/javascript' src='https://10ax.online.tableau.com/javascripts/api/viz_v1.js'></script>
            <div class='tableauPlaceholder' style='width: 1600px; height: 877px;'><object class='tableauViz' width='1600'
                    height='877' style='display:none;'>
                    <param name='host_url' value='https%3A%2F%2F10ax.online.tableau.com%2F' />
                    <param name='embed_code_version' value='3' />
                    <param name='site_root' value='&#47;t&#47;{}' />
                    <param name='name' value='{}&#47;{}' />
                    <param name='tabs' value='no' />
                    <param name='toolbar' value='yes' />
                    <param name='showAppBanner' value='false' /></object>
            </div>""".format(site_id, all_workbooks[wb].name.replace(' ', ''), view.name.replace(' ', '')))


    server.auth.sign_out()
    #once the Views image are populated using---server.views.populate_image(view)---
    #all the images are in the Bytes data type
    #use ---io.BytesIO--- to read the Bytes image
    #---Image.open()--- is used to ready the bytes in to PIL item of .png Image format

    #make dictionary from all the arrays
    #load dictionary to data frame using Pandas
    df = pd.DataFrame.from_dict({'proj_id' : proj_id,
                                'proj_name' : proj_name,
                                'is_default' : is_default,
                                'proj_desc' : proj_desc,
                                'wb_id': wb_id,
                                'wb_name' : wb_name,
                                'wb_tags' : wb_tags,
                                'wb_create_dt' : wb_create_dt,
                                'wb_update_dt' : wb_update_dt,
                                'show_tabs' : show_tabs,
                                'vw_id' : vw_id,
                                'vw_name' : vw_name,
                                'owner_id' : owner_id,
                                'owner_name' : owner_name,
                                'vw_image' : vw_image,
                                'embed_code' : embed_code})

    #file location inside the Current working directory with file name as 'site_<site_id>.csv'
    file_location = os.path.join(cwd,'site_{}.csv'.format(site_id))
    print('\nSaving data to csv in the location : {}'.format(file_location))
    df.to_csv(r'{}'.format(file_location), index = False)

if __name__ == "__main__":
    main()