#!/usr/bin/env python2

import sys
from gtfs_realtime_pb2 import FeedMessage
from google.protobuf.text_format import MessageToString

with open(sys.argv[1], "rb") as f:
    feedmessage = FeedMessage()
    feedmessage.ParseFromString(f.read())
    trip_updates = FeedMessage()
    vehicles = FeedMessage()
    alerts = FeedMessage()

    trip_updates.header.CopyFrom(feedmessage.header)
    vehicles.header.CopyFrom(feedmessage.header)
    alerts.header.CopyFrom(feedmessage.header)

    for feedentity in feedmessage.entity:
        if feedentity.HasField('is_deleted') and feedentity.is_deleted == True:
            # For incremental feeds we don't know where the deleted entity
            # refers to, we must propagate it across all feeds.
            e = trip_updates.entity.add()
            e.CopyFrom(feedentity)
            e = vehicles.entity.add()
            e.CopyFrom(feedentity)
            e = alerts.entity.add()
            e.CopyFrom(feedentity)

        elif feedentity.HasField('trip_update'):
            e = trip_updates.entity.add()
            e.CopyFrom(feedentity)

        elif feedentity.HasField('vehicle'):
            e = vehicles.entity.add()
            e.CopyFrom(feedentity)

        elif feedentity.HasField('alert'):
            e = alerts.entity.add()
            e.CopyFrom(feedentity)


    with open('trip_updates.pb', 'wb') as t:
        t.write(trip_updates.SerializeToString())

    with open('vehicles.pb', 'wb') as v:
        v.write(vehicles.SerializeToString())

    with open('alerts.pb', 'wb') as a:
        a.write(alerts.SerializeToString())

