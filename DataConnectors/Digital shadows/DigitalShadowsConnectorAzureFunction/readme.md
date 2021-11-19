# Digital Shadows Integration for Azure Sentinel

## Introduction

This folder contains the Azure function time trigger code for Digital Shadows-Azure Sentinel connector. The connector will run periodically and ingest the Digital Shadows incidents and alerts data into the Azure Sentinel logs. After the data has been ingested, Analytic rule will promote the data and create the Azure Sentinel incidents out of them. Analytic rule will also trigger playbooks, `status-and-severity-update` and `add-comments`. The playbooks will change the status and severity and add comments to Azure Sentinel incidents according to the latest Digital Shadows data logged. The data can be visualized in the Workbook labelled `Digital Shadows workbook`.

## Folders

1. `Digital shadows/` - This contains The package, requirements, ARM JSON file, connector page template JSON, and other dependencies. 
2. `DigitalShadowsConnectorAzureFunction/` - This contains the Azure function source code along with sample data.


## Installing for the users

After the solution is published, we can find the connector in the connector gallery of Azure Sentinel among other connectors in Data connectors section of Sentinel. 

i. Go to Azure Sentinel -> Data Connectors

ii. Click on the Digital Shadows connector, connector page will open. 

iii. Click on the blue `Deploy to Azure` button.   


![Screenshot from 2021-11-19 12-46-30](https://user-images.githubusercontent.com/88835344/142581388-f4a97e6d-7ce1-4f75-8a9e-7c2164fc38a3.png)


It will lead to a custom deployment page where after entering accurate credentials and other information, the resources will get created. 


![Screenshot from 2021-11-19 12-47-43](https://user-images.githubusercontent.com/88835344/142581668-5d5dd767-55a2-49fc-a9c9-eb458f75a2a7.png)


The connector should start ingesting the data into the logs in next 5-10 minutes.


## Installing for testing


i. Log in to Azure portal using the URL - [https://portal.azure.com/?feature.BringYourOwnConnector=true](https://portal.azure.com/?feature.BringYourOwnConnector=true).

ii. Go to Azure Sentinel -> Data Connectors

iii. Click the “import” button at the top and select the json file `DigitalShadowsSearchlight_API_functionApp.JSON` downloaded on your local machine from Github.

iv. This will load the connector page and rest of the process will be same as the Installing for users guideline above.


Each invocation and its logs of the function can be seen in Function App service of Azure, available in the Azure Portal outside the Azure Sentinel.

i. Go to Function App and click on the function which you have deployed, identified with the given name at the deployement stage.

ii. Go to Functions -> DigitalShadowsConnectorAzureFunction -> Monitor

iii. By clicking on invocation time, you can see all the logs for that run. 

**Note: Furthermore we can check logs in Application Insights of the given function in detail if needed. We can search the logs by operation ID in Transaction search section.**
