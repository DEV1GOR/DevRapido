import customtkinter as ctk
from tkinter import PhotoImage

class Home(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configuracoes_janela_inicial()
        self.home()

    def configuracoes_janela_inicial(self):
        self.geometry("700x400")
        self.title("Novo Milionário")
        self.resizable(False, False)
        self.configure(fg_color="#3b5704")

    def home(self):
        self.img = PhotoImage(file="logo.png")
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=1, column=0, padx=70, pady=20)

        self.frame_home = ctk.CTkFrame(self, width=350, height=380, fg_color="#6c921f")
        self.frame_home.place(x = 350, y = 70)

        self.descricao = ctk.CTkLabel(self.frame_home, text="TESTE SEUS\nCONHECIMENTOS EM\nEDUCAÇÃO FINANCEIRA", font=("Times New Roman", 25, "bold"), text_color="#edffcc")
        self.descricao.grid(row=1, column=0, pady=10, padx = 10)

        self.btn_placar = ctk.CTkButton(self.frame_home, width=300, text="PLACAR", font=("Times New Roman", 20, "bold"), corner_radius=15, fg_color="#edffcc", text_color="#3b5704", hover_color="#59981a")
        self.btn_placar.grid(row=5, column=0, padx=10, pady=10)

        self.btn_perfil = ctk.CTkButton(self.frame_home, width=300, text="PERFIL", font=("Times New Roman", 20, "bold"), corner_radius=15, fg_color="#edffcc", text_color="#3b5704", hover_color="#59981a")
        self.btn_perfil.grid(row=6, column=0, padx=10, pady=10)

        self.btn_quiz = ctk.CTkButton(self.frame_home, width=300, text="QUIZ", font=("Times New Roman", 20, "bold"), corner_radius=15, fg_color="#edffcc", text_color="#3b5704", hover_color="#59981a", command=self.quizzes)
        self.btn_quiz.grid(row=7, column=0, padx=10, pady=10)

    def quizzes(self):
        self.frame_home.place_forget()

        self.frame_quizzes = ctk.CTkFrame(self, width=350, height=380, fg_color="#6c921f")
        self.frame_quizzes.place(x = 350, y = 80)

        self.escolha = ctk.CTkLabel(self.frame_quizzes, text="ESCOLHA A\nDIFICULDADE:", font=("Times New Roman", 25, "bold"), text_color="#edffcc")
        self.escolha.grid(row=1, column=0, pady=10, padx = 10)

        self.btn_facil = ctk.CTkButton(self.frame_quizzes, width=300, text="FÁCIL", font=("Times New Roman", 20, "bold"), corner_radius=15, fg_color="#edffcc", text_color="#3b5704", hover_color="#59981a")
        self.btn_facil.grid(row=5, column=0, padx=10, pady=10)

        self.btn_medio = ctk.CTkButton(self.frame_quizzes, width=300, text="MÉDIO", font=("Times New Roman", 20, "bold"), corner_radius=15, fg_color="#edffcc", text_color="#3b5704", hover_color="#59981a")
        self.btn_medio.grid(row=6, column=0, padx=10, pady=10)

        self.btn_dificil = ctk.CTkButton(self.frame_quizzes, width=300, text="DIFÍCIL", font=("Times New Roman", 20, "bold"), corner_radius=15, fg_color="#edffcc", text_color="#3b5704", hover_color="#59981a", command=self.quizzes)
        self.btn_dificil.grid(row=7, column=0, padx=10, pady=10)


if __name__ == "__main__":
     app = Home()
     app.mainloop()