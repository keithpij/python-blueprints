If you get an error like the one below the follow the steps provided.

    azure.servicebus.exceptions.ServiceBusAuthorizationError: Unauthorized access. 'Send' claim(s) are required to perform this operation. Resource: 'sb://blueprints-namespace.servicebus.windows.net/bp-queue'. 

To get the send to queue and read from queue functions to work I had to
    1. Sign into the Azure portal
    2. Navigate to your queue's Service Bus namespace
    3. Go to Access Control (IAM)
    4. Click on View Access to this Resource
    5. Click Add then Click Add Role Assignment
    6. In the Role Drop down select 'Azure Service Bus Data Owner'
    7. In the Assign Access To drop down select 'User, Group, or Service Principal' 
    8. In the Select text box type in the name of the service principal you created.
    9. Click the Save button.