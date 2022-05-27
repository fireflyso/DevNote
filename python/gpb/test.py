import logical_port_pb2

ts = logical_port_pb2.telemetry_top_pb2.TelemetryStream()

f = open('/Users/liuxulu/workspace/telemetry/data.gpb', "rb")
ts.ParseFromString(f.read())
f.close()
print(ts)
