    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        image.thumbnail((300, 300))  # Resize the image
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo