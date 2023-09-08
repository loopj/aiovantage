# Vantage InFusion Host Command Service

The Host Command service is a text-based service that allows interaction with devices controlled by a Vantage InFusion Controller.

Among other things, this service allows you to change the state of devices (eg. turn on/off a light) as well as subscribe to status changes for devices.

The service is exposed on port 3010 (SSL) by default, and on port 3001 (non-SSL) if this port has been opened by the firewall on the controller.

The service is discoverable via mDNS as `_hc._tcp.local` and/or `_secure_hc._tcp.local`.

## Authentication

If authentication is enabled on the controller, you must authenticate before making further requests by calling `LOGIN username, password`.

## Making Requests

Requests can be made in plain text. The following requests are available:

```markdown
BTN <button vid>
BTNPRESS <button vid>
BTNRELEASE <button vid>
LOAD <load vid> <level (0-100)>
RAMPLOAD <load vid> <level (0-100)> <seconds>
GETLOAD <load vid>
LED <button vid> <color1 (0-255)> <color2> <color3> <offcolor1> <offcolor2 (0-255)> <offcolor3> <blinkrate (FAST/MEDIUM/SLOW/VERYSLOW/OFF)>
GETLED <button vid>
TASK <task vid> <eventType (PRESS/RELEASE/HOLD/TIMER/DATA/POSITION/INRANGE/OUTOFRANGE/TEMPERATURE/DAYMODE/FANMODE/OPERATIONMODE/CONNECT/DISCONNECT/BOOT/LEARN/CANCEL/NONE)>
GETTASK <task vid>
STATUS <type (LOAD/LED/BTN/TASK/TEMP/THERMFAN/THERMOP/THERMDAY/SLIDER/TEXT/VARIABLE/BLIND/PAGE/LEDSTATE/IMAGE/WIND/LIGHT/CURRENT/POWER/ALL/NONE)>
GETTEMP <temperature vid>
THERMTEMP <thermostat vid> <type (COOL/HEAT)> <temperature>
GETTHERMTEMP <thermostat vid> <type (INDOOR/OUTDOOR/COOL/HEAT)>
THERMFAN <thermostat vid> <fan (ON/AUTO)>
GETTHERMFAN <thermostat vid>
THERMOP <thermostat vid> <op mode (OFF/COOL/HEAT/AUTO)>
GETTHERMOP <thermostat vid>
THERMDAY <thermostat vid> <day mode (DAY/NIGHT)>
GETTHERMDAY <thermostat vid>
SLIDER <slider vid> <level (0-100)>
GETSLIDER <slider vid>
TEXT <text vid> <text>
GETTEXT <text vid>
VARIABLE <variable vid> <value "text"/number>
GETVARIABLE <variable vid>
GETFIELD <Obj vid> <field name>
GETSENSOR <Obj vid>
GETLIGHT <Obj vid>
GETWIND <Obj vid>
GETCURRENT <Obj vid>
GETPOWER <Obj vid>
BLIND <Obj vid> <control (OPEN/CLOSE/STOP/POS)> <position>
GETBLIND <Obj vid>
INVOKE <Obj vid> <interface.method> <parameter> ...
!LOAD <type (M/S)> <controller> <bus> <device> <load/count> <level (0-100)>
!RAMPLOAD <type (M/S)> <controller> <bus> <device> <load/count> <level (0-100)> <seconds>
!GETLOAD <type (M/S)> <controller> <bus> <device> <load/count>
ADDSTATUS <vid> ...
DELSTATUS [<vid> ...]
LISTSTATUS
ECHO <text>
VERSION
GETCOUNT
DELIMITER <Hex Byte 1> [<Hex Byte 2>]
LOG  [<controller> ... ] [CONTROLLER] [TYPE] [TIME] [SOURCE] [FULL]   [DEBUG] [DUMP] [INFO] [WARNING] [ERROR] [FATAL] [TASK] [DEVICE] [QUERY] [PROF]
DUMP <controller> [CONTROLLER] [TYPE] [TIME] [SOURCE] [FULL]   [DEBUG] [DUMP] [INFO] [WARNING] [ERROR] [FATAL] [TASK] [DEVICE] [QUERY] [PROF]
ELSIZE [<controller>] <type (STATUS/STATUSEX/AUTOMATION/SYSTEM/EVENT/MODCOM/STATCOM)> <size>
ELGETSIZE [<controller>] <type (STATUS/STATUSEX/AUTOMATION/SYSTEM/EVENT/MODCOM/STATCOM)>
ELAGG [<controller>] <state (ON/OFF)>
ELENABLE [<controller>] <type (STATUS/STATUSEX/AUTOMATION/SYSTEM/EVENT/MODCOM/STATCOM)> <state (ON/OFF)>
ELDUMP <type (STATUS/STATUSEX/AUTOMATION/SYSTEM/EVENT/MODCOM/STATCOM)> [PERCENT] [CONTROLLER] [TIME] [TYPE] [HEX] [FULL] [<filter>]
ELLOG <type (STATUS/STATUSEX/AUTOMATION/SYSTEM/EVENT/MODCOM/STATCOM)> [PERCENT] [CONTROLLER] [TIME] [TYPE] [HEX] [FULL] <state (ON/OFF) [<filter>]
LOGIN <user name> <password>
```
