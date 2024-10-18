[comment]: # "Auto-generated SOAR connector documentation"
# Varonis SaaS for SOAR

Publisher: Varonis  
Connector Version: 1.0.1  
Product Vendor: Varonis  
Product Name: Varonis SaaS  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 6.2.1  

Varonis SaaS for Splunk SOAR

[comment]: # "File: README.md"
[comment]: # "Copyright (c) Varonis, 2024"
[comment]: # ""
[comment]: # "This unpublished material is proprietary to Varonis SaaS. All"
[comment]: # "rights reserved. The methods and techniques described herein are"
[comment]: # "considered trade secrets and/or confidential. Reproduction or"
[comment]: # "distribution, in whole or in part, is forbidden except by express"
[comment]: # "written permission of Varonis SaaS."
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""

Provide the following configuration settings for the integration setup to establish a successful connection:

*   **Varonis FQDN** - Enter the Varonis Web Interface address. This is the Fully Qualified Domain Name (FQDN) or IP address of the Varonis server to which you want to connect.
*   **Varonis Api Key** - [API key generation](https://help.varonis.com/s/document-item?bundleId=ami1661784208197&topicId=emp1703144742927.html&_LANG=enus).
*   **Alert Retrieval Start Point** - Enter the past number of days from which to start retrieving alerts. Up to 30 days and 1,000 alerts are supported.
*   **Threat Detection Policies** - To retrieve alerts related to specific threat detection policies, enter the relevant policy names. **Recomended: Leave this blank to retrive all Alerts (default)**.
*   **Alert Status** - Specify the Varonis alert status.
*   **Alert Severity** - Specify the alert severity.

For additional information, please check: [Our General documentation](https://help.varonis.com/s/documents?page=1).  
Have a general inquiry or want to contact Varonis? [Contact us](https://www.varonis.com/resources/support).

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Varonis SaaS asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**base_url** |  required  | string | Varonis FQDN/IP the integration should connect to
**api_key** |  required  | password | Varonis API Key
**verify_server_cert** |  optional  | boolean | Whether to verify the server certificate
**ingest_artifacts** |  required  | boolean | Should artifacts be ingested
**ingest_period** |  required  | string | Alert Retrieval Start (Days Ago)
**severity** |  optional  | string | Alert Severity
**threat_model** |  optional  | string | Threat Detection Policies
**alert_status** |  optional  | string | Alert Status

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[get alerts](#action-get-alerts) - Get alerts from Varonis SaaS  
[update alert status](#action-update-alert-status) - Update Varonis alert status command  
[close alert](#action-close-alert) - Close Varonis alert command  
[get alerted events](#action-get-alerted-events) - Get alerted events from Varonis SaaS  
[on poll](#action-on-poll) - Callback action for the on_poll ingest functionality  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'get alerts'
Get alerts from Varonis SaaS

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**threat_model_name** |  optional  | List of requested threat models to retrieve | string | 
**page** |  optional  | Page number (default 1) | numeric | 
**max_results** |  optional  | The max number of alerts to retrieve (up to 50) | numeric | 
**start_time** |  optional  | Start time of the range of alerts | string | 
**end_time** |  optional  | End time of the range of alerts | string | 
**alert_status** |  optional  | List of required alerts status | string | 
**alert_severity** |  optional  | List of alerts severity | string | 
**device_name** |  optional  | List of device names | string | 
**user_name** |  optional  | List of user names | string |  `user name` 
**last_days** |  optional  | Number of days you want the search to go back to | numeric | 
**descending_order** |  optional  | Indicates whether alerts should be ordered in newest to oldest order | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.ID | string |  `varonis alert id`  |  
action_result.data.\*.Name | string |  |  
action_result.data.\*.Time | string |  |   2022-11-11T19:35:00 
action_result.data.\*.Severity | string |  |   High 
action_result.data.\*.Category | string |  |  
action_result.data.\*.Country | string |  |  
action_result.data.\*.State | string |  |  
action_result.data.\*.Status | string |  |   Open 
action_result.data.\*.CloseReason | string |  |  
action_result.data.\*.BlacklistLocation | boolean |  |  
action_result.data.\*.AbnormalLocation | string |  |  
action_result.data.\*.NumOfAlertedEvents | numeric |  |  
action_result.data.\*.UserName | string |  `user name`  |  
action_result.data.\*.EventUTC | string |  |  
action_result.data.\*.SamAccountName | string |  |  
action_result.data.\*.PrivilegedAccountType | string |  |  
action_result.data.\*.EventUTC | string |  |   2022-11-11T19:35:00 
action_result.data.\*.DeviceName | string |  |  
action_result.data.\*.ContainMaliciousExternalIP | string |  |  
action_result.data.\*.IPThreatTypes | string |  |  
action_result.data.\*.AssetContainsFlaggedData | string |  |  
action_result.data.\*.AssetContainsSensitiveData | string |  |  
action_result.data.\*.Platform | string |  |   DNS 
action_result.data.\*.Asset | string |  |   DNS 
action_result.data.\*.FileServerOrDomain | string |  |   DNS 
action_result.status | string |  |   success  failed 
action_result.parameter.alert_severity | string |  |  
action_result.parameter.alert_status | string |  |  
action_result.parameter.descending_order | boolean |  |  
action_result.parameter.device_name | string |  |  
action_result.parameter.end_time | string |  |  
action_result.parameter.last_days | numeric |  |  
action_result.parameter.max_results | numeric |  |  
action_result.parameter.page | numeric |  |  
action_result.parameter.start_time | string |  |  
action_result.parameter.threat_model_name | string |  |  
action_result.parameter.user_name | string |  `user name`  |  
action_result.summary | string |  |  
action_result.message | string |  |  
summary.total_objects | numeric |  |  
summary.total_objects_successful | numeric |  |    

## action: 'update alert status'
Update Varonis alert status command

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**status** |  required  | Alert's new status | string | 
**alert_id** |  required  | Array of alert IDs to be updated | string |  `varonis alert id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.alert_id | string |  `varonis alert id`  |  
action_result.parameter.status | string |  |  
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |  
summary.total_objects | numeric |  |  
summary.total_objects_successful | numeric |  |    

## action: 'close alert'
Close Varonis alert command

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**close_reason** |  required  | Alert's close reason | string | 
**alert_id** |  required  | Array of alert IDs to be closed | string |  `varonis alert id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.alert_id | string |  `varonis alert id`  |  
action_result.parameter.close_reason | string |  |  
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |  
summary.total_objects | numeric |  |  
summary.total_objects_successful | numeric |  |    

## action: 'get alerted events'
Get alerted events from Varonis SaaS

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**alert_id** |  required  | List of alert IDs | string |  `varonis alert id` 
**page** |  optional  | Page number (default 1) | numeric | 
**max_results** |  optional  | The max number of events to retrieve (up to 5k) | numeric | 
**descending_order** |  optional  | Indicates whether events should be ordered in newest to oldest order | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.alert_id | string |  `varonis alert id`  |  
action_result.parameter.descending_order | boolean |  |  
action_result.parameter.max_results | numeric |  |  
action_result.parameter.page | numeric |  |  
action_result.data.\*.IsDisabledAccount | boolean |  |  
action_result.data.\*.ByUserAccountDomain | string |  `domain`  |  
action_result.data.\*.IsLockoutAccount | boolean |  |  
action_result.data.\*.ByUserAccount | string |  `user name`  |  
action_result.data.\*.BySamAccountName | string |  |  
action_result.data.\*.IsStaleAccount | boolean |  |  
action_result.data.\*.ByUserAccountType | string |  |  
action_result.data.\*.AlertId | string |  |  
action_result.data.\*.Country | string |  |  
action_result.data.\*.Description | string |  |  
action_result.data.\*.BlacklistedLocation | boolean |  |  
action_result.data.\*.EventOperation | string |  |  
action_result.data.\*.ExternalIP | string |  `ip`  |  
action_result.data.\*.ID | string |  |  
action_result.data.\*.ExternalIPReputation | string |  |  
action_result.data.\*.ExternalIPThreatTypes | string |  |  
action_result.data.\*.IsMaliciousIP | boolean |  |  
action_result.data.\*.DestinationDevice | string |  |  
action_result.data.\*.DestinationIP | string |  `ip`  |  
action_result.data.\*.Filer | string |  |  
action_result.data.\*.OnAccountIsDisabled | boolean |  |  
action_result.data.\*.OnAccountIsLockout | boolean |  |  
action_result.data.\*.IsSensitive | boolean |  |  
action_result.data.\*.OnObjectName | string |  |  
action_result.data.\*.OnObjectType | string |  |  
action_result.data.\*.Path | string |  |  
action_result.data.\*.Platform | string |  |  
action_result.data.\*.OnSamAccountName | string |  |  
action_result.data.\*.SourceDevice | string |  |  
action_result.data.\*.SourceIP | string |  `ip`  |  
action_result.data.\*.State | string |  |  
action_result.data.\*.Status | string |  |  
action_result.data.\*.Type | string |  |  
action_result.data.\*.TimeUTC | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |  
summary.total_objects | numeric |  |  
summary.total_objects_successful | numeric |  |    

## action: 'on poll'
Callback action for the on_poll ingest functionality

Type: **ingest**  
Read only: **True**

The default start_time is the past 5 days. The default end_time is now.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**container_id** |  optional  | Parameter ignored for this app | string | 
**start_time** |  optional  | Parameter ignored for this app | numeric | 
**end_time** |  optional  | Parameter ignored for this app | numeric | 
**container_count** |  optional  | Maximum number of containers to create | numeric | 
**artifact_count** |  optional  | Maximum number of artifacts to create per container | numeric | 

#### Action Output
No Output