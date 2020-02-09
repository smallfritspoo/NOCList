from time import sleep
from sys import exit
from requests import get, Response
from logging import getLogger, FileHandler, Formatter, DEBUG
from typing import Dict
from hashlib import sha256
from json import dumps


# Configure logging
logger = getLogger()
handler = FileHandler('noclist.log')
formatter = Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(DEBUG)
logger = getLogger(__name__)


class NOCList(object):
    """Class that manages interaction with the BADSEC vip user API.

    Args:
        url (str): url or ip (no port should be included) which the vip user api can be reached.
            Defaults to http://localhost Example: 127.0.0.1, http://localhost. Note: SSL support has not been tested.
        port (str): what port the vip user api can be reached on. defaults to 8888

    Attributes:
        url (str): location of the vip users api. defaults to http://127.0.0.1:8888
        user_list (str): json formatted string containing a json array listing the cip users retrieved from /users

    """
    def __init__(self, url: str = "http://127.0.0.1", port: str = "8888") -> None:
        self.url: str = f"http://{url}:{port}"
        self._auth_token: str = self._get_auth_token()  # some minor level of token protection
        self.user_list: str = dumps(self.get_user_list().split('\n'))

    def get_endpoint(self, endpoint: str = '/auth', retries: int = 3) -> Response:
        """Attempts to get the provided endpoint, creating checksum if required.

        Attempts to get the provided endpoint, creating the appropriate headers and checksum if required.
        Will by default, attempt to get provided enpoint up to 3 times in the event of connection errors, or a non
        200 http return code. A shallow backoff is configured on retries at a rate of ( attempt# + 1 * 10 seconds )

        Args:
            endpoint (str): the endpoint to request, should include leading forward slash /
            retries (int): number of times to try again when a connection error or non 200 status_code is returned

        Returns:
            Response: the requests response returned from our request.

        """
        # initialize sane variables
        retries: int = retries
        attempts: int = 0
        url: str = f"{self.url}{endpoint}"

        # We only need the request-checksum header when we are sending data to the /users endpoint.
        if endpoint == '/users':
            headers: Dict = {'X-Request-Checksum': self.compute_checksum(self._auth_token, endpoint)}
        else:
            headers: Dict = {}

        # setup basic retry logic and handle exceptions.
        for i in range(0, retries):
            try:
                logger.debug(f"fetching URL:{url}")
                response: Response = get(url=f"{url}", headers=headers)
            # catch all errors and retry
            except Exception as e:
                attempts += 1
                logger.error(f"Error during GET: {e} Attempt: {attempts}, retries: {retries}")
                sleep(attempts + 1 * 2)  # service is known to be fragile, apply a shallow backoff.
                continue
            else:
                # retry when status code is anything other than 200
                if response.status_code is not 200:
                    attempts += 1
                    logger.error(f"http status {response.status_code} is not 200. Attempt: {attempts}, retries: {retries}")
                    sleep(attempts + 1 * 2)  # service is known to be fragile, apply a shallow backoff.
                    continue
                else:
                    return response
        else:
            exit_message = f"Maximum retries attempted to {url}. Exiting"
            logger.error(exit_message)
            print(exit_message)
            exit(1)

    def _get_auth_token(self) -> str:
        """Retrieves the Authentication token from the vip users api

        Returns:
            str: the value of the Badsec-Authentication-Token return header.

        """
        logger.debug("Attempting to retrieve an authentication token")
        return self.get_endpoint().headers['Badsec-Authentication-Token']

    def get_user_list(self) -> str:
        """Retrieves the users list from the vip users api.

        Returns:
            str: The text from the response.

        """
        logger.debug("Attempting to retrieve the user list")
        return self.get_endpoint(endpoint='/users').text

    @staticmethod
    def compute_checksum(auth_token: str, endpoint: str) -> str:
        """Calculates the vip users api /users authentication checksum.

        Args:
            auth_token (str): the authentication token provided by the vip users apis /auth endpoint.
            endpoint (str): the endpoint to request, should include leading forward slash /

        Returns:
            str: the sha256 digest of the authentication_token and endpoint concatenated.

        """
        logger.debug("computing checksum")
        return sha256(f"{auth_token}{endpoint}".encode()).hexdigest()


def main():
    """Call the NOCList class and print the vip user list.

    Call the NOCList class, then print the NOCList.user_list attribute, followed by exiting with an exit code of 0
    """
    noc_list: NOCList = NOCList()
    print(noc_list.user_list)
    exit(0)


if __name__ == '__main__':
    main()


