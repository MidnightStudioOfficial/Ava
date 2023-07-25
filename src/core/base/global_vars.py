global BRAIN_mood, BRAIN_thought
global ENGINE_probability_matrix

global TOOLTIP_MESSAGES, STYLES_LIST
global VOICE_DEFAULT_SETTINGS

WAKE_WORD = "ava"
VOICE_DEFAULT_SETTINGS = {
    'voice_id': 2,
    'rate': 150,
    'volume': 0.7,
    'pitch': 110
}
TOOLTIP_MESSAGES = {
    "style_dropdown": "Customize your UI window with awesome built-in windows 11 header styles and themes. This is only for windows 11 (some themes may not work with windows 10).",
    "mail_button": "Notifications",
    "profile_button": "Your Profile"
}
STYLES_LIST = ["dark", "mica", "aero", "transparent", "acrylic", "win7",
          "inverse", "popup", "native", "optimised", "light"]


DEBUG_CHATBOT = None  # None
DEBUG_GUI = None
PEODUCTION = None


chatMode = 1

botChatTextBg = "#007cc7"
botChatText = "white"
userChatTextBg = "#4da8da"

chatBgColor = '#12232e'
background = '#203647'
textColor = 'white'
AITaskStatusLblBG = '#203647'
KCS_IMG = 1  # 0 for light, 1 for dark