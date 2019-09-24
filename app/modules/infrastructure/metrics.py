import statsd
client = statsd.StatsClient('graphite', 8125)

def increase_approved_price_counter():
    client.incr("msrp.candidate.approved")

def increase_rejected_price_counter():
    client.incr("msrp.candidate.rejected")


def increase_received_price_counter():
    client.incr("msrp.candidate.received")
