import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
import csv
from PIL import Image

class NodeConnectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flow Diagram Connector Tool")
        self.canvas = tk.Canvas(root, width=1024, height=600, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.nodes = []
        self.connections = []
        self.selected_nodes = []
        self.selected_connection = None

        export_btn = tk.Button(root, text="Export to CSV", command=self.export_to_csv, bg="blue", fg="white", width=20)
        export_btn.pack(pady=5)

        export_png_btn = tk.Button(root, text="Export Diagram as PNG", command=self.export_diagram_png, bg="green", fg="white", width=20)
        export_png_btn.pack(pady=5)

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Double-1>", self.on_double_click)
        self.canvas.bind("<Button-3>", self.on_right_click)

    def on_click(self, event):
        clicked_node = None
        for node in self.nodes:
            x1, y1, x2, y2 = self.canvas.bbox(node['shape'])
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                clicked_node = node
                break

        if clicked_node:
            self.toggle_selection(clicked_node)
        else:
            # Check if clicked on a connection line
            items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
            if items:
                self.select_connection(items[0])
            else:
                self.create_node(event.x, event.y)

    def on_double_click(self, event):
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if not items:
            return

        item = items[0]
        for conn in self.connections:
            if conn['arrow'] == item or conn['label'] == item:
                self.ask_port_details(None, None, conn_ref=conn)
                return

        for node in self.nodes:
            if node['text'] == item:
                self.edit_node_text(node)
                return

    def on_right_click(self, event):
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if not items:
            return

        item = items[0]

        # Check if it's a connection
        for conn in list(self.connections):
            if conn['arrow'] == item or conn['label'] == item:
                self.delete_connection(conn)
                return

        # Check if it's a node
        for node in list(self.nodes):
            if node['shape'] == item or node['text'] == item:
                self.delete_node(node)
                return

    def toggle_selection(self, node):
        if node in self.selected_nodes:
            self.selected_nodes.remove(node)
            self.canvas.itemconfig(node['shape'], outline="black", width=1)
        else:
            self.selected_nodes.append(node)
            self.canvas.itemconfig(node['shape'], outline="yellow", width=3)

        if len(self.selected_nodes) == 2:
            src, dst = self.selected_nodes
            self.ask_port_details(src, dst)
            self.selected_nodes.clear()  # Clear selection immediately after connection is made
            self.canvas.itemconfig(src['shape'], outline="black", width=1)
            self.canvas.itemconfig(dst['shape'], outline="black", width=1)

    def create_node(self, x, y):
        name = simpledialog.askstring("Node Name", "Enter name for the node:")
        if not name:
            return

        # shape = self.canvas.create_oval(x - 50, y - 25, x + 50, y + 25, fill="lightblue", tags="node")
        # text = self.canvas.create_text(x, y, text=name, tags="node")
        # self.nodes.append({'name': name, 'shape': shape, 'text': text})

        shape = self.canvas.create_oval(x - 50, y - 25, x + 50, y + 25, fill="lightblue", tags="node")
        text = self.canvas.create_text(x, y, text=name, tags="node")
        self.canvas.tag_bind(text, "<Double-Button-1>", lambda e, t=text: self.edit_node_text(t))
        self.nodes.append({'name': name, 'shape': shape, 'text': text})


    def edit_node_text(self, text_item):
        current_text = self.canvas.itemcget(text_item, "text")
        new_text = simpledialog.askstring("Edit Node Name", "Enter new name:", initialvalue=current_text)
        if new_text:
            self.canvas.itemconfig(text_item, text=new_text)
            for node in self.nodes:
                if node['text'] == text_item:
                    node['name'] = new_text
                    break
                    
    # def edit_node_text(self, node):
        # current_text = self.canvas.itemcget(text_item, "text")
 # #       new_text = simpledialog.askstring("Edit Node Name", "Enter new name:", initialvalue=current_text)
        # if new_text:
            # self.canvas.itemconfig(text_item, text=new_text)
            # for node in self.nodes:
                # if node['text'] == text_item:
                    # node['name'] = new_text
                    # break
    # def edit_node_text(self, node):
        # # Get the current name of the node
        # current_text = self.canvas.itemcget(node['text'], "text")

        # # Create an entry widget to allow the user to edit the name
        # entry = tk.Entry(self.canvas)
        # entry.insert(0, current_text)
        
        # # Position the entry widget at the same location as the node
        # x1, y1, x2, y2 = self.canvas.bbox(node['shape'])
        # entry.place(x=(x1 + x2) / 2 - 50, y=(y1 + y2) / 2 - 25)

        # def save_edit():
            # new_text = entry.get()
            # if new_text != current_text:
                # self.canvas.itemconfig(node['text'], text=new_text)  # Update the text of the node
                # node['name'] = new_text  # Update the internal node data
            # entry.destroy()  # Destroy the entry widget after editing is done

        # def cancel_edit(event):
            # entry.destroy()  # Destroy the entry widget if the user clicks outside the field

        # # Bind the Enter key to save the text and destroy the entry widget
        # entry.bind("<Return>", lambda event: save_edit())
        # # Bind the Escape key to cancel the edit and destroy the entry widget
        # entry.bind("<Escape>", cancel_edit)

    def ask_port_details(self, src_node, dst_node, conn_ref=None):
        popup = tk.Toplevel(self.root)
        popup.title("Connection Details")

        tk.Label(popup, text="Purpose:").grid(row=0, column=0)
        purpose_entry = tk.Entry(popup)
        purpose_entry.grid(row=0, column=1)

        tk.Label(popup, text="Protocol:").grid(row=1, column=0)
        proto_var = tk.StringVar(value="TCP")
        proto_frame = tk.Frame(popup)
        for proto in ["TCP", "UDP", "ICMP", "Others"]:
            tk.Radiobutton(proto_frame, text=proto, variable=proto_var, value=proto).pack(side=tk.LEFT)
        proto_frame.grid(row=1, column=1)

        tk.Label(popup, text="Direction:").grid(row=2, column=0)
        dir_var = tk.StringVar(value="uni")
        dir_frame = tk.Frame(popup)
        tk.Radiobutton(dir_frame, text="Uni-direction", variable=dir_var, value="uni").pack(side=tk.LEFT)
        tk.Radiobutton(dir_frame, text="Bi-direction", variable=dir_var, value="bi").pack(side=tk.LEFT)
        dir_frame.grid(row=2, column=1)

        tk.Label(popup, text="Port(s):").grid(row=3, column=0)
        port_entry = tk.Entry(popup)
        port_entry.grid(row=3, column=1)

        if conn_ref:
            purpose_entry.insert(0, conn_ref['Purpose'])
            proto_var.set(conn_ref['Protocol'])
            port_entry.insert(0, conn_ref['Destination Port'])

        def submit():
            purpose = purpose_entry.get()
            proto = proto_var.get()
            direction = dir_var.get()
            ports = port_entry.get() if proto != "ICMP" else "ICMP"

            if not purpose or not proto or not direction or (proto != "ICMP" and not ports):
                messagebox.showwarning("Missing Fields", "Please complete all fields")
                return

            if conn_ref:
                conn_ref.update({
                    'Purpose': purpose,
                    'Protocol': proto,
                    'Destination Port': ports
                })
                self.canvas.itemconfig(conn_ref['label'], text=f"{proto}/{ports}")
            else:
                self.create_connection(src_node, dst_node, purpose, proto, ports, direction)

            self.selected_nodes.clear()
            for node in self.selected_nodes:
                self.canvas.itemconfig(node['shape'], outline="black", width=1)
            self.selected_nodes.clear()
            popup.destroy()

        tk.Button(popup, text="Connect", command=submit).grid(row=4, column=0, columnspan=2)

    def create_connection(self, src, dst, purpose, proto, ports, direction):
        x1, y1 = self.get_center(src)
        x2, y2 = self.get_center(dst)

        offset = 10 if direction == "bi" else 0
        dx = offset if y1 == y2 else 0
        dy = offset if x1 == x2 else 0

        line = self.canvas.create_line(x1 - dx, y1 - dy, x2 - dx, y2 - dy, width=2, arrow=tk.LAST, tags="connection")
        label = self.canvas.create_text((x1 + x2) / 2 - dx, (y1 + y2) / 2 - dy - 10,
                                        text=f"{proto}/{ports}", font=("Arial", 6), tags="connection")

        conn = {
            'Purpose': purpose,
            'Source': self.canvas.itemcget(src['text'], "text"),
            'Destination': self.canvas.itemcget(dst['text'], "text"),
            'Protocol': proto,
            'Destination Port': ports,
            'Direction': "Bi-direction" if direction == "bi" else "Uni-direction",
            'arrow': line,
            'label': label
        }
        self.connections.append(conn)

        if direction == "bi":
            line2 = self.canvas.create_line(x2 + dx, y2 + dy, x1 + dx, y1 + dy, width=2, arrow=tk.LAST, tags="connection")
            label2 = self.canvas.create_text((x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy + 10,
                                             text=f"{proto}/{ports}", font=("Arial", 6), tags="connection")
            self.connections.append({
                **conn,
                'Source': conn['Destination'],
                'Destination': conn['Source'],
                'arrow': line2,
                'label': label2
            })

    def get_center(self, node):
        coords = self.canvas.bbox(node['shape'])
        x = (coords[0] + coords[2]) / 2
        y = (coords[1] + coords[3]) / 2
        return x, y

    def select_connection(self, item):
        for conn in self.connections:
            if conn['arrow'] == item or conn['label'] == item:
                if self.selected_connection == conn:
                    self.canvas.itemconfig(conn['arrow'], fill="black")
                    self.selected_connection = None
                else:
                    if self.selected_connection:
                        self.canvas.itemconfig(self.selected_connection['arrow'], fill="black")
                    self.canvas.itemconfig(conn['arrow'], fill="red")
                    self.selected_connection = conn
                return

    def delete_connection(self, connection):
        self.canvas.delete(connection['arrow'])
        self.canvas.delete(connection['label'])
        self.connections.remove(connection)

    def delete_node(self, node):
        self.canvas.delete(node['shape'])
        self.canvas.delete(node['text'])
        self.nodes.remove(node)

        # Delete associated connections
        for conn in list(self.connections):
            if conn['Source'] == node['name'] or conn['Destination'] == node['name']:
                self.delete_connection(conn)

    def export_to_csv(self):
        if not self.connections:
            messagebox.showinfo("No Data", "No connection data to export.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            with open(file_path, mode="w", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["Purpose", "Source", "Destination", "Protocol", "Destination Port", "Direction"])
                writer.writeheader()
                for conn in self.connections:
                    writer.writerow({k: conn[k] for k in writer.fieldnames})
            messagebox.showinfo("Export Complete", f"Data exported to {file_path}")

    def export_diagram_png(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if not file_path:
            return
        self.canvas.postscript(file="temp.ps", colormode='color')
        img = Image.open("temp.ps")
        img.save(file_path, "png")
        messagebox.showinfo("Export Complete", f"Diagram exported to {file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = NodeConnectorApp(root)
    root.mainloop()
