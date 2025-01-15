import customtkinter
from tkinter import *
from collections import defaultdict
from tabulate import tabulate


APP_NAME = "Приорітет апартаментів"
WIDTH = 600
HEIGHT = 360


item_names = {
    1: "Ціна",
    2: "Краєвиди",
    3: "Ізюминка",
    4: "Затишок",
    5: "Кухонна поверхня",
    6: "Тераса",
    7: "Доступність",
    8: "Додаткові послуги",
    9: "Зовнішній вигляд будинку",
    10: "Наявність інтернету"
}

root = customtkinter.CTk()
root.title("Приорітет будинків")

label1 = customtkinter.CTkLabel(root, text= "Пункт", height=10)
label1.place(x = 260, y = 10)
label2 = customtkinter.CTkLabel(root, text= "Кількість збігів", height=10)
label2.place(x = 385, y = 10)
label3 = customtkinter.CTkLabel(root, text= "Приорітетність", height=10)
label3.place(x = 495, y = 10)

text_out1 = customtkinter.CTkTextbox(root,width=200, height=280)
text_out1.place(x=170, y = 30)
text_out1.insert(text="\n".join([f'{key}: {value}' for key, value in item_names.items()]), index=END)
text_out1.configure(state = "disabled")

text_out2 = customtkinter.CTkTextbox(root,width=100, height=280)
text_out2.place(x=380, y = 30)
text_out2.configure(state = "disabled")

text_out3 = customtkinter.CTkTextbox(root,width=100, height=280)
text_out3.place(x=490, y = 30)
text_out3.configure(state = "disabled")

root.geometry(f"{WIDTH}x{HEIGHT}")

def analyze_priorities(all_responses, item_names):
    priority_counts = defaultdict(lambda: defaultdict(int))

    for response in all_responses:
        for rank, item in enumerate(response, start=1):
            priority_counts[item][rank] += 1

    most_common_priorities = []
    print(priority_counts.items)
    for item, ranks in priority_counts.items():
        if item != ",":
            most_common_rank = max(ranks, key=ranks.get)
            frequency = ranks[most_common_rank]

            additional_frequency = 0
            if most_common_rank > 1:
                additional_frequency += ranks.get(most_common_rank - 1, 0)
            if most_common_rank < 10:
                additional_frequency += ranks.get(most_common_rank + 1, 0)

            most_common_priorities.append([item_names[int(item)], f"{frequency} ({additional_frequency})", most_common_rank])

    most_common_priorities.sort(key=lambda x: x[2])

    headers = ["Пункт", "Кількість збігів (додаткові збіги)", "Місце пріоритетності"]
    
    
    result = tabulate(most_common_priorities, headers=headers, tablefmt='pretty')

    text1 = ""
    text2 = ""
    for value in most_common_priorities:
        text1 += f"{value[1]}\n"
        text2 += f"{value[2]}\n"
    print(most_common_priorities)
    text_out2.configure(state = "normal")
    text_out2.delete('1.0', END)
    text_out2.insert(text=text1, index=END)

    text_out3.configure(state = "normal")
    text_out3.delete('1.0', END)
    text_out3.insert(text=text1, index=END)

    with open("result.txt", "w") as file:
        file.write(result)
        file.close()

def create_matrix():
    text = textbox.get('1.0', END)
    apartaments_text = text.strip().split("\n")  # Видаляємо зайві пробіли та розділяємо на апартаменти
    apartaments = []

    for apartament in apartaments_text:
        if apartament:  # Перевірка чи рядок не пустий
            numbers = [int(num) for num in apartament.split(",")]  # Конвертація кожного числа в int
            apartaments.append(numbers)

    analyze_priorities(apartaments, item_names)



textbox = customtkinter.CTkTextbox(root,width=150, height=300)
textbox.place(x = 10, y= 10)


button = customtkinter.CTkButton(root,text="Відсортувати дані", width=580, command=create_matrix)
button.place(x = 10, y = 320)

root.mainloop()