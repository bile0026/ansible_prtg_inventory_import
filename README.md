# ansible_prtg_inventory_import
import inventory into ansible from PRTG NMS

NOT WORKING YET

Uses the PRTG API: https://www.paessler.com/manuals/prtg/application_programming_interface_api_definition

Need to create a .ini file in the same directory with your variables. You will need to create a user in PRTG with API permissions and a passhash. Using normal username and password does not work.
```
[prtg]
prtg_server = myserver
prtg_user = myser
prtg_passhash = mypasshash
prtg_tag = mytag
```

If running in AWX, you can paste in the script file and update the connection vars in the beginning of the file so you don't have to include the .ini file.