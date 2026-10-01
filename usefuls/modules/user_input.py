def validate_user_input(question, options):
    user_input = input(f'\n{question} [{'/'.join(options)}] ')

    while user_input not in options:
        print('Invalid input.')
        user_input = input(f'\n{question} [{'/'.join(options)}] ')
    return user_input


# if validate_user_input('Hit or stay?', ['h', 's']) == 's':
#     print('Stay')
# else:
#     print('Hit')

