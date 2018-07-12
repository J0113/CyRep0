import re
import easygui


sentence = easygui.enterbox(title="CyRep0", msg="Name?")
name = re.sub(r"\s+", "", sentence, flags=re.UNICODE)


print(name)