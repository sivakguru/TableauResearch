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


    request_options = TSC.RequestOptions()
    all_workbooks = list(TSC.Pager(server.workbooks, request_options))
    all_views = list(TSC.Pager(server.views, request_options))
    all_users = list(TSC.Pager(server.users, request_options))

    #load all workbook items by using workbook ID
    workbook_info = []
    for wb in range(len(all_workbooks)):
        workbook_info.append(server.workbooks.get_by_id(all_workbooks[wb].id))

    #loop through Workbook Items and populate the data for Views under each workbook
    #each loop appends the data to the array

    vw_id = []
    vw_name = []
    wb_id = []
    wb_name = []
    proj_id = []
    proj_name = []
    owner_id = []
    owner_name = []
    vw_image = []
    embed_code = []

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
            server.views.populate_preview_image(view)
            vw_image.append(Image.open(io.BytesIO(view.preview_image)))
            embed_code.append("""<script type='text/javascript' src='https://10ax.online.tableau.com/javascripts/api/viz_v1.js'></script>
            <div class='tableauPlaceholder' style='width: 1600px; height: 877px;'><object class='tableauViz' width='1600'
                    height='877' style='display:none;'>
                    <param name='host_url' value='https%3A%2F%2F10ax.online.tableau.com%2F' />
                    <param name='embed_code_version' value='3' />
                    <param name='site_root' value='&#47;t&#47;vizsivadev749967' />
                    <param name='name' value='{}&#47;{}' />
                    <param name='tabs' value='no' />
                    <param name='toolbar' value='yes' />
                    <param name='showAppBanner' value='false' /></object>
            </div>""".format(workbook_info[wb].name.replace(' ', ''), view.name.replace(' ', '')))


    server.auth.sign_out()
    #once the Views image are populated using---server.views.populate_image(view)---
    #all the images are in the Bytes data type
    #use ---io.BytesIO--- to read the Bytes image
    #---Image.open()--- is used to ready the bytes in to PIL item of .png Image format

    #make dictionary from all the arrays
    #load dictionary to data frame using Pandas
    df = pd.DataFrame.from_dict({'proj_id' : proj_id,
                                'proj_name' : proj_name,
                                'wb_id': wb_id,
                                'wb_name' : wb_name,
                                'vw_id' : vw_id,
                                'vw_name' : vw_name,
                                'owner_id' : owner_id,
                                'owner_name' : owner_name,
                                'vw_image' : vw_image,
                                'embed_code' : embed_code})

    df.to_csv(r'C:/Users/sivkumar/Documents/Project MOM/RR/Tableau/test.csv', index = False)


if __name__ == "__main__":
    main()