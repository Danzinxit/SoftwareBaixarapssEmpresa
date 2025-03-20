import tkinter as tk
from tkinter import messagebox, PhotoImage, Label
from PIL import Image, ImageTk
import requests
import subprocess
import threading  # Para download em paralelo

# Lista de Apps e seus links
apps = {
    "Google Chrome": "https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7BDE47FF55-C368-4019-1C36-DB1EA44002A7%7D%26lang%3Dpt-BR%26browser%3D4%26usagestats%3D1%26appname%3DGoogle%2520Chrome%26needsadmin%3Dprefers%26ap%3Dx64-statsdef_1%26installdataindex%3Dempty/update2/installers/ChromeSetup.exe",
    "Any Desk": "https://download.anydesk.com/AnyDesk.exe",
    "Adobe Acrobat": "https://dw.uptodown.net/dwn/SVdZHiJFWhrc1GJknpGfIBdgUzDiiFXxYrtJMjCYUieqR2n7Tq7tAi1GQKFn8-I5KvFKbMqYoOa5pPDzR2t7v7-eSYa46yaBPUdjZVJKZGekRmwm5QTWn-LJcEwAzCqw/fZpPUazRZvQqwLM40-xkm9cG_TPlRmrqjEK9vEBl54pbYUM_AumxvzStRrWg01iATuXkzUDzXlhRNOMBxT0mSpMmv0ByBSzSAX6BRkLux3Twsbg-30ls7axeidhxA_wO/Szwk-Boey6QJMko4lXpEFv8Dt__c6IYrhz5Lq9zewLNheQ6k5egprt_OBl7yNnlkrzBJtfIbs2cWMd0GUK5UwmEBGKDgWYVUciRkfJ-5wS0=/adobe-acrobat-reader-dc-2025-001-20432.exe",
    "Team Viewer": "https://dl.teamviewer.com/download/TeamViewerQS_x64.exe?ref=https%3A%2F%2Fwww.teamviewer.com%2Fpt-br%2Fdownload%2Fwindows%2F%3F",
    "Winrar": "https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-710br.exe",
    "7-Zip": "https://dw.uptodown.net/dwn/HM4oNUjNTCPubeNdVVRcl-oDcHmO-Ill9vRTstFBibgRn_YhRun5oQDWX0fsKWS_VKpQdUee1d6jyTRSqz4OqV5J1OrYSb7Hjz7_4GMvt4--_v9tLBdoaz1uBL6s7JJe/EfPRmGqqjj1g1XyWFNXNDhEc9U56S5mM8lFy6lyH__h00x_3YJ1w5YdfNg8lO5e624K3wxgjoDXEqq4-RhPkJ2eX1srRT8tY9q22CE4r_PdN85e0R1eT-lUFwvqzCBAc/R7DpLem6uSd6khUGc5zBvOAwlGGvAMXPPSk5rs2ic23b_zfEmEr70iR2LPsRGash/7-zip-24-09.exe",
    "Google Drive": "https://dl.google.com/drive-file-stream/GoogleDriveSetup.exe",
    "Java": "https://sdlc-esd.oracle.com/ESD6/JSCDL/jdk/8u441-b07/7ed26d28139143f38c58992680c214a5/jre-8u441-windows-x64.exe?GroupName=JSC&FilePath=/ESD6/JSCDL/jdk/8u441-b07/7ed26d28139143f38c58992680c214a5/jre-8u441-windows-x64.exe&BHost=javadl.sun.com&File=jre-8u441-windows-x64.exe&AuthParam=1742488489_f9da2d56a4dddfc3c54cbafd611f3741&ext=.exe"
}

def download_file(url, app_name):
    try:
        filename = url.split("/")[-1]
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=4096):  # Aumentando o tamanho do chunk
                    if chunk:
                        f.write(chunk)
            messagebox.showinfo("Sucesso", f"{app_name} foi baixado com sucesso!")
            open_installer(filename)
        else:
            messagebox.showerror("Erro", f"Erro ao baixar {app_name}. Tente novamente.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar {app_name}: {str(e)}")

def open_installer(installer_path):
    try:
        subprocess.Popen(installer_path, shell=True)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível abrir o instalador: {str(e)}")

def start_downloads():
    selected_apps = [app for app, var in app_vars.items() if var.get()]
    if not selected_apps:
        messagebox.showwarning("Aviso", "Nenhum aplicativo selecionado para download.")
        return

    # Usar threads para downloads paralelos
    for app in selected_apps:
        threading.Thread(target=download_file, args=(apps[app], app), daemon=True).start()

def toggle_all_apps():
    select_all = select_all_var.get()
    for var in app_vars.values():
        var.set(select_all)

# Criar a janela principal
root = tk.Tk()
root.title("Baixador de Aplicativos")
root.geometry("500x650")  # Aumentando a janela
root.config(bg="#f0f0f0")

# Carregar a imagem
try:
    img = Image.open("logo_epamig_2024-1024x277.png")
    img = img.resize((150, 150), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)

    label_img = tk.Label(root, image=photo, bg="#fff")
    label_img.image = photo
    label_img.pack(pady=20)

except Exception as e:
    print(f"Erro ao carregar a imagem: {str(e)}")

# Criar um frame para conter os checkbuttons
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20)

# Variável para o checkbox "Selecionar Tudo"
select_all_var = tk.BooleanVar()

# Checkbox "Selecionar Tudo"
select_all_chk = tk.Checkbutton(frame, text="Selecionar Tudo", variable=select_all_var, command=toggle_all_apps,
                                bg="#f0f0f0", font=("Arial", 12))
select_all_chk.pack(anchor="w", padx=10, pady=5)

# Adicionar caixas de seleção para cada aplicativo
app_vars = {}
for app in apps:
    var = tk.BooleanVar()
    chk = tk.Checkbutton(frame, text=app, variable=var, bg="#f0f0f0", font=("Arial", 12))
    chk.pack(anchor="w", padx=10, pady=5)
    app_vars[app] = var

# Adicionar o botão para iniciar os downloads
download_button = tk.Button(root, text="Baixar Selecionados", command=start_downloads, bg="#4CAF50", fg="white",
                            font=("Arial", 12, "bold"))
download_button.pack(pady=10, padx=10, fill='x')

# Iniciar a interface gráfica
root.mainloop()
