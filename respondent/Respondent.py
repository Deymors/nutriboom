from .Response import Response


class Respondent:
    @staticmethod
    def get_num_stages():
        return 10

    def __init__(self, current_question=0, number_surveyed=0, number_sufficient=0, number_deficient=0):
        self.q = current_question
        self.surveyed = number_surveyed
        self.sufficient = number_sufficient
        self.deficient = number_deficient
        return

    def recordAnswer(self, message_received):
        stage = self.q
        if stage < 0 or stage >= Respondent.get_num_stages() - 1:
            stage = 0
        stage += 1
        message = Response(stage, True, response[stage], False)
        ###secret keys
        if 'STAGE' in message_received:
            message.is_message_valid = True
            message.contactable = True
            message.content = str(stage)
            stage -= 1
        elif 'CLEAR' in message_received:
            message.is_message_valid = True
            message.contactable = True
            stage = 0
            message.content = 'Welcome to Nutriboom! Here we will ask you about your observations in regards to the nutrient consumption in the region. Send BEGIN to begin the survey or SMSINFO to find out more'
        elif 'CEASE' in message_received:
            message.is_message_valid = True
            message.contactable = False
            stage = 0
            message.content = 'You will no longer receive any messages, unless you send CLEAR'
        elif 'SKIP' in message_received:
            stage -= 1
            message.is_message_valid = True
            stage = min(stage + 1, Respondent.get_num_stages() - 1)
            message.content = response[stage]
            message.is_message_valid = True
        elif 'BACK' in message_received:
            stage -= 1
            message.is_message_valid = True
            if message.stage == 1:
                message.content = 'You can\'t go back at this stage'
            else:
                message.content = response[stage - 2]
                stage -= 1
        elif message.stage == 1:
            message.is_message_valid = True
            if 'BEGIN' in message_received:
                stage = 1
            elif 'SMSINFO' in message_received:
                stage -= 1
                message.content = 'BEGIN - start survey\n CEASE - stop receiving messages \n CLEAR - remove all progress \n BACK - go one step back \n SKIP - skip the question'
            else:
                stage -= 1
                message.content = 'To start the survey, please send BEGIN. To learn more about other commands send SMSINFO'
        elif 1 < stage < 9 and not stage == 3 and not stage == 4 and not message_received.isdigit():
            message.is_message_valid = False
        elif message.stage == 2:
            if 0 < int(message_received) < 5:
                message.is_message_valid = True
        elif stage == 3:
            if len(message_received) > 1:
                message.is_message_valid = True
        elif stage == 4:
            if len(message_received) > 1:
                message.is_message_valid = True
        elif stage == 5:
            if 0 < int(message_received) < 10001:
                message.is_message_valid = True
                self.surveyed = int(message_received)
        elif stage == 6:
            if 0 < int(message_received) < 3:
                message.is_message_valid = True
        elif stage == 7:
            if -1 < int(message_received) <= self.surveyed:
                message.is_message_valid = True
                self.sufficient = int(message_received)
        elif stage == 8:
            if 0 < int(message_received) <= self.surveyed - self.sufficient:
                message.is_message_valid = True
                self.deficient = int(message_received)
        elif stage == 9 or stage == 10:
            message.is_message_valid = True
        else:
            message.content = 'Error Occurred'
        if not message.is_message_valid:
            message.content = 'Your input is invalid. Please, try again.'
            stage -= 1
        message.stage = stage
        message.content += '(your message: ' + message_received + ')'
        return message


q0 = "Welcome to Nutriboom! Here we will ask you about your observations in regards to the nutrient consumption in the region."

q1 = "Enter the number corresponding to the nutrient you studied.\n"
q1 += "1. Vitamin A \n2. Vitamin B12\n3. Iron\n4. Zinc"

q2 = "Enter the country in which you collected this data."

q3 = "Enter the city in which you collected this data."

q4 = "Enter a number between 1 and 10000 for the number of people/households you surveyed."

q5 = "Enter the number corresponding to the type of data you collected.\n"
q5 += "1. Door to door survey\n2. Individuals at health centers"

q6 = "Enter the number of households/people who likely have sufficient levels of the nutrient you surveyed"

q7 = "Enter the number of households/people who are likely deficient in the nutrient you surveyed"

q8 = "Confirm that you have finished the survey with any message or use the commands (BACK, CLEAR)"

q9 = "Thank you for completing the survey!"
response = [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9]
