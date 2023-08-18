from googleapiclient.errors import HttpError
from simplegmail import Gmail


class Mail:
    def __init__(self, params):
        self.count_msg = 0
        self.flag = True
        self.params = params

    def send_message(self):
        try:
            # Attempt to send the message using simplegmail
            if Gmail().send_message(**self.params):
                self.count_msg += 1

            # If 100 messages have been sent, trash them to avoid clutter
            if self.count_msg >= 100:
                messages = Gmail().get_sent_messages()
                for message in messages:
                    message.trash()
                self.count_msg = 0
        except HttpError:
            self.flag = False

        # Print the count of sent messages for monitoring purposes
        print(self.count_msg)
        return self.flag
