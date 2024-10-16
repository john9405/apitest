import threading
import tkinter as tk
import uuid
from tkinter import ttk

from .his import HistoryWindow
from .req import RequestWindow
from .col import CollectionWindow, ProjectWindow, FolderWindow
from .env import EnvironmentWindow, VariableWindow
from .help import HelpWindow
from .about import AboutWindow
from .tools.aes import AesGui
from .tools.b64 import Base64GUI
from .tools.md5 import MD5GUI
from .tools.pwd import GenPwdWindow
from .tools.timestamp import TimestampWindow
from .tools.regex import RegexWindow, CommonlyUsed
from .tools.RSA import RSAKeyFrame, RsaPublicKey, RSACheck, RSAEncrypt, RSADecrypt
from .tools.draft_paper import DraftPaper


class MainWindow:
    tag_list = []  # List of enabled labels
    sidebar = ""
    console_state = False

    def __init__(self):
        self.root = tk.Tk()
        # Create main window
        self.root.title("HTTP Client")
        self.root.after(0, self.on_start)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.geometry("800x600")
        self.root.after(300000, self.write_to_disk)
        self.images = [
            tk.PhotoImage(
                name='col',
                data='iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAchJREFUWEftV21ygjAQfSsHKT1J5b/O9ARFTtJ6EtATdEb/iycp3qNm6+4QDJgW0kFnOpWfZLN5+/YjL4Se7znnuM9m6Pp7RlXXlr7bPFvx62nxbajzALuKDbJtRqXs8QKYr3kHxjTAabApGyQC4gLAfM0LMHLHYwXCBXXBJ8qGdlDVJqXHFgDJ9zFC3hgSSmYoVb/5iHDgIypLd9d/ZHAGcFXaCWV0RCZFOC84PzG6UEIMEmXgqodb6gjl5oWSCwBKywQf1o5HrHxixDbaJmJC2mKgVXSMImIsPydIiYZ3gdTJNqWlDUJ9Gjw1vuqgJDgXlKbABdA1CCk821aa0hWfXGmTSwGvbFcNAgCDPU2wCzkcgLZUw0BdaBphhDgIgFAZOn59I7aVjnqu9DIQGHWw+Z8AMM7IbXPT3Ka9DIiB207BHHs2/NRl3ja8A7gzcGfgXzGgkqw7KK7JgF7PjjC9PQB3UtYS7bYMnAFUkUEi1zjNcp42AoRRbBaUjXEH+PSACBcGCjfN1BGlaiB6fgwQzHhwn3eubDuLZdFwjlYf42Cvjzrn3TV9FwgLqoRHlOSdg5qcewHYn1oPEWKhbjQmDPb2aebz+QWOe7dO2oOpygAAAABJRU5ErkJggg=='
            ),
            tk.PhotoImage(
                name='var',
                data='iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAcRJREFUWEftV21ygkAMfYHeo3qS6n+d6QlETqKeBPAEnaH/pScpvUchZYO7Liv1o8BMHeWXLG7yNpu8vBCc5zXi0Tcwctf7en8C8reQcm2P9I9ZxBPyEGFA5+YQhMwvECogAkCduvDw2dcpL7STpwGNBcA85giE5YUbe/sbA+saQMLq9PW9M+J0SWFvXixDEmkfERgTWSZkGkAFpn64xPQ9pGwIAMrmLOFV5XR9WwAkRzyMdOa60ZEK8rECkKQLik9F7+oINDa05IdbQX6JsV3nR2CvvYIGAEBKxza654+dXrsPAPMtK84IVE4o2iYPjQjIGiGAhw83J7rlAJD7JaaGNQkZF9i4AIoakPCKeyWdAYCwAUvPMLzRAsDQussrDwCPCNx+BLhEaGV97rxL2dllmAZkVNefumEbFQsRlXhhRiJt/RciUt/d1t75Cu6vF0i4NfMRsnRBU7sb7tuxpt6jbtm5HRvRqnidsWnr9XZOnJNzV+dA39rw/wMAITyn67pEpTGDMOJalm95Z7Q6kFdDipndujg72suiEQ5zpwbg6rpenZ4wpljzMJzaanV4BELhqmIaPL0fnSbMeB4KAxG+7Bz7AR7bNVkLvYTOAAAAAElFTkSuQmCC'
            ),
            tk.PhotoImage(
                name='his',
                data='iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAn9JREFUWEetV9tx4zAMXFjXR5xO7P94JhXEViU5VyIpFdyM8h+nklMhsXAGJdESCT6UnH4FAgtgQS4IP/ieK97K8T8ldd91Q7kHJdjXBkci7MDYKec6EARIw1d07yVdcnwnAUjgK+H15vyU49DaMOqCcU5VJwrgqeHXm8HvVYGXxh0D9fuRziEfKgCTdYEqUGrxNfR8KDnAEC4YPgS+ruix16rhATDBN/jQHLJUo8en1l/DEWBLhGOgXSoID8DhjT/czCVwrIxu1pawfvu69kiPc/sFADV4j32I0cIRcRYCp3KIUbcnKicQFsBTxTsaSn8nciK4JajjdO7j8MYnMKqQXwvAy55Qti9Uh1i1sCdc2hfah2yVSthWGAAeyoTD8cydKwl7jdg8VncAUHM1Z+70Mzb/ayqgJjm2bQDQ8N/Z2HlM1YCsBTBWQeJMn4kzAbhN2vhFCOWQK7sF0zmXZ0WPR/LYnyCf6iyDM3LOJaO0mlwCCqrUA6KRsLjCzrb813xoyf4fADpb5Xk+z0dZmbbSa0HOBHgVCI/LgtAqAJedKwB4N5yHwyG0ywFDQm88MqfAkEqu70J/hjVVpE6BUs6seyB2SQWv74a9cVev4tw2rAGh9V8IagCEbqk1AVK2h3n2AKZxvz/Hjv5bK0Ky3w2j4O4CxwJQqrAwTGUY7Lvz0IldK+J+/FxF5IuHlXJs8V4owV1+eZpQlVGEC19xzl02xitXVNBCKWttVWV5cB9g1NjgU1NKMyEqC4wn0UOcCi4mmpZz+jzfB2M7AWJjHd2MIvI6j5MZ61lyN7T3RP5+aNaxXz2anGc9C8CUrt1+CmyZ8UDDSgaeVrTA1hQr1z/YEshuS7ifxQAAAABJRU5ErkJggg=='
            ),
            tk.PhotoImage(
                name='right',
                data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAM5JREFUOE+1ksENgkAUROejBRBsABMhsQqlEzguFiEWYTgClUAXJuKBBkQKwP2KiagcXJSwt012Zt5MljDw0EA9xjfQw4NJPI2Yaq8Sy6JLrCSY7Y8uE0UAF5KuTtdEaWCEpwjM7jOZmL3zxo7be4Oo8SQFyOw9KCGQqJOGhvQwX2uMtLe4jaa4FAvvfwNwUfr2nF4V3hm+12Egu/iW0yh+HvGuCEph7domqu5GmG/BCJp3kuBUwso+WFUGj3+gaSsJTrriXhVUAcoNRje4AS5HThGKogbHAAAAAElFTkSuQmCC'
            ),
            tk.PhotoImage(
                name='left',
                data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAMhJREFUOE+1k80RgjAQhfehBSAVwAFm7AI6kSNYBNqEOWIn0IUHPNCASAHIOhmGH3VGiBlzTPZ7eZu3AWkuaPL0HwFTFD6YEkYT1tG2/Obyw4GEDaZMQi0oqCM3XyywORUZiPweAHN423vnWQFTXGzwOp3CI8STFmD3+0yU32M3gIQNXmVE4+HSZFo0jr6AvO03F1xWsee8pGCJa0rMu6EF0KGK3OPsI04LLFEknQhs5Rh7oW4WOG3xCJQHaWkCw6yoAu/12p/pCc44SU1DCcWEAAAAAElFTkSuQmCC'
            ),
            tk.PhotoImage(
                name='add',
                data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAASJJREFUOE+lk11ugkAUhc+lLsDqBjQpJt0FrER9hC5CXYTwqDuBXZiAibOBUt8r3GZmFJlBSG3ncebeb865P4R/HrLzh/Fh4mAwZ4ZHgAewYJAgIlHhe3MO3kUzxwAM49xzGEm3KBYg2heBu7nF1IBHyRXBBy7C4cHJ+JV5+fkx28u7GjCKshNAk2ZgEbrqfRTlbKpiUVHpSzs6ID7uwLywpXcD1NdraeXPAAbSr9D1rxK1fOn5HLhpX2dVl1RNWBThbGp4pEZxuiB3ACAtKsBrlCe65+bpq4FpIc5XYKyfAeh5eFsqBVrWS/L7NgIVXaZ1GyVkvM0WTLSzB6Z0ytQepGaxjVHWEKxsJXdozyjfgtrLJF/aia1deNQ2CbO3z477AXnBoxFYbQ0+AAAAAElFTkSuQmCC1'
            ),
            tk.PhotoImage(
                name='subtract',
                data='iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAPxJREFUOE+dk0EOgjAQRf8Q3KsnwERMvAWcRF3CJdRLyFI9idzCREzkBOhe7RhaFEq0VbvszLz2z58hGE432XuXaJybcqgdLIscdOZgntYxzkFOKnBdtoEaoJ9kczAWn18sQbQpIn/5zHkB7MUNLGHxhEhAN8kCh7EzadVjnAu6h6UcCegnx7Wu2Y5iID3HfqgAq8MJIM9e1szgvIhHgwqQsQw1tL2DKYfciWp0BZCX7J6+B9QWF7FPf0vQetBbZTsCgp96IOdhOKtsbMj4kiLoNnjZqKy0TWFNFoTwEvmp6nt19A4bvtFyyrBMIqhnQ+2AwG1rXKZ3m2lb5wfrMX4RRvB8VgAAAABJRU5ErkJggg=='
            )
        ]
        col_top = None
        history_top = None
        state_bar = ttk.Frame(self.root)
        state_bar.pack(side=tk.BOTTOM, fill=tk.X)
        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(side=tk.BOTTOM, fill=tk.X)
        side_bar = ttk.Frame(self.root)
        label1 = ttk.Label(side_bar, image='col')
        label2 = ttk.Label(side_bar, image='var')
        label3 = ttk.Label(side_bar, image='his')
        label1.bind('<Button-1>', lambda e: self.main_bar_show('col', col_top, history_top))
        label2.bind('<Button-1>', lambda e: self.main_bar_show('var', col_top, history_top))
        label3.bind('<Button-1>', lambda e: self.main_bar_show('his', col_top, history_top))
        label1.pack(padx=3, pady=3)
        label2.pack()
        label3.pack(padx=3, pady=3)
        side_bar.pack(side=tk.LEFT, fill=tk.Y)
        panel_window = ttk.PanedWindow(self.root, orient="horizontal")
        main_bar = ttk.Frame(panel_window)
        col_top = ttk.Frame(main_bar)
        self.col_win = CollectionWindow(col_top, **{"callback": self.collection})
        col_top.pack(fill='both', expand=True)
        self.sidebar = 'col'
        self.env_win = EnvironmentWindow(master=main_bar, callback=self.environment)
        history_top = ttk.Frame(main_bar)
        self.history_window = HistoryWindow(history_top, self.history)
        panel_window.add(main_bar, weight=1)
        main_frame = ttk.Frame(panel_window)
        nbb = ttk.Notebook(main_frame)
        nbb.pack(fill='both', expand=True)
        self.nbb = nbb
        panel_window.add(main_frame, weight=10)
        panel_window.pack(fill='both', expand=True)

        menu = tk.Menu(self.root)
        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label="New request", command=self.new_request)
        file_menu.add_command(label="New collection", command=self.col_win.new_proj)
        file_menu.add_command(label="Import", command=self.col_win.open_proj)
        file_menu.add_command(label="Export", command=self.col_win.export_proj)
        file_menu.add_command(label="Write data", command=self.write_to_disk)
        file_menu.add_command(label="Exit", command=self.on_closing)
        menu.add_cascade(label="File", menu=file_menu)
        tool_menu = tk.Menu(menu, tearoff=False)
        tool_menu.add_command(label="AES", command=lambda: self.new_tab(AesGui, "AES"))
        tool_menu.add_command(label="Base64", command=lambda: self.new_tab(Base64GUI, "Base64"))
        tool_menu.add_command(label="MD5", command=lambda: self.new_tab(MD5GUI, "MD5"))
        tool_menu.add_command(label="Password", command=lambda: self.new_tab(GenPwdWindow, "Password"))
        tool_menu.add_command(label="Timestamp", command=lambda: self.new_tab(TimestampWindow, "Timestamp"))
        tool_menu.add_command(label="Regular Expression ", command=lambda: self.new_tab(RegexWindow, "Regular Expression "))
        tool_menu.add_command(label="Common Regular Expressions", command=lambda: self.new_tab(CommonlyUsed, "Common Regular Expressions"))
        tool_menu.add_command(label="RSA Key", command=lambda: self.new_tab(RSAKeyFrame, "RSA Key"))
        tool_menu.add_command(label="RSA Public Key", command=lambda: self.new_tab(RsaPublicKey, "RSA Public Key"))
        tool_menu.add_command(label="RSA Check", command=lambda: self.new_tab(RSACheck, "RSA Check"))
        tool_menu.add_command(label="RSA Encrypt", command=lambda: self.new_tab(RSAEncrypt, "RSA Encrypt"))
        tool_menu.add_command(label="RSA Decrypt", command=lambda: self.new_tab(RSADecrypt, "RSA Decrypt"))
        tool_menu.add_command(label='DraftPaper', command=lambda: self.new_tab(DraftPaper, "DraftPaper"))
        menu.add_cascade(label="Tools", menu=tool_menu)
        help_menu = tk.Menu(menu, tearoff=False)
        help_menu.add_command(label="Help", command=lambda: self.new_tab(HelpWindow, "Help"))
        help_menu.add_command(label="About", command=lambda: self.new_tab(AboutWindow, "About"))
        menu.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menu)

        ttk.Sizegrip(state_bar).pack(side="right", anchor="se")
        btn1 = ttk.Label(state_bar, image="subtract")
        btn2 = ttk.Label(state_bar, image="add")
        btn3 = ttk.Label(state_bar, image="right")
        btn4 = ttk.Label(state_bar, image="left")
        btn1.bind("<Button-1>", self.close_tab)
        btn2.bind("<Button-1>", lambda e: self.new_request())
        btn3.bind("<Button-1>", self.next_tab)
        btn4.bind("<Button-1>", self.previous_tab)
        btn1.pack(side="right", padx=(0, 3))
        btn2.pack(side="right")
        btn3.pack(side="right")
        btn4.pack(side="right")

    def main_bar_show(self, name, col_box, his_box):
        if self.sidebar != name:
            if self.sidebar == 'col':
                col_box.forget()
            elif self.sidebar == 'var':
                self.env_win.root.forget()
            elif self.sidebar == 'his':
                his_box.forget()

            if name == 'col':
                col_box.pack(fill='both', expand=True)
            elif name == 'var':
                self.env_win.root.pack(fill='both', expand=True)
            elif name == 'his':
                his_box.pack(fill='both', expand=True)

            self.sidebar = name

    def new_request(self, data=None, **kwargs):
        tl = ttk.Frame(self.nbb)
        req_win = RequestWindow(
            window=tl,
            get_script=self.col_win.get_script,
            env_variable=self.env_win.get_variable,
            glb_variable=self.env_win.get_globals,
            local_variable=self.col_win.get_variable,
            cache_history=self.history_window.on_cache,
            save_item=self.col_win.save_item,
            path=kwargs.get('path', "Name:"),
            callback=self.request,
        )
        req_win.item_id = kwargs.get("item_id")
        name = "New Request"
        if data is not None:
            req_win.fill_blank(data)
            name = data.get("name", "New Request")
        self.nbb.add(tl, text=name)
        self.nbb.select(tl)
        if data is None:
            self.tag_list.append(str(uuid.uuid1()))  # new request

    def on_start(self):
        t1 = threading.Thread(target=self.col_win.on_start)
        t2 = threading.Thread(target=self.env_win.on_start)
        t3 = threading.Thread(target=self.history_window.on_start)
        t1.start()
        t2.start()
        t3.start()

    def write_to_disk(self):
        self.col_win.on_close()
        self.env_win.on_end()
        self.history_window.on_end()

    def on_closing(self):
        self.write_to_disk()
        self.root.destroy()

    def request(self, **kwargs):
        name = kwargs.get('name')
        if name is not None:
            self.nbb.tab(self.nbb.index("current"), text=name)
        item_id = kwargs.get('item_id')
        if item_id is not None:
            index = self.nbb.index("current")
            self.tag_list[index] = f"col_{kwargs['item_id']}"

    def update_tab(self, **kwargs):
        name = kwargs.get('name')
        if name is not None:
            self.nbb.tab(self.nbb.index("current"), text=name)

    def collection(self, **kwargs):
        if f"col_{kwargs['item_id']}" in self.tag_list:
            self.nbb.select(self.tag_list.index(f"col_{kwargs['item_id']}"))
            return

        if kwargs["tag"] == "project":
            frame = ttk.Frame(self.nbb)
            ProjectWindow(
                master=frame,
                item_id=kwargs["item_id"],
                callback=self.col_win.save_item,
                data=kwargs["data"],
            )
            self.nbb.add(frame, text=kwargs["data"]['name'])
            self.nbb.select(frame)
        elif kwargs["tag"] == "folder":
            frame = ttk.Frame(self.nbb)
            FolderWindow(
                master=frame,
                item_id=kwargs["item_id"],
                callback=self.col_win.save_item,
                data=kwargs["data"],
                path=kwargs['path'],
            )
            self.nbb.add(frame, text=kwargs["data"]['name'])
            self.nbb.select(frame)
        else:
            self.new_request(kwargs["data"], item_id=kwargs["item_id"], path=kwargs['path'], )
        self.tag_list.append(f"col_{kwargs['item_id']}")

    def history(self, **kwargs):
        """History callback"""
        if kwargs['data']['uuid'] in self.tag_list:
            self.nbb.select(self.tag_list.index(kwargs['data']['uuid']))
            return
        self.new_request(kwargs.get("data"))
        self.tag_list.append(kwargs['data']['uuid'])

    def environment(self, **kwargs):
        if f'env_{kwargs.get("item_id")}' in self.tag_list:
            self.nbb.select(self.tag_list.index(f'env_{kwargs.get("item_id")}'))
            return
        frame = ttk.Frame(self.nbb)
        VariableWindow(
            frame,
            item_id=kwargs.get('item_id'),
            index=kwargs.get('index'),
            collection=kwargs.get("collection", ""),
            data=kwargs.get("data", {}),
            set_variable=self.env_win.set_variable,
            set_active=self.env_win.set_active,
        )
        self.tag_list.append(f'env_{kwargs.get("item_id")}')
        self.nbb.add(frame, text=kwargs.get("collection", "Var"))
        self.nbb.select(frame)

    def previous_tab(self, event):
        try:
            # 获取当前选中的选项卡的索引
            current_tab_index = self.nbb.index("current")
            # 计算上一个选项卡的索引
            previous_tab_index = (current_tab_index - 1) % self.nbb.index("end")
            # 选中上一个选项卡
            self.nbb.select(previous_tab_index)
        except tk.TclError:
            pass

    def next_tab(self, event):
        try:
            # 获取当前选中的选项卡的索引
            current_tab_index = self.nbb.index("current")
            # 计算下一个选项卡的索引
            next_tab_index = (current_tab_index + 1) % self.nbb.index("end")
            # 选中下一个选项卡
            self.nbb.select(next_tab_index)
        except tk.TclError:
            pass

    def new_tab(self, ui, text):
        if text in self.tag_list:
            self.nbb.select(self.tag_list.index(text))
            return
        frame = ttk.Frame(self.nbb)
        ui(master=frame)
        self.tag_list.append(text)
        self.nbb.add(frame, text=text)
        self.nbb.select(frame)

    def close_tab(self, event):
        try:
            index = self.nbb.index('current')
            self.tag_list.pop(index)
            self.nbb.forget(index)
        except tk.TclError:
            pass
