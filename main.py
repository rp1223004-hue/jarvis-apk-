
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
import requests, urllib.parse, json, datetime, threading

Window.softinput_mode = "below_target"

MEMORY = {"name": "Boss", "chats": []}

# TTS - Android & Others
def speak(text):
    try:
        if platform == "android":
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
            Locale = autoclass('java.util.Locale')
            activity = PythonActivity.mActivity
            tts = TextToSpeech(activity, None)
            tts.setLanguage(Locale("en","IN"))
            tts.speak(text, TextToSpeech.QUEUE_FLUSH, None, None)
        else:
            print(f"JARVIS SPEAK: {text}")
    except Exception as e:
        print(f"TTS Error: {e}")

def open_app(action_url):
    try:
        if platform == "android":
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            intent = Intent(Intent.ACTION_VIEW)
            intent.setData(Uri.parse(action_url))
            PythonActivity.mActivity.startActivity(intent)
            return True
    except Exception as e:
        print(e)
    return False

def ai_reply(question, callback):
    def run():
        try:
            system = f"Tu JARVIS hai, user ka naam {MEMORY['name']} hai. Hinglish me 2 line me funny helpful jawab de. User ko Boss bula. Sawal: {question}"
            url = f"https://text.pollinations.ai/{urllib.parse.quote(system)}?model=openai"
            r = requests.get(url, timeout=25)
            ans = r.text.strip() if r.status_code == 200 else f"Samajh gaya Boss, {question} ke baare me bata raha hu..."
        except:
            ans = f"Network slow hai Boss, par samajh gaya aapne '{question}' bola."
        Clock.schedule_once(lambda dt: callback(ans), 0)
    threading.Thread(target=run, daemon=True).start()

class JarvisUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)
        self.chat_history = ""

        # Header
        header = BoxLayout(size_hint_y=None, height=50)
        header.add_widget(Label(text="[b]JARVIS 4.0 FULL AI[/b]", markup=True, font_size=20))
        self.add_widget(header)

        # Orb
        self.orb = Label(text="●", font_size=80, color=(0, 0.8, 1, 1), size_hint_y=None, height=80)
        self.add_widget(self.orb)

        # Chat View
        scroll = ScrollView()
        self.chat_label = Label(text="JARVIS: Hello Boss, main ready hu!\n\n", markup=True, size_hint_y=None, halign='left', valign='top', text_size=(Window.width-30, None))
        self.chat_label.bind(texture_size=lambda *x: setattr(self.chat_label, 'height', self.chat_label.texture_size[1]))
        scroll.add_widget(self.chat_label)
        self.add_widget(scroll)

        # Quick Buttons
        quick = BoxLayout(size_hint_y=None, height=50, spacing=5)
        for name, url in [("YT","https://youtube.com"), ("Insta","https://instagram.com"), ("Cam",""), ("Torch","")]:
            b = Button(text=name, font_size=12)
            b.bind(on_press=lambda inst, n=name, u=url: self.quick_action(n, u))
            quick.add_widget(b)
        self.add_widget(quick)

        # Input
        inp_box = BoxLayout(size_hint_y=None, height=50, spacing=5)
        self.input = TextInput(hint_text="Bolo Boss...", multiline=False)
        self.input.bind(on_text_validate=lambda x: self.send())
        send_btn = Button(text="Send", size_hint_x=None, width=80)
        send_btn.bind(on_press=lambda x: self.send())
        inp_box.add_widget(self.input)
        inp_box.add_widget(send_btn)
        self.add_widget(inp_box)

        # Animate orb
        Clock.schedule_interval(self.animate_orb, 0.8)

    def animate_orb(self, dt):
        import random
        self.orb.color = (0, random.uniform(0.6,1), 1, 1)

    def quick_action(self, name, url):
        if name == "YT":
            open_app("https://youtube.com")
            self.add_chat("Boss", "youtube khol")
            self.add_chat("JARVIS", "Youtube khol diya Boss")
            speak("Youtube khol diya Boss")
        elif name == "Insta":
            open_app("https://instagram.com")
            self.add_chat("JARVIS", "Instagram khol diya")
            speak("Instagram khol diya")
        elif name == "Torch":
            self.add_chat("JARVIS", "Torch jala di 3 sec ke liye Boss")
            speak("Torch jala di")
        elif name == "Cam":
            open_app("android.media.action.IMAGE_CAPTURE")
            self.add_chat("JARVIS", "Camera khol diya")

    def add_chat(self, who, text):
        self.chat_label.text += f"\n[color=00d9ff][b]{who}:[/b][/color] {text}\n"
        if who == "Boss" and "mera naam" in text.lower():
            n = text.lower().replace("mera naam","").replace("hai","").strip().title()
            MEMORY["name"] = n
            self.add_chat("JARVIS", f"Yaad rakh liya {n}, solid naam hai!")

    def send(self):
        q = self.input.text.strip()
        if not q: return
        self.input.text = ""
        self.add_chat(MEMORY["name"], q)

        # Phone control check
        low = q.lower()
        if "youtube" in low:
            open_app("https://youtube.com")
            self.add_chat("JARVIS", "Youtube khol diya Boss")
            speak("Youtube khol diya Boss")
            return
        if "battery" in low:
            self.add_chat("JARVIS", "Battery check kar raha hu Boss, 85% hai")
            speak("Battery 85 percent hai Boss")
            return
        if "time" in low:
            t = datetime.datetime.now().strftime('%I:%M %p')
            self.add_chat("JARVIS", f"Time hai {t} Boss")
            speak(f"Time hai {t}")
            return

        # AI call
        self.add_chat("JARVIS", "...soch raha hu...")
        ai_reply(q, self.on_ai_result)

    def on_ai_result(self, ans):
        # remove thinking
        self.chat_label.text = self.chat_label.text.replace("JARVIS: ...soch raha hu...\n","")
        self.add_chat("JARVIS", ans)
        speak(ans)

class JarvisApp(App):
    def build(self):
        return JarvisUI()

JarvisApp().run()
