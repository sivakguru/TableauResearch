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
import sqlalchemy as db
from sqlalchemy.engine.reflection import Inspector

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
            server.workbooks.download(all_workbooks[wb].id, filepath=os.path.join(cwd, proj_wb_name), no_extract=False)
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
    view_id = []
    view_name = []
    workbook_id = []
    workbook_name = []
    tags = []
    doc_created_dt = []
    doc_modified_dt = []
    show_tabs = []
    project_id = []
    project_name = []
    is_default = []
    description = []
    owner_id = []
    owner_name = []
    view_image = []
    embed_code = []

    for wb in range(len(all_workbooks)): 
        server.workbooks.populate_views(all_workbooks[wb])
        for view in all_workbooks[wb].views:
            workbook_id.append(all_workbooks[wb].id)
            workbook_name.append(all_workbooks[wb].name)
            tags.append(all_workbooks[wb].tags)
            doc_created_dt.append(all_workbooks[wb].created_at)
            doc_modified_dt.append(all_workbooks[wb].updated_at)
            show_tabs.append(all_workbooks[wb].show_tabs)
            project_id.append(all_workbooks[wb].project_id)
            project_name.append(all_workbooks[wb].project_name)
            for proj in range(len(all_projects)):
                if all_workbooks[wb].project_id == all_projects[proj].id:
                    is_default.append(all_projects[proj].is_default())
                    description.append(all_projects[proj].description)
            owner_id.append(all_workbooks[wb].owner_id)
            for usr in range(len(all_users)):
                if all_workbooks[wb].owner_id == all_users[usr].id:
                    owner_name.append(all_users[usr].name)
            view_id.append(view.id)
            view_name.append(view.name)
            server.views.populate_preview_image(view)
            view_image.append(Image.open(io.BytesIO(view.preview_image)))
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
    df = pd.DataFrame.from_dict({'project_id' : project_id,
                                'project_name' : project_name,
                                'is_default' : is_default,
                                'description' : description,
                                'workbook_id': workbook_id,
                                'workbook_name' : workbook_name,
                                'tags' : tags,
                                'doc_created_dt' : doc_created_dt,
                                'doc_modified_dt' : doc_modified_dt,
                                'show_tabs' : show_tabs,
                                'view_id' : view_id,
                                'view_name' : view_name,
                                'owner_id' : owner_id,
                                'owner_name' : owner_name,
                                'view_image' : view_image,
                                'embed_code' : embed_code})

    #file location inside the Current working directory with file name as 'site_<site_id>.csv'
    file_location = os.path.join(cwd,'site_{}.csv'.format(site_id))
    print('\nSaving data to csv in the location : {}'.format(file_location))
    df.to_csv(r'{}'.format(file_location), index = True)

    # db_conn = "postgres://postgres:Sivkumar_123@localhost:5432/postgres"

    # engine = db.create_engine(db_conn)

    # conn = engine.connect()

    # metadata = db.MetaData(schema='prestage')

    # engine.execute("""CREATE table if not EXISTS prestage.tableau_app_info (
    #     rowid numeric(10) NULL,
    #     doc_type text NULL,
    #     id text NULL,
    #     "name" text NULL,
    #     "version" text NULL,
    #     project_id text NULL,
    #     project_name text NULL,
    #     description text NULL,
    #     is_default bool NULL,
    #     workbook_id text NULL,
    #     workbook_name text NULL,
    #     tags text NULL,
    #     doc_created_dt text NULL,
    #     doc_modified_dt text NULL,
    #     workbook_show_tabs text NULL,
    #     view_id text NULL,
    #     view_name text NULL,
    #     view_count text NULL,
    #     content_url text NULL,
    #     owner_id text NULL,
    #     owner_name text NULL,
    #     png_image bytea NULL,
    #     embeded_code text NULL
    # );""")


    # tableau_table = db.Table('tableau_app_info', metadata)

    # insp = Inspector.from_engine(engine)

    # insp.reflecttable(tableau_table, None)

    # for x in range(len(df['rowid'])):
    #     query = db.insert(tableau_table).values(
    #     rowid = int(df['rowid'][x]),
    #     doc_type = df['doc_type'][x],
    #     id = df['id'][x],
    #     name = df['name'][x],
    #     version = df['version'][x],
    #     project_id = df['project_id'][x],
    #     project_name = df['project_name'][x],
    #     description = df['description'][x],
    #     is_default = df['is_default'][x],
    #     workbook_id = df['workbook_id'][x],
    #     workbook_name = df['workbook_name'][x],
    #     tags = df['tags'][x],
    #     doc_created_dt = str(df['doc_created_dt'][x]),
    #     doc_modified_dt = str(df['doc_modified_dt'][x]),
    #     workbook_show_tabs = df['workbook_show_tabs'][x],
    #     view_id = df['view_id'][x],
    #     view_name = df['view_name'][x],
    #     view_count = df['view_count'][x],
    #     content_url = df['content_url'][x],
    #     owner_id = df['owner_id'][x],
    #     owner_name = df['owner_name'][x],
    #     png_image = df['png_image'][x],
    #     embeded_code = df['embeded_code'][x]
    #     )
    #     conn.execute(query)

if __name__ == "__main__":
    main()