import requests

def run(mispurl, mispkey, mispssl, diag):

    data = {}
    
    # Create a requests session with our authkey in the header
    sess = requests.session()
    sess.headers.update({
        'Authorization': mispkey,
        'Accept': 'application/json'
                         })  
    
    # Fetch instance stats
    instance = sess.get(url=f"{mispurl}/users/statistics/data", verify=mispssl)
    data["instance"] = instance.json()

    # Fetch attribute stats
    attributes = sess.get(url=f"{mispurl}/attributes/attributeStatistics", verify=mispssl)
    data["attributes"] = attributes.json()

    # Fetch organistation stats
    orgs = sess.get(url=f"{mispurl}/users/statistics/orgs/scope:local", verify=mispssl)
    data["orgs"] = orgs.json()

    # Fetch diagnostic data if enabled
    if diag:
        diag = sess.get(url=f"{mispurl}/servers/serverSettings/diagnostics", verify=mispssl)
        data["diag"] = diag.json()
    
    # Fetch tag stats
    tags = sess.get(url=f"{mispurl}/users/statistics/tags", verify=mispssl)
    data["tags"] = tags.json()


    return data