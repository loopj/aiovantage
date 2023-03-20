import asyncio
import logging
import ssl

# R:ERROR:21 - Login required
# R:ERROR:23 - Login failed

class Vantage:
    """Control a Vantage InFusion Controller via TCP API."""
    def __init__(self, host, username = None, password = None,
                 use_ssl = True, file_port = None, command_port = None):
        self._host = host
        self._username = username
        self._password = password
        self._use_ssl = use_ssl
        self._tasks = []
        self._logger = logging.getLogger("aiovantage")

        # "File" port (_aci._tcp.local or _secure_aci._tcp.local in mDNS)
        if file_port is None:
            self._file_port = 2010 if use_ssl else 2001
        
        # "Command" port (_hc._tcp.local or _secure_hc._tcp.local in mDNS)
        if command_port is None:
            self._command_port = 3010 if use_ssl else 3001
        
        if use_ssl:
            self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)

    @property
    def host(self) -> str: 
        """Return the hostname of the controller."""
        return self._host

    async def initialize(self):
        # TODO: Fetch full state
        # TODO: Initialize event stream


        # Open a connection to the controller
        self._reader, self._writer = await asyncio.open_connection(
            self._host, self._command_port, ssl=self._ssl_context
        )

        # Login if we have a username and password
        if self._username is not None and self._password is not None:
            response = await self.send_command_sync(f"LOGIN {self._username} {self._password}")
            # TODO: Centralize error parsing / exceptions
            if response.startswith("R:ERROR:23"):
                raise Exception("Login failed")
            else:
                self._logger.info("Login successful")

        # Start a background task to monitor incoming messages
        self._tasks.append(asyncio.create_task(self.__event_reader()))
    
    async def close(self):
        pass

    async def send_command(self, command):
        self._writer.write((command + "\r\n").encode())
        await self._writer.drain()

    async def send_command_sync(self, command):
        await self.send_command(command)
        reply = await self._reader.readline()
        return reply.decode().rstrip()

    async def __event_reader(self):
        # Statuses are: TEMP, CURRENT, POWER, LOAD, 
        while True:
            message = await self._reader.readline()
            print(message.decode().rstrip())
    
    async def __aenter__(self):
        """Return Context manager."""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_t, exc_v, exc_tb):
        """Exit context manager."""
        await self.close()



import base64
import xml.etree.ElementTree as ET

class SchemaClient:
    LOGIN_CMD = """
        <ILogin><Login><call>
            <User>{username}</User>
            <Password>{password}</Password>
        </call></Login></ILogin>
        """
    
    GETFILE_CMD = """
        <IBackup><GetFile>
            <call>{filename}</call>
        </GetFile></IBackup>
        """

    def __init__(self, host, username=None, password=None, use_ssl=True, port=None):
        self._host = host
        self._username = username
        self._password = password
        self._use_ssl = use_ssl
        self._logger = logging.getLogger("aiovantage")

        if port is None:
            self._port = 2010 if use_ssl else 2001

        if use_ssl:
            self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    
    
    async def _send(self, command):
        self._writer.write(command.encode())
        await self._writer.drain()

    async def _login(self):
        # Send login command
        await self._send(self.LOGIN_CMD.format(username=self._username, password=self._password))
    
        # Fetch the response
        data = await self._reader.readuntil(b"</ILogin>")
        response = ET.fromstring(data.decode())

        # Validate the response
        el = response.find("Login/return")
        if el is None:
            raise Exception("Login failed (unknown response)")
        elif el.text == "false":
            raise Exception("Login failed")
        else:
            self._logger.info("Login successful")

    async def _fetch_project_xml(self):
        await self._send(self.GETFILE_CMD.format(filename="Backup\\Project.dc"))

        # Fetch the response
        data = await self._reader.readuntil(b"</IBackup>")
        response = ET.fromstring(data.decode(), parser=ET.XMLParser(target=ET.TreeBuilder(insert_pis=True)))

        # Validate the response
        el = response.find("GetFile/return/Result")
        if el is None:
            raise Exception("Fetching XML file failed (unknown response)")
        elif el.text == "false":
            raise Exception("Fetching XML file failed")
        else:
            self._logger.info("Fetching XML file successful")
        
        # Extract and parse the embedded XML file
        el = response.find("GetFile/return/Result")
        el = next(response.iter(tag=ET.ProcessingInstruction))
        b64 = el.text.split()[2][1:]

        return base64.b64decode(b64).decode()

    async def initialize(self):
        # TODO: Cache xml file

        # Connect
        self._reader, self._writer = await asyncio.open_connection(self._host, self._port, limit=10*1024*1024, ssl=self._ssl_context)

        # Authenticate (if required)
        if self._username is not None and self._password is not None:
            await self._login()
        
        # Fetch the project XML backup
        project_xml = await self._fetch_project_xml()
        
        # Parse the XML file
        root = ET.fromstring(project_xml)
        objects = root.find("Objects")

        # Areas
        loads = objects.findall("Object/Area[@VID]")
        print("\n\n[Area] ")
        for load in loads:
            name = load.find("Name").text
            print(name, end=", ")

        # Loads
        loads = objects.findall("Object/Load[@VID]")
        print("\n\n[Load] ")
        for load in loads:
            name = load.find("Name").text
            print(name, end=", ")
        
        # DryContacts
        loads = objects.findall("Object/DryContact[@VID]")
        print("\n\n[DryContact] ")
        for load in loads:
            name = load.find("Name").text
            print(name, end=", ")'
            '