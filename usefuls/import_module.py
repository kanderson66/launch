import modules.user_input as user_tools

question = 'Hit or stay?'
options = ['h', 's']

user_input = user_tools.validate_user_input(question, options)

if user_input == 's':
    print('Stay')
else:
    print('Hit')
