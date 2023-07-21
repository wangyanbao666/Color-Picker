import tkinter as tk

def show_color_popup(color):
    root = tk.Tk()
    root.geometry("400x100")
    # Set window attributes to make it appear at the top and not minimize
    root.wm_attributes("-topmost", 1)
    root.overrideredirect(True) 
    root.attributes("-alpha", 0.8)     
    
    # Calculate the position to center the window on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 400
    window_height = 100
    x = (screen_width-window_width//2) // 2
    y = (screen_height - window_height) // 4
    root.geometry(f"+{x}+{y}")
    # customize title bar
    title_bar = tk.Frame(root, bg='#2e2e2e', relief='raised', bd=2,highlightthickness=0)

    # put a close button on the title bar
    close_button = tk.Button(title_bar, text='X', command=root.destroy,bg="#2e2e2e",padx=2,pady=2,activebackground='red',bd=0,font="bold",fg='white',highlightthickness=0)

    # pack the widgets
    title_bar.pack(expand=1, fill=tk.X)
    close_button.pack(side=tk.RIGHT)

    # Create a frame to hold the color block and text
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)
    # Create a canvas to display the color block
    color_canvas = tk.Canvas(frame, width=50, height=50, bg=color, highlightthickness=0)
    color_canvas.pack(side=tk.LEFT)

    # Create a label to display the color in hex
    color_hex_label = tk.Label(frame, text=f"Color: {color}", font=("Arial", 12))
    color_hex_label.pack(side=tk.LEFT, padx=(10, 20))
    root.after(3000, root.destroy)
    
    # # Show and focus the window
    # root.deiconify()
    # root.lift()
    
    root.mainloop()