# Weight Cell GUI

This an interface for a weight cell with serial output. The application connects to the serial 
port and display the weight infromation. The user can enter additional information related to 
the weight (Truck details, driver details ) and save that recording. The system allows to take
two readings for the same vehical and print a receipt with the details. The receipt formats can
be changed in the Settings and there are 6 pre-configured formats to select. The information is
saved to a database and can be viewed later as required in the Report page. The receipts can be
reprinted using Print page. The receipt infromation like the company name and contact details 
can be changed in Settings page. The system provides two user types. A previlaged admin user 
who can use the Setting page funcationalities and an operator user who does not have the Setting
page functionality. 

The system was tested and run in Raspberry Pi 4 hardware. 

<video src="tharadi-demo.mp4" width="320" height="240" controls></video>

## Dependancies

- This require a Python environment with Kivy installed. 
- To save the data, mysql database is required. The table structure can be created 
by using scalar_system.sql file. Use below command to create the database for the
application. The application only accept a local database. 

` sudo mysql -u root -p < scalar_system.sql `

- For connecting to the database, install the mysql package for the Python environment. 

- Application uses libreoffice to print the tickets. Make sure the libreoffice is running
in background or use the startup script main.sh 

- The application required a working directory which can be set by using SCALAR_WD. 

## create a standalone executable

Use below commands to create a standalone executable using pyinstaller. 

` pip install -I pyinstaller`

` python compile.py build_ext --inplace`

` pyinstaller main.spec -y --onefile`
