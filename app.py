import customtkinter as ctk
from tkinter import PhotoImage


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configuracoes_janela_inicial()
        self.tela_login()

    def configuracoes_janela_inicial(self):
        self.geometry("700x400")
        self.title("Novo Milionário")
        self.resizable(False, False)
        self.configure(fg_color="#3b5704")


        
    def tela_login(self):
        
        self.img = PhotoImage(file="logo.png")
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=1, column=0, padx=70, pady=20)

        self.title = ctk.CTkLabel(self, text="LOGIN", font=("Times New Roman", 40, "bold"), text_color="#edffcc")
        self.title.grid(row=8, column=0, pady=10, padx = 10)

        self.frame_login = ctk.CTkFrame(self, width=350, height=380, fg_color="#6c921f")
        self.frame_login.place(x = 350, y = 30)

        self.email_login_entrada = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="E-mail", font=("Times New Roman", 20, "bold"), corner_radius=15, fg_color="#edffcc", placeholder_text_color="#59981a", border_color="#3b5704")
        self.email_login_entrada.grid(row=1, column=0, padx=10, pady=10)

        self.senha_login_entrada = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Senha", font=("Times New Roman", 20, "bold"), corner_radius=15, fg_color="#edffcc", placeholder_text_color="#59981a", border_color="#3b5704", show="!")
        self.senha_login_entrada.grid(row=2, column=0, padx=10, pady=10)

        self.ver_senha = ctk.CTkCheckBox(self.frame_login, text="Ver Senha", font=("Times New Roman", 15, "bold"), corner_radius=20, checkmark_color="#edffcc", fg_color="#3b5704", text_color="#edffcc", hover_color="#59981a")
        self.ver_senha.grid(row=3, column=0, padx=10, pady=10)

        self.btn_login = ctk.CTkButton(self.frame_login, width=300, text="FAZER LOGIN", font=("Times New Roman", 20, "bold"), corner_radius=15, fg_color="#edffcc", text_color="#3b5704", hover_color="#59981a")
        self.btn_login.grid(row=4, column=0, padx=10, pady=10)

        self.span = ctk.CTkLabel(self.frame_login, text="Se você não tem conta...", font=("Times New Roman", 15, "bold"), text_color="#edffcc")
        self.span.grid(row=5, column=0, padx=5, pady=5)

        self.btn_cad_red = ctk.CTkButton(self.frame_login, width=300, text="FAZER CADASTRO", font=("Times New Roman", 20, "bold"), corner_radius=15, fg_color="#edffcc", text_color="#3b5704", hover_color="#59981a", command=self.tela_cadastro)
        self.btn_cad_red.grid(row=6, column=0, padx=10, pady=10)

    def tela_cadastro(self):
        self.frame_login.place_forget()
        self.title.place_forget()

        self.title = ctk.CTkLabel(self, text="CADASTRO", font=("Times New Roman", 40, "bold"), text_color="#edffcc")
        self.title.grid(row=8, column=0, pady=10, padx = 10)

        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=380, fg_color="#6c921f")
        self.frame_cadastro.place(x = 350, y = 30)

        self.usuario_cadastro_entrada = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Nome de Usuário", font=("Times New Roman", 20, "bold"), corner_radius=15, fg_color="#edffcc", placeholder_text_color="#59981a", border_color="#3b5704")
        self.usuario_cadastro_entrada.grid(row=1, column=0, padx=10, pady=5)

        self.email_cadastro_entrada = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="E-mail", font=("Times New Roman", 20, "bold"), corner_radius=15, fg_color="#edffcc", placeholder_text_color="#59981a", border_color="#3b5704")
        self.email_cadastro_entrada.grid(row=2, column=0, padx=10, pady=5)

        self.senha_cadastro_entrada = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Senha", font=("Times New Roman", 20, "bold"), corner_radius=15, fg_color="#edffcc", placeholder_text_color="#59981a", border_color="#3b5704", show="!")
        self.senha_cadastro_entrada.grid(row=3, column=0, padx=10, pady=5)
        
        self.confirmar_senha_entrada = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Confirme sua senha", font=("Times New Roman", 20, "bold"), corner_radius=15, fg_color="#edffcc", placeholder_text_color="#59981a", border_color="#3b5704", show="!")
        self.confirmar_senha_entrada.grid(row=4, column=0, padx=10, pady=5)

        self.ver_senha = ctk.CTkCheckBox(self.frame_cadastro, text="Ver Senha", font=("Times New Roman", 15, "bold"), corner_radius=20, checkmark_color="#edffcc", fg_color="#3b5704", text_color="#edffcc", hover_color="#59981a")
        self.ver_senha.grid(row=5, column=0, padx=10, pady=5)

        self.btn_cadastro = ctk.CTkButton(self.frame_cadastro, width=300, text="FAZER CADASTRO", font=("Times New Roman", 20, "bold"), corner_radius=15, fg_color="#edffcc", text_color="#3b5704", hover_color="#59981a")
        self.btn_cadastro.grid(row=6, column=0, padx=10, pady=5)

        self.btn_log_red = ctk.CTkButton(self.frame_cadastro, width=300, text="FAZER LOGIN", font=("Times New Roman", 20, "bold"), corner_radius=15, fg_color="#edffcc", text_color="#3b5704", hover_color="#59981a", command=self.tela_login)
        self.btn_log_red.grid(row=7, column=0, padx=10, pady=5)

if __name__ == "__main__":
     app = App()
     app.mainloop()
