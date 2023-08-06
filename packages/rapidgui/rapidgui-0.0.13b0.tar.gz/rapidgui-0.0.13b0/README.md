# rapidGui

No fuss rapid gui for quick and easy development

## how to use:

For quick setup, create instance of quickgui class and add member variables:

    q = rapidgui.quickGui()
    
    q.value = "eyooo?"
    q.variable = 42.0

    def clickMe():
        print("hello world")

    q.hello = clickMe

This will create a tkinter window that contains titles and controls to change these variables.

Currently only these types are supported:

> int, float, Decimal - will create a ttk.spinbox
>
> string - will create a ttk.entry
>
> function - will create a ttk.button

## change log

2/18/2023 - Fix: values were returned as int

2/18/2023 - added decimal support (precision is dependent on tkinter spinbox)
          - added safe fail on empty spinbox (doesn't update value)