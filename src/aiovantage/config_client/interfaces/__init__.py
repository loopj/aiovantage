"""Interface definitions for ACI service calls.

These interfaces define the expected format of the XML requests and responses
for a subset of ACI service calls.

RPC requests have the following structure:

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
"""
