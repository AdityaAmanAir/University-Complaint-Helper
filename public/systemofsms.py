import time

while True:
    with open('messages.log', 'r') as input_file:
        content = input_file.read()
    
    if content:
        reversed_content = """This is the reply from the Server!"""
        with open('messages2.log', 'w') as output_file:
            output_file.write("[2025-09-16 18:34:00] Processing message: "+ reversed_content)
        with open('messages.log', 'w') as input_file:
            input_file.write('')
        print("[2025-09-16 18:34:00] Processing message:", reversed_content)
    
    time.sleep(1)