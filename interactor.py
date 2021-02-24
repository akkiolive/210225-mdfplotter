import tkinter as tk
import re


class Interactor:
    def __init__(self):
        pass



    def OpenFileSelector(self):
        pass
    

    def SignalSelector(self, all_signals, already_selected):
        class SEL:
            def __init__(self):
                root = tk.Tk()
                root.title("")
                root.minsize(width=400, height=500)
                pw = tk.PanedWindow(root, orient="vertical")
                pw.pack(expand=True, fill=tk.BOTH)
                frame = tk.Frame(pw, relief=tk.RIDGE, bd=1)
                frame.pack(expand=True, fill=tk.BOTH)
                def callback(var, idx, mode):
                    inp = sv.get()
                    inp_reg = "^" + inp.replace("*", ".*")
                    
                    print("")
                    for signal_name in all_signals:
                        if re.match(inp_reg, signal_name, flags = re.I):
                            print(signal_name)
                            txt = lb.get(0, "end")
                            if signal_name not in txt:
                                lb.insert(tk.END, signal_name)
                        else:
                            txt = lb.get(0, "end")
                            removed_idx = []
                            for i, t in enumerate(txt):
                                if t == signal_name:
                                    lb.delete(i)
                                    removed_idx.append(i)
                            txt = lb.get(0, "end")
                            dic = {}
                            for i, v in enumerate(txt):
                                dic[v] = i
                            
                sv = tk.StringVar()
                sv.trace_add("write", callback)
                search_box_frame = tk.Frame(frame)
                entry = tk.Entry(search_box_frame, textvariable=sv, validatecommand=lambda: print(entry.get()))
                entry.grid(row=0, column=0, sticky=tk.W)
                entry.focus()
                clear_button = tk.Button(search_box_frame, text="clear", command=lambda: entry.delete(0, tk.END))
                clear_button.grid(row=0, column=1, sticky=tk.E)
                def push_action():
                    sels = lb.curselection()
                    txt = lb.get(0, "end")
                    to_be_pushed = []
                    for sel in sels:
                        name = txt[sel]
                        lb.delete(sel)
                        to_be_pushed.append(name)
                    sels = lb.curselection() 
                    while sels:
                        lb.delete(sels[0])
                        sels = lb.curselection() 
                    for signal_name in to_be_pushed:
                        lb2.insert("end", signal_name)
                        already_selected.append(signal_name)
                def pop_action():
                    sels = lb2.curselection()
                    txt = lb2.get(0, "end")
                    to_be_poped = []
                    for sel in sels:
                        name = txt[sel]
                        to_be_poped.append(name)
                    sels = lb2.curselection() 
                    while sels:
                        lb2.delete(sels[0])
                        sels = lb2.curselection() 
                    for signal_name in to_be_poped:
                        lb.insert("end", signal_name)
                        for num, sign in enumerate(already_selected):
                            if signal_name == sign:
                                already_selected.pop(num)
                push_button = tk.Button(search_box_frame, text="add", command=push_action)
                pop_button = tk.Button(search_box_frame, text="remove", command=pop_action)
                push_button.grid(row=0, column=2)
                pop_button.grid(row=0, column=3)
                search_box_frame.pack(fill=tk.X, expand=False)

                lb = tk.Listbox(frame, selectmode="extended")
                sb = tk.Scrollbar(frame, orient=tk.VERTICAL, command=lb.yview)
                lb["yscrollcommand"] = sb.set
                sb.pack(side=tk.RIGHT,  fill="y")
                sbx = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=lb.xview)
                lb["xscrollcommand"] = sbx.set
                sbx.pack(side=tk.BOTTOM,  fill="x")
                lb.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                for signal_name in all_signals:
                    if signal_name not in already_selected:
                        lb.insert(tk.END, signal_name)


                frame2 = tk.Frame(pw)
                frame2.pack(expand=True, fill=tk.BOTH, pady=5)
                lb2 = tk.Listbox(frame2, selectmode="extended")
                sb2 = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=lb2.yview)
                lb2["yscrollcommand"] = sb2.set
                sb2.pack(side=tk.RIGHT,  fill="y")
                sb2x = tk.Scrollbar(frame2, orient=tk.HORIZONTAL, command=lb2.xview)
                lb2["xscrollcommand"] = sb2x.set
                sb2x.pack(side=tk.BOTTOM,  fill="x")
                lb2.pack(fill=tk.BOTH, expand=True)
                for signal_name in already_selected:
                    lb2.insert(tk.END, signal_name)
                pw.add(frame)
                pw.add(frame2)

                self.ret_txt = list(lb2.get(0, "end"))
                self.ok_pushed = False
                
                def ret_action():
                    self.ok_pushed = True
                    self.ret_txt = list(lb2.get(0, "end"))
                    root.destroy()
                    
                class ButtonFrame:
                    def __init__(self, root):
                        self.frame = tk.Frame(root)
                        self.buttonOK = tk.Button(self.frame, text="OK", command=ret_action)
                        self.buttonCancel = tk.Button(self.frame, text="Cancel", command=lambda: root.destroy())
                        self.buttonOK.grid(row=0, column=0, sticky=tk.S)
                        self.buttonCancel.grid(row=0, column=1, sticky=tk.S)
                        self.frame.pack(anchor=tk.S, fill=tk.BOTH, expand=False, padx=5, pady=0)
                ButtonFrame(root)

                root.mainloop()
        
        Sel = SEL()
        return (Sel.ok_pushed, Sel.ret_txt)

if __name__ == "__main__":
    interact = Interactor()
    print(interact.SignalSelector(["TOKY_2020", "2020_TOKYO", "adfad32342sadf43fd342",
    "asdfasdfasdfsadfsadfsafadfasfsafsafadasdfasdfasdfsadfasdfsadfsadfsadfasfsadfsafsadfs",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    ], ["asdfasdfasdfsadfsadfsafadfasfsafsafadasdfasdfasdfsadfasdfsadfsadfsadfasfsadfsafsadfs",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    ]))
            

