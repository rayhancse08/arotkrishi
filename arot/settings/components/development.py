# Always use IPython for shell_plus
# SHELL_PLUS = "ipython"
SHELL_PLUS_PRINT_SQL = True
SHELL_PLUS_PRE_IMPORTS = [
    ('django.forms.models', ('model_to_dict',)),
]