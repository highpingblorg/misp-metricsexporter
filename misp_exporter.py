import urllib3, os, configparser
from modules import convert_data, fetch_data

cwd = os.getcwd()
config_path = f"{cwd}/config.ini"

if not os.path.isfile(config_path):
    raise Exception(f"Config file not found or accessible, make sure config.ini exists at {config_path}")

try:
    config = configparser.ConfigParser()
    config.read(config_path)

    misp_url = config["connection"]["misp_url"]
    misp_key = config["connection"]["misp_key"]
    misp_ssl = eval(config["connection"]["misp_ssl"])

    instancename = config["preferences"]["instance_name"]
    diagnostics = eval(config["preferences"]["include_diagnostics"])
except:
    raise Exception("Failure reading config file, make sure it is configured correctly")

if not misp_ssl:
    # Disable warnings to stdout if not validating SSL
    urllib3.disable_warnings()

if __name__ == "__main__":
    data = fetch_data.run(mispurl=misp_url, mispkey=misp_key, mispssl=misp_ssl, diag=diagnostics)
    metrics = convert_data.run(data=data, instancename=instancename)
    print(metrics, end='')
