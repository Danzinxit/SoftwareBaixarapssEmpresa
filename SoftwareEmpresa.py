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
    "Team Viewer": "https://dl.teamviewer.com/download/version_15x/TeamViewer_Setup_x64.exe?ref=https%3A%2F%2Fwww.teamviewer.com%2Fpt-br%2Fdownload%2Fwindows%2F",
    "Winrar": "https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-710br.exe",
    "7-Zip": "https://dw.uptodown.net/dwn/HM4oNUjNTCPubeNdVVRcl-oDcHmO-Ill9vRTstFBibgRn_YhRun5oQDWX0fsKWS_VKpQdUee1d6jyTRSqz4OqV5J1OrYSb7Hjz7_4GMvt4--_v9tLBdoaz1uBL6s7JJe/EfPRmGqqjj1g1XyWFNXNDhEc9U56S5mM8lFy6lyH__h00x_3YJ1w5YdfNg8lO5e624K3wxgjoDXEqq4-RhPkJ2eX1srRT8tY9q22CE4r_PdN85e0R1eT-lUFwvqzCBAc/R7DpLem6uSd6khUGc5zBvOAwlGGvAMXPPSk5rs2ic23b_zfEmEr70iR2LPsRGash/7-zip-24-09.exe",
    "Google Drive": "https://dl.google.com/drive-file-stream/GoogleDriveSetup.exe",
    "Java": "https://sdlc-esd.oracle.com/ESD6/JSCDL/jdk/8u441-b07/7ed26d28139143f38c58992680c214a5/jre-8u441-windows-x64.exe?GroupName=JSC&FilePath=/ESD6/JSCDL/jdk/8u441-b07/7ed26d28139143f38c58992680c214a5/jre-8u441-windows-x64.exe&BHost=javadl.sun.com&File=jre-8u441-windows-x64.exe&AuthParam=1742488489_f9da2d56a4dddfc3c54cbafd611f3741&ext=.exe"
}


def download_file(url, app_name, label_status):
    try:
        filename = url.split("/")[-1]
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=4096):  # Aumentando o tamanho do chunk
                    if chunk:
                        f.write(chunk)
            label_status.config(text=f"Instalando {app_name}...")
            open_installer(filename, app_name)
        else:
            messagebox.showerror("Erro", f"Erro ao baixar {app_name}. Tente novamente.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar {app_name}: {str(e)}")


def open_installer(installer_path, app_name):
    try:
        # Apenas o Google Chrome será instalado silenciosamente
        silent_args = ""
        if app_name == "Google Chrome":
            silent_args = "/silent"

        # Para os outros aplicativos, não há argumentos silenciosos
        subprocess.Popen([installer_path, silent_args], shell=True)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível abrir o instalador: {str(e)}")


def start_downloads():
    selected_apps = [app for app, var in app_vars.items() if var.get()]
    if not selected_apps:
        messagebox.showwarning("Aviso", "Nenhum aplicativo selecionado para download.")
        return

    # Usar threads para downloads paralelos
    for app in selected_apps:
        label_status = app_labels[app]  # Obter o Label associado ao app
        threading.Thread(target=download_file, args=(apps[app], app, label_status), daemon=True).start()


def toggle_all_apps():
    select_all = select_all_var.get()
    for var in app_vars.values():
        var.set(select_all)


# Criar a janela principal
root = tk.Tk()
root.title("Baixador de Aplicativos")
root.geometry("400x550")  # Janela menor e mais compacta
root.resizable(False, False)  # Desabilitar o redimensionamento
root.config(bg="#f0f0f0")

# Criar o frame principal para centralizar o conteúdo
frame_main = tk.Frame(root, bg="#f0f0f0")
frame_main.place(relx=0.5, rely=0.5, anchor="center")

# Carregar a imagem (opcional)
try:
    img = Image.open("logo_epamig_2024-1024x277.png")
    img = img.resize((120, 120), Image.ANTIALIAS)  # Reduzir o tamanho da imagem
    photo = ImageTk.PhotoImage(img)

    label_img = tk.Label(frame_main, image=photo, bg="#fff")
    label_img.image = photo
    label_img.grid(row=0, column=0, columnspan=2, pady=15)

except Exception as e:
    print(f"Erro ao carregar a imagem: {str(e)}")

# Criar o frame de seleção
frame = tk.Frame(frame_main, bg="#f0f0f0")
frame.grid(row=1, column=0, columnspan=2, pady=5)

# Variável para o checkbox "Selecionar Tudo"
select_all_var = tk.BooleanVar()

# Checkbox "Selecionar Tudo"
select_all_chk = tk.Checkbutton(frame, text="Selecionar Tudo", variable=select_all_var, command=toggle_all_apps,
                                bg="#f0f0f0", font=("Arial", 10))
select_all_chk.grid(row=0, column=0, padx=5, pady=3, sticky="w")

# Adicionar caixas de seleção para cada aplicativo e Labels de status
app_vars = {}
app_labels = {}  # Dicionário para armazenar os Labels de status

for i, app in enumerate(apps):
    var = tk.BooleanVar()
    chk = tk.Checkbutton(frame, text=app, variable=var, bg="#f0f0f0", font=("Arial", 10))
    chk.grid(row=i + 1, column=0, padx=5, pady=2, sticky="w")  # Reduzindo o pady entre os checkboxes

    # Criar o Label de status
    label_status = tk.Label(frame, text="", bg="#f0f0f0", font=("Arial", 8))
    label_status.grid(row=i + 1, column=1, padx=5, pady=2, sticky="w")

    app_vars[app] = var
    app_labels[app] = label_status

# Adicionar o botão para iniciar os downloads
download_button = tk.Button(frame_main, text="Baixar Selecionados", command=start_downloads, bg="#4CAF50", fg="white",
                            font=("Arial", 10, "bold"))
download_button.grid(row=len(apps) + 1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Texto discreto de Direitos Autorais
copyright_label = tk.Label(frame_main, text="© AINF 2025", bg="#f0f0f0", font=("Arial", 8), fg="#888")
copyright_label.grid(row=len(apps) + 2, column=0, columnspan=2, pady=5)

# Iniciar a interface gráfica
root.mainloop()
