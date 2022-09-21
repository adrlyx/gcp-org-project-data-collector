



# gcp-org-project-data-collector

## What is this?
A python program that uses googleapiclient discovery module to fetch project data & metrics from Google Cloud Platform. 
<br />

## Motivation?

When migrating to Google Cloud Platform there were already a bunch of projects created in the console(400+) that was not created with the recomendations and structure that my team had set up. When I asked around if we could delete some projects many people said they were using the projects with Google Workspace and so forth.
I created this python program to go through all the projects within the organization and extract data that could prove if the project was in use or not. If there were no billing active and there were no request count metrics to Googles APIs the projects was considered to be not in use.

- Recursively finds all projects in Google Cloud Platform in an organization and under all folders.
- Extract data to determine if the project is in use or not
<br />

## Prerequisites 

1. Authenticate to gcloud:

```
gcloud auth application-default login
```

2. Create an *.env* file in the top directory and set the organization ID:

```
[ENV]
# Format: <organizations/org-id>
ORG_ID=
```

### Result

Data table will be written to file output.txt (included in gitignore so you won´t upload any sensitive data).

Example output:
```
+-----------------+-----------------------+----------------------+-------------------------+----------------------+--------------------------+---------------------------+-----------------+-------------------------+---------------------------+
|   Folder Name   |       Folder ID       |     DisplayName      |      ProjectName        |      ProjectId       |        User/Owner        |           Labels          |  BillingEnabled | 2Weeks API RequestCount |   1M Log Bytes Ingested   |
+-----------------+-----------------------+----------------------+-------------------------+----------------------+--------------------------+---------------------------+-----------------+-------------------------+---------------------------+
|       IT        |  folders/678967896789 |    Admin IT Google   |  projects/123412341234  |   admin-it-google    |  user:test1@example.com  |    {'department': 'IT'}   |       True      |           5431          |          5804KiB          |
|       N/A       |  folders/108212341234 |   GAM Project ASDF   |  projects/234523452345  |   gam-project-asdf   |  user:test2@example.com  |    {'department': 'IT'}   |       False     |           116           |          7419KiB          |   
+-----------------+-----------------------+----------------------+-------------------------+----------------------+--------------------------+---------------------------+-----------------+-------------------------+---------------------------+
```

*Folder Name: N/A means the project is located on the top level in the GCP organization*