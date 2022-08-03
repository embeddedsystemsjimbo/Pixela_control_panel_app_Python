# Pixela_control_panel_app_Python
GUI created in Python using the Tkinter and Requests module to interact with Pixela habit tracking API

This is a python GUI created to help users interact with the Pixela API. Pixela is an online service that lets you record and track your habits and daily activities with a Github-like graph. The graph illustrates the intensity of the habit you are tracking with increasingly opaque pixels over a timescale.

See Pixela API's website for more details at https://pixe.la

![image](https://user-images.githubusercontent.com/76194492/182506147-b5c1c3f7-54ba-44fd-b748-8a53b9bca80d.png)

Example of Pixela Graph

***


The "Pixela Control Panel App" is consisted of five different frames. The selection of each frame is determined by a series of radio buttons at the bottom of the window entitled "Options”. Refer to Figures 1 though 5. 

The five label frames users can choose from are called "View Graph", "Create User Frame", "Create New Graph", "Delete Graph”, and "Add pixel to Graph”, which are displayed in the middle of the app window. 

There is an additional label frame called "Update Status”, which overlaps applicable frames when API transactions are successful. 

The "View Graph" frame, as seen in Figure 1, lets the user inspect their past and current Pixela graph by opening a URL link directly to their pixel graph hosted on Pixila's website (Refer to Figure 6). 

The "Create User" label frame allows the user to register a new user name with Pixela, and saves user data locally. Refer to Figure 2 for this label frame.

The "Create New Graph" label frame lets the user register a new graph online with Pixela, and saves graph data locally. The user is required to select a user name for the new graph, to assign a unit measurement to track the habit, to choose between a float or integer type for the unit type, and to select a graph name and a graph ID. Refer to Figure 4 for this label frame.

The "Delete Graph" frame allows users to delete data both locally and online with Pixela delete graphs. Refer to Figure 4 for this label frame. 

The "Add a Pixel to Graph" label frame lets the user register a value to track with a registered Pixela graph. Each value has a time stamp corresponding to the current day, where one new graph value entry can be made per day. Refer to Figure 5 for this label frame.

For more details on the Pixela API, visit their website at https://pixe.la



***

<img width="779" alt="image" src="https://user-images.githubusercontent.com/76194492/182499315-d1b78f6d-8377-43d4-933a-94f3f8a5bf34.png">

Figure 1: View Graph Frame.

***

<img width="779" alt="image" src="https://user-images.githubusercontent.com/76194492/182499358-1a3657fc-d2ee-471a-a18b-42a7d4d567c0.png">

Figure 2: Create User Frame.

***

<img width="779" alt="image" src="https://user-images.githubusercontent.com/76194492/182499398-e4b81235-a620-492c-8c6c-23484f3ad00e.png">

Figure 3: Create New Graph Frame.

***

<img width="779" alt="image" src="https://user-images.githubusercontent.com/76194492/182499429-71b5be6f-2cc0-4313-85b0-989611115967.png">

Figure 4: Delete Graph Frame.

***

<img width="840" alt="image" src="https://user-images.githubusercontent.com/76194492/182499466-00e25619-7b86-4696-a3ed-916d1fa97044.png">

Figure 5: Add Pixel to Graph Frame.

***

<img width="923" alt="image" src="https://user-images.githubusercontent.com/76194492/182505453-44703a75-4436-4d37-92c6-92e31e7e05c8.png">

Figure 6: Pixela Graph example. 
