tree_scroll = Scrollbar(search_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=tree_scroll.set)
tree_scroll.grid(row=4, column=5, sticky="ns")