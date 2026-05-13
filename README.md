# Wan2GP Canvas Plugin

A powerful plugin for **Wan2GP** that adds an integrated **Canvas Editor** directly into the UI. It allows you to draw, move, resize, rotate, and edit images with ease.

## 🚀 Main Features

- **Canvas Image Support:** Import your own images or paste them directly from the clipboard.
- **Precision Tools:** Move (nudge), resize, rotate, flip, and adjust opacity with advanced controls.
- **Multi-Layer Support:** Draw non-destructively with customizable brushes, colors, and layer management.
- **Export Options:** Save your work locally as `.png` or `.jpg`.
- **Fully Local & Secure:** This is a native client-side plugin built with React/Gradio. No cloud services, no telemetry, and no hidden connections. Your data stays on your device.

## ⚠ Send to Ref > Work In Progress

The **"Send to Reference"** button is currently a **work in progress**.  
I haven't managed to get this feature working correctly yet.

If anyone has experience with Wan2GP internals, Gradio communication, or knows how to properly send images to the reference system, feel free to contact me or contribute. Any help or guidance would be greatly appreciated!

## 📦 Installation

Installing the plugin is simple — just copy the folder into Wan2GP:

1. Download and/or extract the zip containing the `wan2gp_canvas_plugin` folder so that it includes its contents (`__init__.py`, `plugin.py`, the `dist` directory, etc.).
2. Move the entire `wan2gp_canvas_plugin` folder into the `plugins/` subdirectory of your Wan2GP installation (final path: `wan2gp/plugins/wan2gp_canvas_plugin`).
3. Launch (or restart) Wan2GP.
4. You will find the new **"Canvas Editor"** tab ready to use!

## 🛠 Built With

- **Python** & **Gradio** for the integration bridge with Wan2GP
- **React** & **Konva** (Vite single-file mode) for the canvas editor UI

## 📝 License

Released under the **MIT License**.  
Feel free to use, modify, and share this plugin freely!
