from kivymd.uix.textfield import MDTextField

class RuleTextField(MDTextField):
    def insert_text(self, substring, from_undo=False):
        clear_substring = ""
        for ch in substring:
            if ch not in self.text:
                clear_substring = clear_substring + ch
        return super().insert_text(clear_substring, from_undo=from_undo)
