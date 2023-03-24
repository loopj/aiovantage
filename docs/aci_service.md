# Vantage InFusion ACI (Application Communication Interface) Service

The ACI service is an XML-based RPC service that Design Center uses to communicate with
Vantage InFusion Controllers. There are a number of interfaces exposed, each with one
or more methods.

The service is exposed on port 2010 (SSL) by default, and on port 2001 (non-SSL) if this
port has been opened by the firewall on the controller.

The service is discoverable via mDNS as `_aci._tcp.local` and/or `_secure_aci._tcp.local`.


## Authentication

If authentication is enabled on the controller, you must authenticate before making further
requests by calling the `ILogin.Login(username, password)` RPC.


## Making Requests

Vantage RPC requests have the following structure:

```xml        
<IInterface>
    <Method>
        <call>
            <param1>...</param1>
            <param2>...</param2>
        </call>
    </Method>
</IInterface>
```

The server will then respond with

```xml
<IInterface>
    <Method>
        <return>
            ...
        </return>
    </Method>
</IInterface>
```


## Interfaces

The following is a list of known interfaces and methods available on a Vantage InFusion Controller's ACI service.


### Introspection

```python
IIntrospection.GetSysInfo()
IIntrospection.GetVersion()
IIntrospection.GetInterfaces()
```


### Configuration

```python
IConfiguration.Clear()
IConfiguration.GetObject(VID: int)
IConfiguration.SetObject(?)
IConfiguration.GetTime() -> str
IConfiguration.SetTime(str)
IConfiguration.GetNTPServer() -> str
IConfiguration.SetNTPServer(str)
IConfiguration.GetBuffers()
IConfiguration.OpenFilter(Objects: ?, XPath: str) -> int
IConfiguration.GetFilterResults(Count: int, WholeObject: bool, hFilter: int)
IConfiguration.CloseFilter(int)
IConfiguration.GetZeroCross()
IConfiguration.SetZeroCross(MaxAdjust: int, MaxError: int)
IConfiguration.GetSMTP()
IConfiguration.SetSMTP(Server: str, Username: str, Password: str)
IConfiguration.GetTimeZone() -> str
IConfiguration.SetTimeZone(str)
IConfiguration.GetLocation() -> str
IConfiguration.SetLocation(str)
IConfiguration.GetLocale() -> str
IConfiguration.SetLocale(?) -> bool
IConfiguration.GetObjectInit(str)
IConfiguration.SetObjectInit(Type: str, Init: ?)
IConfiguration.Save()
IConfiguration.GetAuthenticationAccess()
IConfiguration.SetAuthenticationAccess(str)
IConfiguration.GetIpAddressExceptions()
IConfiguration.SetIpAddressExceptions(?)
```


### Backup

Backup or download files to the controller's SD card, eg. Design Center xml files.
The latest/current Design Center XML file is backed up to `Backup\Project.dc`.

```python
IBackup.IsMounted() -> bool
IBackup.GetFile(str)
IBackup.PutFile(Name: str, Controllers, File)
```


### Diagnostic

```python
IDiagnostic.GetSystemComplexity()
IDiagnostic.GetStationBuses()
IDiagnostic.SetStationConfigMode(Bus: int, Mode: bool)
IDiagnostic.GetStations(int)
IDiagnostic.GetEnhancedLogConfig()
IDiagnostic.SetEnhancedLogConfig(Aggregator: {Enabled: bool, Status: int}, Logging: {Status: bool})
IDiagnostic.GetFirewallConfiguration()
IDiagnostic.SetFirewallConfiguration(OpenPorts: {TCP: List[int], UDP: List[int], ICMP: bool)
IDiagnostic.ResetEventLog()
IDiagnostic.GetModules(int)
```


## Register Interface

```
IRegister.RegisterObject(?)
IRegister.RegisterInterface(?)
IRegister.RegisterLocale(?)
IRegister.UnregisterLocale(?)
```