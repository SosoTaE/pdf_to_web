import poplib
import time
from email import parser
from email import policy
import email
from config import SERVER, ADDRESS, PORT, PASSWORD
from logger import logger
from pdf import read_pdf_and_save_as_pdf

# Server Configuration
pop_server = str(SERVER)
pop_port = int(PORT)  # or 995 for SSL
pop_username = str(ADDRESS)
pop_password = str(PASSWORD)


class EmailServer:
    def __init__(self, pop_server, pop_port, pop_username, pop_password):
        self.pop_server = pop_server
        self.pop_port = pop_port
        self.pop_username = pop_username
        self.pop_password = pop_password

    def _try_to_connect(self):
        logger.info(
            f"start connecting to server server:{self.pop_server}, port:{self.pop_port} username:{self.pop_username}")
        try:
            server = poplib.POP3_SSL(self.pop_server, self.pop_port)
            server.user(self.pop_username)
            server.pass_(self.pop_password)
            return server
        except Exception as e:
            raise ConnectionError(
                f"Could not connect to server: {e} server:{self.pop_server}, port:{self.pop_port} username:{self.pop_username}")

    def _try_reconnect_to_server(self):
        logger.info(
            f"start reconnecting to server server:{self.pop_server}, port:{self.pop_port} username:{self.pop_username}")
        for i in range(5):
            try:
                server = self._try_to_connect()
                return server
            except ConnectionError as e:
                logger.error(str(e))

        raise ConnectionError(
            f"Could not connect to server: {e} server:{self.pop_server}, port:{self.pop_port} username:{self.pop_username}")

    def _connect_to_server(self):
        # Connect and Authenticate
        try:
            server = self._try_to_connect()
            return server
        except Exception as e:
            logger.error(str(e))
            server = self._try_reconnect_to_server()


class EmailReceiver(EmailServer):
    def __init__(self, pop_server: str, pop_port: int, pop_username: str, pop_password: str):
        super().__init__(pop_server, int(pop_port), pop_username, pop_password)
        self.server = self._connect_to_server()

    def _email_listener(self):
        messages_quantity = self.server.list()[1]

        while True:
            print("looping")
            self.quit()
            self.server = self._connect_to_server()

            new_messages_quantity = len(self.server.list()[1])

            # Check if the count has increased
            if messages_quantity < new_messages_quantity:
                for i in range(messages_quantity + 1, new_messages_quantity + 1):
                    # Fetch the last email (use your own logic to get the email you want)
                    response, lines, octets = self.server.retr(i)
                    raw_email = b'\n'.join(lines)
                    # Parse the raw email into a convenient object
                    msg = email.message_from_bytes(raw_email, policy=policy.default)
                    # Loop through the email parts
                    for part in msg.iter_attachments():
                        # Only download attachments
                        if part.get_content_disposition() == 'attachment':
                            # Extract filename
                            filename = part.get_filename()
                            print(f"Found attachment: {filename}")

                            # Download and save the attachment
                            with open(filename, 'wb') as f:
                                f.write(part.get_payload(decode=True))

                            read_pdf_and_save_as_pdf(filename, filename)

                # Update the old message count
                messages_quantity = new_messages_quantity

            time.sleep(2)  # sleep for 30 seconds

    def listen_to_server(self, thread=False):
        pass

    def quit(self):
        self.server.quit()
