import tableauserverclient as TSC

#set up authentication
server = TSC.Server('https://tableau.internal.deloitte.com/')
server.use_server_version()
#tableau_auth = TSC.TableauAuth('atrapa.deloitte.com\sivkuma', 'Justdoit_07', 'default')

tableau_auth = TSC.PersonalAccessTokenAuth('siva_token', '0fVxl4yPQ9mIW+VQv7QOzw==:ci1v7r9by9Nfz3q2viAqNfCvtQmTkMYZ')


server.auth.sign_in(tableau_auth)

request_options = TSC.RequestOptions()
all_projects = list(TSC.Pager(server.projects, request_options))
all_workbooks = list(TSC.Pager(server.workbooks, request_options))
all_users = list(TSC.Pager(server.users, request_options))
