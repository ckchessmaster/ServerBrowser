from datetime import datetime, timezone

class FakeServer:
  def __init__(self, ip, port, row_key='123', region='eastus', lastHeartbeatTime=None):
    self.ip = ip
    self.port = port
    self.row_key = row_key
    self.region = region
    self.lastHeartbeatTime = lastHeartbeatTime if lastHeartbeatTime else datetime.now(timezone.utc)