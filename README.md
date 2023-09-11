# MISP Metrics Exporter

This project provides a way to export metrics from MISP in Prometheus format.

Works using the Node Exporter textfile collector.

## Collected metrics

**Instance metrics:**

- Total events
- Total attributes
- Total correlations
- Total attributes per attribute type
- Total events per organisation
- Total events per TLP

**Diagnostics metrics:**

- Worker health
- Update status

## Installation and usage

This script can be run on any server with MISP API access, including on the MISP instance itself.

Examples are written for Ubuntu Server 20.04.

**Important:** If you enable diagnostics collection in config.ini, the API key used MUST be from an admin user with write permission.

## Prerequisites

MISP API access.

[Node Exporter](https://github.com/prometheus/node_exporter) running and collecting textfiles from /var/prometheus/.

TLP taxonomy enabled and tags active

## Installation steps

```bash
# All commands assume that you are root.
apt install python3 virtualenv git moreutils cron
cd /opt
git clone https://github.com/Truesec/misp-metricsexporter.git
cd misp-metricsexporter
virtualenv .venv
chmod -R 600 /opt/misp-metricsexporter
source .venv/bin/activate
python3 -m pip install -r requirements.txt

# This assumes that Node Exporter is scraping /var/prometheus/.
touch /var/prometheus/misp-metrics.prom
chmod 644 /var/prometheus/misp-metrics.prom
```

### Configuration

Edit config.ini with your preferred text editor, all values need to be set, use the comments in config.ini as reference.

### Testing

Run the following to test that everything works properly.

```bash
cd /opt/misp-metricsexporter/
source .venv/bin/activate
python3 misp_exporter.py
```

This should print the metrics collected to stdout.

If you get an error related to TLP, enable the TLP taxonomy and add all tags.

### Scheduling

Edit your crontab using ```crontab -e``` and add a job:

```bash
*/5 * * * * cd /opt/misp-metricsexporter/ && /opt/misp-metricsexporter/.venv/bin/python3 /opt/misp-metricsexporter/misp_exporter.py | sponge /var/prometheus/misp-metrics.prom
```

Adjust the schedule as needed.

## Exported metrics example

``` text
# HELP misp_instance_events_total Total number of events on the MISP instance
# TYPE misp_instance_events_total gauge
misp_instance_events_total{instancename="Example MISP"} 10000.0
# HELP misp_instance_attributes_total Total number of attributes on the MISP instance
# TYPE misp_instance_attributes_total gauge
misp_instance_attributes_total{instancename="Example MISP"} 10000.0
# HELP misp_instance_correlations_total Total number of correlations on the MISP instance
# TYPE misp_instance_correlations_total gauge
misp_instance_correlations_total{instancename="Example MISP"} 10000.0
# HELP misp_instance_attributes_per_type Total number of attributes per type on the MISP instance
# TYPE misp_instance_attributes_per_type gauge
misp_instance_attributes_per_type{instancename="Example MISP",type="AS"} 20.0
misp_instance_attributes_per_type{instancename="Example MISP",type="attachment"} 20.0
misp_instance_attributes_per_type{instancename="Example MISP",type="authentihash"} 20.0
misp_instance_attributes_per_type{instancename="Example MISP",type="bank-account-nr"} 20.0
misp_instance_attributes_per_type{instancename="Example MISP",type="bic"} 20.0
misp_instance_attributes_per_type{instancename="Example MISP",type="boolean"} 20.0
misp_instance_attributes_per_type{instancename="Example MISP",type="btc"} 20.0
misp_instance_attributes_per_type{instancename="Example MISP",type="campaign-id"} 20.0
misp_instance_attributes_per_type{instancename="Example MISP",type="campaign-name"} 20.0
misp_instance_attributes_per_type{instancename="Example MISP",type="comment"} 20.0
----- snip -----
# HELP misp_org_events_total Total number of events per org on the MISP instance
# TYPE misp_org_events_total gauge
misp_org_events_total{instancename="Example MISP",orgid="1",orgname="Example_Org_1"} 5000.0
misp_org_events_total{instancename="Example MISP",orgid="83",orgname="Example_Org_2"} 5000.0
misp_org_events_total{instancename="Example MISP",orgid="84",orgname="Example_Org_3"} 5000.0
# HELP misp_org_attributes_total Total number of attributes per org on the MISP instance
# TYPE misp_org_attributes_total gauge
misp_org_attributes_total{instancename="Example MISP",orgid="1",orgname="Example_Org_1"} 5000.0
misp_org_attributes_total{instancename="Example MISP",orgid="83",orgname="Example_Org_2"} 5000.0
misp_org_attributes_total{instancename="Example MISP",orgid="84",orgname="Example_Org_3"} 5000.0
# HELP misp_tlp_stats Count of TLP tags on instance
# TYPE misp_tlp_stats gauge
misp_tlp_stats{instancename="Example MISP",tlp="tlp_red"} 10.0
misp_tlp_stats{instancename="Example MISP",tlp="tlp_amber_strict"} 10.0
misp_tlp_stats{instancename="Example MISP",tlp="tlp_amber"} 10.0
misp_tlp_stats{instancename="Example MISP",tlp="tlp_green"} 10.0
misp_tlp_stats{instancename="Example MISP",tlp="tlp_white"} 10.0
misp_tlp_stats{instancename="Example MISP",tlp="tlp_clear"} 10.0
# HELP misp_up_to_date MISP update status
# TYPE misp_up_to_date gauge
misp_up_to_date{instancename="Example MISP"} 1.0
# HELP misp_workers_healthy Checks if workers are healthy
# TYPE misp_workers_healthy gauge
misp_workers_healthy{instancename="Example MISP",workertype="cache"} 1.0
misp_workers_healthy{instancename="Example MISP",workertype="default"} 1.0
misp_workers_healthy{instancename="Example MISP",workertype="email"} 1.0
misp_workers_healthy{instancename="Example MISP",workertype="prio"} 1.0
misp_workers_healthy{instancename="Example MISP",workertype="update"} 1.0
```
