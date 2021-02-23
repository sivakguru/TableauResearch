import tableauserverclient as TSC

#set up authentication
server = TSC.Server('https://10ax.online.tableau.com')
server.use_server_version()
tableau_auth = TSC.TableauAuth('siva.dhanush.007@gmail.com', 'Developer_123', 'vizsivadev749967')

server.auth.sign_in(tableau_auth)

request_options = TSC.RequestOptions()
all_projects = list(TSC.Pager(server.projects, request_options))
all_workbooks = list(TSC.Pager(server.workbooks, request_options))
all_users = list(TSC.Pager(server.users, request_options))
