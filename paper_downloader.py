import requests
import json
import sys
import hashlib
import logging

# REFER TO https://fill.papermc.io/swagger-ui/index.html#/ FOR API FORMAT

headers = {
    'User-Agent': 'python-paper-script/1.0.0',
}


def download(version):
    builds = requests.get(f"https://fill.papermc.io/v3/projects/paper/versions/{version}/builds", headers=headers)
    if builds.status_code == 200:
        obj = json.loads(builds.content)

        for i in obj:
            if i["channel"] == "STABLE":
                jar = requests.get(i["downloads"]["server:default"]["url"], headers=headers)
                result = hashlib.sha256(jar.content).hexdigest()

                if result == i["downloads"]["server:default"]["checksums"]["sha256"]:
                    with open(i["downloads"]["server:default"]["name"], "wb") as f:
                        f.write(jar.content)

                    return 0
                else:
                    logging.error("Checksum does not match.")
                    return 1

        logging.info("Stable release not found.")
        return 1
    else:
        logging.error("An error occured with the Paper API.")
        return 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        version = sys.argv[1]
        sys.exit(download(version))
    else:
        print("Provide version.")
        sys.exit(1)




