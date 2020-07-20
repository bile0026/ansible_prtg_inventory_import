# ansible_prtg_inventory_import
import inventory into ansible from PRTG NMS

Uses the PRTG API: https://www.paessler.com/manuals/prtg/application_programming_interface_api_definition

You will need to create a user in PRTG with API permissions and a passhash. https://www.paessler.com/manuals/prtg/http_api

Need to create a .ini file in the same directory as this script with your variables. Using normal username and password does not work. If you try and use hard coded variables you will have a very bad day and be chasing your tail.

.ini format:
```
[prtg]
prtg_server = myserver
prtg_user = myuser
prtg_passhash = mypasshash
prtg_tag = mytag
prtg_domain = domain.com
```

If running in AWX, use a "from project" source type when you create your inventory so you can pull from git or another location that will include your .ini file.

Regex host name cleanup can handle these various formats of hostnames (should be inclusive of most default naming schemes in PRTG):

* HOST_NAME (host-name.example.com)
* host-name.example.com
* (host-name.example.com) host-name
* HOST-NAME.example.COM (HOST-NAME) [Cisco Device]
* (HOST-NAME.example.com) HOST-NAME
* HOST-NAME (HOST-NAME.example.com)
* 10.150.252.40
* HOST-NAME.example.COM (host-name.example.com) [Cisco Device Cisco IOS]

If a name isn't able to be formatted, it will import it as ```bad_name_delete_me```, so it's easy to identify and cleanup.
