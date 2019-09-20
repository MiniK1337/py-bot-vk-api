import json

class Keyboard:
    def __init__(self):
        self.colors = ('default', 'primary', 'positive', 'negative')
        self.one_time = None
        self.buttons = []

    def __call__(self, buttons, one_time = False):
        self.one_time = one_time
        return self._check_buttons(buttons)
    
    def _check_buttons(self, buttons):
        if len(buttons) > 10:
            raise ValueError("The number of rows exceeds the limit (max rows: 10)")

        for row_num, row in enumerate(buttons, 1):
            if len(row) > 4:
                raise ValueError(f"The number of buttons in the same row exceeds the limit (row: {row_num})")

            for btn_num, btn in enumerate(row, 1):
                if 'label' not in btn:
                    raise ValueError(f"The field must not be empty: 'label' (row: {row_num}, button: {btn_num})") 
                if 'color' not in btn:
                    raise ValueError(f"The field must not be empty: 'color' (row: {row_num}, button: {btn_num})") 

                if btn['color'] not in self.colors:
                    raise ValueError("Wrong button color! Available colors: {}".format(", ".join(self.colors)))

        return self._dump_keyboard(buttons)

    def _dump_keyboard(self, buttons):
        btn_num = 1
        for row in buttons:
            formatted_row = []
            for btn in row:
                btn_template = dict(
                    action = dict(
                        type = "text",
                        payload = "{\"button\": "f"{btn_num}""}",
                        label = btn['label']
                    ),
                    color = btn['color']
                )
                formatted_row.append(btn_template)
                btn_num += 1
                print(btn_num)
            self.buttons.append(formatted_row)

        return json.dumps(dict(
            one_time = self.one_time,
            buttons = self.buttons,
        ), ensure_ascii = False)
