import pyttsx3
import wikipedia as wp
import tkinter as tk
import threading
import speech_recognition as sr

result = ""  # Global variable to store search result


def search_wikipedia():
    global result
    topic = topic_entry.get()
    sentences = sentences_entry.get()

    try:
        n = int(sentences)
    except ValueError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Please enter a valid number of sentences.")
        return

    if n <= 0:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Please enter a number greater than zero for sentences.")
        return

    try:
        result = wp.summary(topic, sentences=n)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result)
    except wp.DisambiguationError as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END,
                           f"Ambiguous search query. Please be more specific.\n\nOptions:\n{', '.join(e.options)}")
    except wp.PageError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "No matching page found on Wikipedia.")

    voice = pyttsx3.init()
    voice.say(result)
    voice.runAndWait()


def search_and_play_audio():
    global result
    topic = topic_entry.get()
    sentences = sentences_entry.get()

    try:
        n = int(sentences)
    except ValueError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Please enter a valid number of sentences.")
        return

    if n <= 0:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Please enter a number greater than zero for sentences.")
        return

    try:
        result = wp.summary(topic, sentences=n)
    except wp.DisambiguationError as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END,
                           f"Ambiguous search query. Please be more specific.\n\nOptions:\n{', '.join(e.options)}")
        return
    except wp.PageError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "No matching page found on Wikipedia.")
        return

    # Update status label
    status_label.config(text="Searching Wikipedia and playing audio...")

    # Create thread for searching Wikipedia and playing audio
    search_thread = threading.Thread(target=search_wikipedia)

    # Start search thread
    search_thread.start()

    # Create a separate thread for playing audio
    audio_thread = threading.Thread(target=perform_audio)
    audio_thread.start()


def perform_audio():
    voice = pyttsx3.init()
    voice.say(result)
    voice.runAndWait()

    # Update status label
    status_label.config(text="Audio playback complete.")

def listen_and_search():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening... Speak your topic.")
        audio_data = recognizer.listen(source, timeout=8)

    try:
        topic = recognizer.recognize_google(audio_data)
        topic_entry.delete(0, tk.END)
        topic_entry.insert(0, topic)
        status_label.config(text="Topic recognized.")

    except sr.UnknownValueError:
        status_label.config(text="Sorry, could not understand audio. Please try again.")
    except sr.RequestError as e:
        status_label.config(text=f"Speech recognition request failed: {e}")


root = tk.Tk()
root.title("Wikipedia Search")
root.geometry("500x500")
root.config(bg="lightblue")
root.resizable(False, False)
heading_label = tk.Label(root, text="Voice Assistant Using Python", font=("Times New Roman", 20, "bold"),
                         bg="lightblue")
heading_label.pack(pady=10)

topic_label = tk.Label(root, text="Enter Topic to Search on Wikipedia:", font=("Times New Roman", 12, "bold"))
topic_label.pack()

topic_entry = tk.Entry(root, width=50, font=("Arial", 10))
topic_entry.pack()
break_line1 = tk.Label(root, text="", bg="lightblue")
break_line1.pack()

sentences_label = tk.Label(root, text="Enter the number of sentences:", font=("Times New Roman", 12, "bold"))
sentences_label.pack()

sentences_entry = tk.Entry(root, width=5, font=("Times New Roman", 10))
sentences_entry.pack()

break_line2 = tk.Label(root, text="", bg="lightblue")
break_line2.pack()

search_button = tk.Button(root, text="Search and Play Audio", command=search_and_play_audio,
                          font=("Times New Roman", 12),
                          bg="green", fg="white")
search_button.pack()
voice_input_button = tk.Button(root, text="Voice Input", command=listen_and_search, font=("Times New Roman", 12),
                               bg="blue", fg="white")
voice_input_button.pack()

status_label = tk.Label(root, text="Enter a topic and the number of sentences, then click 'Search and Play Audio'.",
                        font=("Times New Roman", 10), fg="blue")
status_label.pack()

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text = tk.Text(root, wrap=tk.WORD, width=70, height=15, font=("Times New Roman", 10),
                      yscrollcommand=scrollbar.set)
result_text.pack()

scrollbar.config(command=result_text.yview)

root.mainloop()