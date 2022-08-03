from tkinter import *
from tkinter import messagebox
from save_load import SaveAndLoad
import tkinter.font as tkFont
from pixela import Pixela
import webview
from password_generator import generate_password

FONT_NAME = 'Helvetica'
BG_FRAME_COLOR = "grey82"
FG_FRAME_COLOR = "green"
BUTTON_BG_COLOR = "white"
BUTTON_FG_COLOR = "green"


class ViewGraph(LabelFrame):

    """
    This class creates the LabelFrame object required to view the graphs registered with the Pixela API

        Attributes:
                container (Tk): Tkinter parent object
                controller (LabelFrame): LabelFrame parent object
    """

    def __init__(self, container, controller=None):
        super().__init__(container)
        self.config(bg=BG_FRAME_COLOR, fg=FG_FRAME_COLOR, text="View Graph")

        # give access to UI class / Tk
        self.container = container

        # get pixela object
        self.pixela_list = container.get_pixela_obj_list()

        # input variables
        self.option_variable = StringVar()
        self.select_user()
        self.create_open_url_button()

        # placement
        self.grid(column=1, row=1, padx=30, pady=30, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)

    def create_open_url_button(self):

        """
        Creates "url" button GUI object. When button pressed in GUI the "open_url" method is called.
        """

        delete_graph_name_label = Button(self,
                                         text="Got to URL",
                                         bg=BUTTON_BG_COLOR,
                                         fg=BUTTON_FG_COLOR,
                                         font=(FONT_NAME, 15),
                                         borderwidth=0,
                                         command=self.open_url)
        delete_graph_name_label.grid(column=2, row=1, padx=10, pady=10)

    def open_url(self):

        """
        Takes the selected username and graph from the drop menu GUI object variables then creates and opens the
        corresponding URL in a separate window
        """

        try:
            # get username and graph from drop menu
            user_name, user_graph = self.option_variable.get().split()

        except ValueError:

            messagebox.showerror(title="ERROR", message="Incorrect Field Entry, Try Again")

        else:

            # if username exist in pixel object list open window with associated url
            for item in self.pixela_list:
                if user_name == item.username and user_graph in item.graph_id:
                    # open url in window
                    webview.create_window("Pixela Graph", f"https://pixe.la/v1/users/{user_name}/graphs/{user_graph}.html")
                    webview.start()

    def select_user(self):

        """
        Creates a drop menu GUI object filled with all available usernames and graphs. Selection is stored as
        variable
        """

        drop_menu = DropMenu(parent_container=self, master_container=self.container)
        drop_menu.config(bg=BG_FRAME_COLOR)
        drop_menu.grid(column=1, row=1, padx=10, pady=10)
        self.option_variable = drop_menu.get_option_variable()


class CreateUser(LabelFrame):

    """
    This class creates the LabelFrame object required to register new users with the Pixela API
    """

    def __init__(self, container, controller):
        super().__init__(container)
        self.config(bg=BG_FRAME_COLOR, fg=FG_FRAME_COLOR, text="Create New User")

        # give access to UI class / Tk
        self.container = container

        # give access to FrameController class
        self.controller = controller

        # input variables
        self.new_user_entry = None

        # get pixela object
        self.pixela_list = container.get_pixela_obj_list()

        # instantiate warning message
        self.warning_message = WarningMessage(self)
        self.warning_message.grid(column=1, columnspan=2, row=2, sticky="ew", padx=10, pady=10)

        # startup function calls
        self.get_new_user()

        # placement
        self.grid(column=1, row=1, padx=30, pady=30, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)

    def get_new_user(self):

        """
        Creates username entry field and button GUI objects. Upon activation of the button, inputted username
        information is stored in a variable and the "create_new_user" method is called
        """

        def reset_new_user_entry(event):
            self.new_user_entry.delete(0, "end")

        # create new username entry field GUI object

        self.new_user_entry = Entry(self, width=30, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, font=(FONT_NAME, 15))
        self.new_user_entry.insert(0, "Enter New Username")
        self.new_user_entry.config(width=25)
        self.new_user_entry.bind("<FocusIn>", reset_new_user_entry)
        self.new_user_entry.grid(column=1, row=1, padx=10, pady=10)

        # create new username button GUI object

        new_user_label = Button(self, text="Create New User",
                                bg=BUTTON_BG_COLOR,
                                fg=BUTTON_FG_COLOR,
                                font=(FONT_NAME, 15),
                                borderwidth=0,
                                command=self.create_new_user)
        new_user_label.grid(column=2, row=1, padx=10, pady=10)

    def create_new_user(self):

        """
        Registers new Pixela user with Pixela API using stored username variable
        """

        # generated token required for Pixela API registration
        token = generate_password()

        # register with Pixela API
        response_message = Pixela(username=self.new_user_entry.get(), token=token).create_user()

        # continue only if registration with Pixela API successful
        if self.warning_message.update_warning_message(response_message):
            # save locally
            SaveAndLoad.save(username=self.new_user_entry.get(), token=token)

            # after 2 seconds refresh frame
            self.after(2000, lambda: self.controller.switch_frame(CreateUser))


