
try:
    from Pi_switch.Pi_switch_main import run
except ModuleNotFoundError:
    from Pi_switch_main import run
# email[send, no of emails each day, hr to send]
run(debug=True, email=[True, 1, 20], taps=1)
