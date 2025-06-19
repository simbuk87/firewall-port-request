## 📘 Flow Diagram Connector Tool

A Python-based GUI application to create and manage flow diagrams with node-to-node connections. Designed for visualizing system architecture, network flows, or any logical process using labeled nodes and directional links.

Built with **Tkinter** for the UI and **Pillow** for image export.

---

### 🚀 Features

* 🧱 **Create Nodes**: Click anywhere to create labeled nodes.
* 🔗 **Connect Nodes**: Select two nodes to draw a directional connection between them with protocol/port info.
* ✏️ **Edit Nodes/Connections**: Double-click to modify names or connection attributes.
* ❌ **Delete**: Right-click to delete individual nodes or connections.
* 💾 **Export Options**:

  * Export connection data to **CSV**
  * Export the diagram to **PNG**

---

### 📦 Requirements

Install dependencies via pip:

```bash
pip install pillow
```

---

### ▶️ How to Run

```bash
python flow_diagram_tool.py
```

You can now:

* Click to create a node
* Click two nodes to connect them
* Double-click or right-click for edit/delete
* Use the buttons to export your diagram

---

### 🗃️ File Export

* **CSV**: Contains connection data: source, destination, protocol, port, direction, and purpose.
* **PNG**: Captures the entire canvas as a flow diagram image.

---

### 📸 Preview


![Screenshot 2025-06-20 005000](https://github.com/user-attachments/assets/4d130d1d-0b6c-428a-9c11-79a990be875e)

### 📸 Exported .CSV File
![image](https://github.com/user-attachments/assets/99d0e85b-b256-4ef5-974e-619152bef17b)

---

### ⚠️ Disclaimer

This tool is intended for educational, visualization, and personal documentation purposes. Please ensure your use complies with any relevant data handling or copyright guidelines.

---

### 📝 License

This project is licensed under the [MIT License](LICENSE).

---