class WarningMessage(LabelFrame):

    """
    This class creates the warning message LabelFrame object that provides response feedback from Pixela API

            Attributes:
                controller (LabelFrame): LabelFrame parent object
    """

    def __init__(self, controller):
        super().__init__(controller)
        self.config(bg=BG_FRAME_COLOR, fg=FG_FRAME_COLOR, padx=10, pady=10, text="Update Status")

        # create label
        self.result = Label(self, text="None", bg=BG_FRAME_COLOR, fg=FG_FRAME_COLOR, wraplength=250)

        # placement
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.result.grid(column=1, row=1)

    def update_warning_message(self, text):

        """
        Takes response message from Pixela API, prints Pixela API response message then returns if Pixela API
        transaction was successful

            Parameter: text (json): A json formatted string

            Returns: text['isSuccess'] (bool): True or False if Pixela API transaction was successful
        """

        self.result.config(text=f"Message:{text['message']}\n "
                                f"Update Successful:{text['isSuccess']}")

        return text['isSuccess']


class ModifyGraph(LabelFrame):

    """
    This class creates the LabelFrame GUI object required to register a new Pixela graph with Pixela API

            Attributes:
                container (Tk): Tkinter parent object
                controller (LabelFrame): LabelFrame parent object
    """

    def __init__(self, container, controller):
        super().__init__(container)
        self.config(bg=BG_FRAME_COLOR, fg=FG_FRAME_COLOR, text="Add a Pixel to Graph")

        # give access to UI class / Tk
        self.container = container

        # give access to FrameController class
        self.controller = controller

        # instantiate warning message
        self.warning_message = WarningMessage(self)
        self.warning_message.grid(column=0, columnspan=4, row=2, sticky="ew", padx=10, pady=10)

        # get pixela obj
        self.pixela_list = container.get_pixela_obj_list()

        # input variables
        self.add_value_entry = StringVar()
        self.option_variable = StringVar()

        # startup function calls
        self.select_user_and_graph()
        self.add_graph_value()
        self.add_button()

        # placement
        self.grid(column=1, row=1, padx=30, pady=30, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(4, weight=1)

    def add_graph_value(self):

        """
        Creates "add value" input field GUI object. Input value stored as variable.
        """

        def reset_add_value_entry(event):
            self.add_value_entry.delete(0, "end")

        self.add_value_entry = Entry(self, width=24, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, font=(FONT_NAME, 15))
        self.add_value_entry.insert(0, "Enter Value to Add to Graph")
        self.add_value_entry.grid(column=2, row=1, padx=10, pady=10)

        self.add_value_entry.bind("<FocusIn>", reset_add_value_entry)

    def add_button(self):

        """
        Creates "add value" button GUI object. When button is activated, "add_pixel" method is called.
        """

        add_value_button = Button(self,
                                  text="Add value",
                                  bg=BUTTON_BG_COLOR,
                                  fg=BUTTON_FG_COLOR,
                                  font=(FONT_NAME, 15),
                                  borderwidth=0,
                                  command=self.add_pixel)
        add_value_button.config(width=22)
        add_value_button.grid(column=3, row=1, padx=10, pady=10)

    def select_user_and_graph(self):

        """
        Creates a drop menu GUI object filled with all available usernames and graphs. Selection is stored as
        variable
        """

        drop_menu = DropMenu(parent_container=self, master_container=self.container)
        drop_menu.config(bg=BG_FRAME_COLOR)
        drop_menu.grid(column=1, row=1, padx=10, pady=10)
        self.option_variable = drop_menu.get_option_variable()

    def add_pixel(self):

        """
        Register new pixel value using "add to graph" variable with associated user and graph using
        "user and graph" variable with Pixela API
        """

        try:

            # get username and graph from drop menu
            user_name, user_graph = self.option_variable.get().split()

        except ValueError:

            messagebox.showerror(title="ERROR", message="Incorrect Field Entry, Try Again")

        else:

            # if username and graph exist in pixela object list continue
            for index, item in enumerate(self.pixela_list):
                if user_name == item.username and user_graph in item.graph_id:

                    # get current pixela object associated username
                    pixela_obj = self.pixela_list[index]

                    # register pixel with associated username and graph with pixela API
                    response_message = pixela_obj.create_pixel(self.add_value_entry.get(), user_graph)

                    # display response from Pixela API
                    self.warning_message.update_warning_message(response_message)

                    # after 2 seconds refresh frame
                    self.after(2000, lambda: self.controller.switch_frame(ModifyGraph))


class NewGraph(LabelFrame):

    """
    This class creates the LabelFrame GUI object required to register a new graph with the Pixela API

            Attributes:
                container (Tk): Tkinter parent object
                controller (LabelFrame): LabelFrame parent object
    """

    def __init__(self, container, controller):
        super().__init__(container)
        self.config(bg=BG_FRAME_COLOR, fg=FG_FRAME_COLOR, text="Create New Graph")

        # give access to UI class / Tk
        self.container = container

        # give access to FrameController class
        self.controller = controller

        # get pixela object
        self.users = {user_obj.username: user_obj.graph_id for user_obj in container.get_pixela_obj_list()}
        self.pixela_list = container.get_pixela_obj_list()

        # instantiate warning message
        self.warning_message = WarningMessage(self)
        self.warning_message.grid(column=1, row=8, sticky="ew", padx=10, pady=10)

        # input variables
        self.new_graph_units_value = None
        self.user_selection_value = StringVar()
        self.unit_type_value = StringVar()
        self.color_value = StringVar()
        self.new_graph_name_value = None
        self.new_graph_id_value = None

        # startup functions
        self.select_user()
        self.select_graph_units()
        self.select_unit_type()
        self.select_color()
        self.select_graph_name()
        self.select_graph_id()
        self.create_graph_button()

        # frame position
        self.grid(column=1, row=1, padx=30, pady=30, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

    def select_user(self):

        """
        Create drop menu GUI object that is filled with all usernames. Selection is saved as variable
        """

        user_list = self.users.keys()
        self.user_selection_value.set("Select a User")
        drop_menu = OptionMenu(self, self.user_selection_value, *user_list)
        hel_15 = tkFont.Font(family='Helvetica', size=15)
        drop_menu.config(bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, font=hel_15, width=20)
        drop_menu.grid(column=1, row=1, padx=10, pady=10)

    def select_graph_units(self):

        """
        Creates "units of measure" input field GUI object. Input is saved as variable
        """

        def reset_graph_units_entry(event):
            self.new_graph_units_value.delete(0, "end")

        self.new_graph_units_value = Entry(self, width=24, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, font=(FONT_NAME, 15))
        self.new_graph_units_value.insert(0, "Enter Unit of Measure")
        self.new_graph_units_value.grid(column=1, row=2, padx=10, pady=10)
        self.new_graph_units_value.bind("<FocusIn>", reset_graph_units_entry)

    def select_unit_type(self):

        """
        Create drop menu GUI object that is filled with unit type options ["int", "float"]. Selection is saved as
        variable
        """

        unit_list = ["int", "float"]
        self.unit_type_value.set("Select a Unit Type")
        drop_menu_unit_type = OptionMenu(self, self.unit_type_value, *unit_list)
        hel_15 = tkFont.Font(family='Helvetica', size=15)
        drop_menu_unit_type.config(bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, font=hel_15, width=20)
        drop_menu_unit_type.grid(column=1, row=3, padx=10, pady=10)

    def select_color(self):

        """
        Create drop menu GUI object that is filled with color options ["shibafu", "momiji", "sora", "ichou",
        "ajisai", "kuro"]. Selection is saved as variable
        """

        color_list = ["shibafu", "momiji", "sora", "ichou", "ajisai", "kuro"]
        self.color_value.set("Select a Color")
        drop_menu_color = OptionMenu(self, self.color_value, *color_list)
        hel_15 = tkFont.Font(family='Helvetica', size=15)
        drop_menu_color.config(bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, font=hel_15, width=20)
        drop_menu_color.grid(column=1, row=4, padx=10, pady=10)

    def select_graph_name(self):

        """
        Create "graph name" input field GUI object. Input is stored as variable
        """

        def reset_graph_name_entry(event):
            self.new_graph_name_value.delete(0, "end")

        self.new_graph_name_value = Entry(self, width=24, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, font=(FONT_NAME, 15))
        self.new_graph_name_value.insert(0, "Enter Graph Name")
        self.new_graph_name_value.grid(column=1, row=5, padx=10, pady=10)
        self.new_graph_name_value.bind("<FocusIn>", reset_graph_name_entry)

    def select_graph_id(self):

        """
        Create "graph id" input field GUI object. Input is stored as variable
        """

        def reset_graph_id_entry(event):
            self.new_graph_id_value.delete(0, "end")

        self.new_graph_id_value = Entry(self, width=24, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, font=(FONT_NAME, 15))
        self.new_graph_id_value.insert(0, "Enter Graph ID")
        self.new_graph_id_value.grid(column=1, row=6, padx=10, pady=10)
        self.new_graph_id_value.bind("<FocusIn>", reset_graph_id_entry)

    def create_graph_button(self):

        """
        Create "create graph" button GUI object. When button is activated "register_graph" method is called.
        """

        graph_name_label = Button(self,
                                  text="Create Graph",
                                  bg=BUTTON_BG_COLOR,
                                  fg=BUTTON_FG_COLOR,
                                  font=(FONT_NAME, 15),
                                  borderwidth=0,
                                  command=self.register_graph)
        graph_name_label.config(width=22)
        graph_name_label.grid(column=1, row=7, padx=10, pady=10)

    def register_graph(self):

        """
        Register new graph using "username", "unit_value", "unit_type","graph_name" and "graph_id" variables with
        Pixela API
        """

        # get username from field GUI
        user_name = self.user_selection_value.get()

        # if username  exist in pixela object list continue
        for index, item in enumerate(self.pixela_list):
            if user_name == item.username:

                # get pixel object associated with current user
                pixela_obj = self.pixela_list[index]

                # register current pixela object user with Pixela API
                response_message = pixela_obj.create_graph(graph_id=self.new_graph_id_value.get(),
                                                           graph_name=self.new_graph_name_value.get(),
                                                           units=self.new_graph_units_value.get(),
                                                           unit_type=self.unit_type_value.get(),
                                                           color=self.color_value.get())

                # continue only if registration with Pixela API successful
                if self.warning_message.update_warning_message(response_message):

                    # update pixela current pixel object with new graph data
                    pixela_obj.update_graph_id_list(self.new_graph_id_value.get())

                    # save locally
                    SaveAndLoad.save(username=user_name, graph_list=pixela_obj.get_graph_id_list())

                    # after 2 seconds refresh frame
                    self.after(2000, lambda: self.controller.switch_frame(NewGraph))


class DeleteGraph(LabelFrame):

    """
    This class creates the LabelFrame GUI object required to delete a graph with the Pixela API
            Attributes:
                container (Tk): Tkinter parent object
                controller (LabelFrame): LabelFrame parent object
    """

    def __init__(self, container, controller):
        super().__init__(container)
        self.config(bg=BG_FRAME_COLOR, fg=FG_FRAME_COLOR, text="Delete Graph")

        # get pixela object
        self.pixela_list = container.get_pixela_obj_list()

        # give access to FrameController class
        self.controller = controller

        # Instantiate warning message
        self.warning_message = WarningMessage(self)
        self.warning_message.grid(column=1, columnspan=2, row=8, sticky="ew", padx=10, pady=10)

        # give access to UI class / TK
        self.container = container

        # input variables
        self.option_variable = StringVar()

        # startup function
        self.select_user()
        self.create_delete_button()

        # placement
        self.grid(column=1, row=1, padx=30, pady=30, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)

    def create_delete_button(self):

        """
        Creates a "delete" button GUI object. When button is activated the "delete_graph" method is called
        """

        delete_graph_name_label = Button(self,
                                         text="Delete Graph",
                                         bg=BUTTON_BG_COLOR,
                                         fg=BUTTON_FG_COLOR,
                                         font=(FONT_NAME, 15),
                                         borderwidth=0,
                                         command=self.delete_graph)
        delete_graph_name_label.grid(column=2, row=1, padx=10, pady=10)

    def select_user(self):

        """
        Creates a drop menu GUI object filled with all available usernames and graphs. Selection is stored as
               variable
        """

        drop_menu = DropMenu(parent_container=self, master_container=self.container)
        drop_menu.config(bg=BG_FRAME_COLOR)
        drop_menu.grid(column=1, row=1, padx=10, pady=10)
        self.option_variable = drop_menu.get_option_variable()

    def delete_graph(self):

        """
        Delete graph associated with username registered with Pixela API
        """

        try:

            # get username and graph from input fields
            user_name, user_graph = self.option_variable.get().split()

        except ValueError:

            messagebox.showerror(title="ERROR", message="Incorrect Field Entry, Try Again")

        else:

            # if username exist in pixela object list continue
            for index, item in enumerate(self.pixela_list):
                if user_name == item.username and user_graph in item.graph_id:

                    # get pixela object for current username
                    pixela_obj = self.pixela_list[index]

                    # delete graph corresponding to username and graph selection with Pixela API
                    response_message = pixela_obj.delete_graph(user_graph)

                    # continue only if registration with Pixela API successful
                    if self.warning_message.update_warning_message(response_message):

                        # update pixela current pixel object by deleting selected graph data
                        pixela_obj.delete_graph_id(user_graph)

                        # save locally
                        SaveAndLoad.save(username=user_name, graph_list=pixela_obj.get_graph_id_list())

                        # after 2 seconds refresh frame
                        self.after(2000, lambda: self.controller.switch_frame(DeleteGraph))


class DropMenu(Frame):

    """
    This class create a nest drop menu GUI object
            Attributes:
                parent_container (Frame): Parent object
                master_container (Tk): Tkinter parent object
    """

    def __init__(self, parent_container, master_container):
        super().__init__(parent_container)

        # get Pixela object
        self.users = {user_obj.username: user_obj.graph_id for user_obj in master_container.get_pixela_obj_list()}

        # input variable
        self.option_variable = StringVar()

        # create nested option menu
        self.option_variable.set("Select Username and Graph")
        menubutton = Menubutton(self, textvariable=self.option_variable)
        top_menu = Menu(menubutton, tearoff=False)
        hel_15 = tkFont.Font(family='Helvetica', size=15)
        menubutton.config(menu=top_menu, fg=BUTTON_FG_COLOR, bg=BUTTON_BG_COLOR, font=hel_15, width=20)

        for key in sorted(self.users.keys()):
            menu = Menu(top_menu)
            top_menu.add_cascade(label=key, menu=menu)
            for graph_id in self.users[key]:
                menu.add_radiobutton(label=graph_id, variable=self.option_variable, value=(key, graph_id))

        menubutton.grid(column=1, row=1, padx=10, pady=10)

    def get_option_variable(self):

        """
        Returns selected drop menu string.
                Return:
                        option_variable (str): Returns selected drop menu string variable.
        """

        return self.option_variable


class ControlFrame(LabelFrame):

    """
    This class creates the LabelFrame GUI object required to select "Pixel Control Panel" options. Additionally,
    this class  facilitates the switching mechanism between  ViewGraph, CreateUser, NewGraph, DeleteGrap and
    ModifyGraph frames

            Attributes:
                container (Tk): Tkinter parent object
    """

    def __init__(self, container):
        super().__init__(container)
        self.config(bg=BG_FRAME_COLOR, fg=FG_FRAME_COLOR, text="Options")

        # give access to UI class / TK
        self.container = container

        # frame instantiation variable
        self.frame = None

        # input variable
        self.selected_value = IntVar()
        self.selected_value.set(0)

        # placement
        self.switch_frame(ViewGraph)

        # placement
        self.grid(column=1, row=2, padx=10, pady=10)

        # create radio buttons corresponding to frame options. Each radio button instantiates selected frame.
        # Frame selections include ViewGraph, CreateUser, NewGraph, DeleteGraph, ModifyGraph
        Radiobutton(
            self,
            text="View Graph",
            value=0,
            variable=self.selected_value,
            bg=BG_FRAME_COLOR,
            fg=FG_FRAME_COLOR,
            command=lambda: self.switch_frame(ViewGraph)
        ).grid(column=0, row=0)

        Radiobutton(
            self,
            text="Create User",
            value=1,
            variable=self.selected_value,
            bg=BG_FRAME_COLOR,
            fg=FG_FRAME_COLOR,
            command=lambda: self.switch_frame(CreateUser)
        ).grid(column=1, row=0)

        Radiobutton(
            self,
            text="Create New Graph",
            value=2,
            variable=self.selected_value,
            bg=BG_FRAME_COLOR,
            fg=FG_FRAME_COLOR,
            command=lambda: self.switch_frame(NewGraph)
        ).grid(column=2, row=0)

        Radiobutton(
            self,
            text="Delete Graph",
            value=3,
            variable=self.selected_value,
            bg=BG_FRAME_COLOR,
            fg=FG_FRAME_COLOR,
            command=lambda: self.switch_frame(DeleteGraph)
        ).grid(column=3, row=0)

        Radiobutton(
            self,
            text="Add a Pixel to Graph",
            value=4,
            variable=self.selected_value,
            bg=BG_FRAME_COLOR,
            fg=FG_FRAME_COLOR,
            command=lambda: self.switch_frame(ModifyGraph)
        ).grid(column=4, row=0)

    def switch_frame(self, frame_class):

        """
        Accepts captured function containing class to be instantiated. Each class instantiation corresponds to be
        a different frame object in the Pixela Control Panel.
            Parameter: frame_class (class): Class to be instantiated
        """

        # create new labelframe class instantiation
        new_frame = frame_class(self.container, self)

        # destroy any old labelframe class instantiations
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.grid(column=1, row=1)


class UI(Tk):

    """
    This class instantiates Tkinter module and provides base window for GUI
    """

    def __init__(self):
        super().__init__()
        self.title("Pixela Control Panel")
        self.config(bg="white", padx=10, pady=10)

        # create Pixela banner
        self.img = PhotoImage(file="./pixela_logo.png")
        self.image_label = Label(self, image=self.img, borderwidth=0, bg="white")
        self.image_label.grid(column=1, row=0)

    def get_pixela_obj_list(self):

        """
        Takes local data.json data if it exists and creates pixela_object list
                Returns:
                        pixela_obj_list (Pixela) : Pixela object list created using local data.json
         """

        pixela_obj_list = []

        if SaveAndLoad.get_userdata() is not None:
            for user_name, data in SaveAndLoad.get_userdata().items():
                pixela_obj_list.append(Pixela(user_name, data["token"], data["graph_id"]))

        return pixela_obj_list
