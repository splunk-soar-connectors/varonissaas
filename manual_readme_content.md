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