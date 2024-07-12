from prometheus_client import CollectorRegistry, Gauge, generate_latest

# Instance wide stats
def instancestats(instance, attributes, instancename, registry):
    g = Gauge('instance_events_total', 'Total number of events on the MISP instance', labelnames=['instancename'], namespace='misp', registry=registry)
    g.labels(instancename=instancename).set(instance["stats"]["event_count"])
    g = Gauge('instance_attributes_total', 'Total number of attributes on the MISP instance', labelnames=['instancename'], namespace='misp', registry=registry)
    g.labels(instancename=instancename).set(instance["stats"]["attribute_count"])
    g = Gauge('instance_correlations_total', 'Total number of correlations on the MISP instance', labelnames=['instancename'], namespace='misp', registry=registry)
    g.labels(instancename=instancename).set(instance["stats"]["correlation_count"])

    g = Gauge('instance_attributes_per_type', 'Total number of attributes per type on the MISP instance', labelnames=['type', 'instancename'], namespace='misp', registry=registry)
    for type in attributes:
        g.labels(type=type, instancename=instancename).set(attributes[type])

# Organisation stats
def orgstats(data, instancename, registry):
    g = Gauge('org_events_total', 'Total number of events per org on the MISP instance', labelnames=['orgid', 'orgname', 'instancename'], namespace='misp', registry=registry)
    for org in data:
        try:
            data[org]["eventCount"]
        except:
            continue
        g.labels(orgid=data[org]["id"], orgname=data[org]["name"], instancename=instancename).set(data[org]["eventCount"])
    g = Gauge('org_attributes_total', 'Total number of attributes per org on the MISP instance', labelnames=['orgid', 'orgname', 'instancename'], namespace='misp', registry=registry)
    for org in data:
        try:
            data[org]["attributeCount"]
        except:
            continue
        g.labels(orgid=data[org]["id"], orgname=data[org]["name"], instancename=instancename).set(data[org]["attributeCount"])


# Diagnostic data
def diagnostics(data, instancename, registry):
    # Update status
    g = Gauge('up_to_date', 'MISP update status', labelnames=['instancename'], namespace='misp', registry=registry)
    if data["version"]["upToDate"] == "same":
        g.labels(instancename=instancename).set(1)
    else:
        g.labels(instancename=instancename).set(0)
    # Worker status
    g = Gauge('workers_healthy', 'Checks if workers are healthy', labelnames=['workertype', 'instancename'], namespace='misp', registry=registry)
    for worker_type in ["cache", "default", "email", "prio", "update"]:
        if data["workers"][worker_type]["ok"]:
            g.labels(workertype=worker_type, instancename=instancename).set(1)
        else:
            g.labels(workertype=worker_type, instancename=instancename).set(0)
   
# Tag stats
def tags(data, instancename, registry):
    g = Gauge("tlp_stats", 'Count of TLP tags on instance', labelnames=['tlp', 'instancename'], namespace='misp', registry=registry)
    for tlp in ["tlp:red", "tlp:amber+strict", "tlp:amber", "tlp:green", "tlp:white", "tlp:clear"]:
        if "tlp" in data.get("flatdata", {}):
            if tlp in  data['flatData']["tlp"]:
                metric = tlp.translate(str.maketrans({':': '_', '+': '_'}))
                g.labels(tlp=metric, instancename=instancename).set(data["flatData"]["tlp"][tlp]["size"])

def run(data, instancename):
    # Create a Prometheus registry
    registry = CollectorRegistry()

    # Prepare data and add to registry
    instancestats(data["instance"], data["attributes"], instancename, registry)
    orgstats(data["orgs"], instancename, registry)
    tags(data["tags"], instancename, registry)

    # Only convert diagnostics if it exists
    if "diag" in data:
        diagnostics(data["diag"], instancename, registry)

    # Convert the registry to a printable format and return
    metrics = generate_latest(registry).decode()
    return(metrics)
