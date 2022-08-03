# Pixela_control_panel_app_Python
GUI created in Python using the Tkinter and Requests module to interact with Pixela habit tracking API

This is a python GUI I created to help interacted with the Pixela API. Pixela is an online service that lets you record and track your habits with a Github like graph that illustrates the intensity of the habit you are tracking with increasingly opaque pixels over a timescale. 

See Pixela API's website for more details at https://pixe.la

The "Pixela Control Panel App" consists of five different frames where the selection of each frame is determined by a series of radio buttons at the bottom of the window in the "Options" titled label frame as can be seen in Figure 1 though Figure 5. The five user selected label frames titled "View Graph", "Create User Frame", "Create New Graph", "Delete Graph" and "Add pixel to Graph" are display in the middle of the window. Furthermore the "Update Status" label frame overlaps applicable frames indicating if the transaction was success or an error has occurred. Referencing Figure 2, the "Create User" label frame lets the user registering a new username online with Pixela in addition to saving user data locally. Referencing Figure 3, the "Create New Graph" label frame lets the user register a new graph online with Pixela in addition to saving graph data locally. The user is required to select a username to associate the new graph, a unit on which to track the habit, whether the unit is a float or integer type, a graph name, and a graph ID. Referencing Figure 5, the "Add a Pixel to Graph" label frame lets the user register a value to track with a registered Pixela graph. Each value has a time stamp corresponding to the current day where one new graph value entry can be made per day. Refferencing Figure 1, the "View Graph" frame lets the user inspect their past and current Pixela graph by opening a URL link directly to their pixel graph hosted on Pixila's website. Referencing Figure 4, the "Delete Graph" frame allows users to both locally and online with Pixela delete graphs.

***

<img width="779" alt="image" src="https://user-images.githubusercontent.com/76194492/182499315-d1b78f6d-8377-43d4-933a-94f3f8a5bf34.png">
Figure 1: View Graph Frame.

<img width="779" alt="image" src="https://user-images.githubusercontent.com/76194492/182499358-1a3657fc-d2ee-471a-a18b-42a7d4d567c0.png">
Figure 2: Create User Frame.

<img width="779" alt="image" src="https://user-images.githubusercontent.com/76194492/182499398-e4b81235-a620-492c-8c6c-23484f3ad00e.png">
Figure 3: Create New Graph Frame.

<img width="779" alt="image" src="https://user-images.githubusercontent.com/76194492/182499429-71b5be6f-2cc0-4313-85b0-989611115967.png">
Figure 4: Delete Graph Frame.

<img width="840" alt="image" src="https://user-images.githubusercontent.com/76194492/182499466-00e25619-7b86-4696-a3ed-916d1fa97044.png">
Figure 5: Add Pixel to Graph Frame.

<img width="923" alt="image" src="https://user-images.githubusercontent.com/76194492/182505453-44703a75-4436-4d37-92c6-92e31e7e05c8.png">
Figure 6: Opened Pixela Graph example. 
