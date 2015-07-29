#!/usr/bin/env python2

import sys
from gtfs_realtime_pb2 import FeedMessage
from google.protobuf.text_format import MessageToString

with open(sys.argv[1], "rb") as f:
    feedmessage = FeedMessage()
    feedmessage.ParseFromString(f.read())

    with open(sys.argv[1] + '.txt', 'wb') as a:
        a.write(MessageToString(feedmessage))

