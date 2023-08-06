from fabric import Connection, Config
import config
from domain.grafana import Grafana


# Using SSH key
# KEY_FILE = '/exnovo/etc/ssh/'
# 'key_filename': KEY_FILE

# Using password
# 'connect_kwargs': {'password': config.ftp_password}


class GrafanaShell(Grafana):
    @staticmethod
    def connection():
        configuration = Config(overrides={'user': config.grafana_username,
                                          'port': config.grafana_port,
                                          'sudo': {'password': config.grafana_password}})
        conn = Connection(host=config.grafana_host, config=configuration)
        return conn

    @staticmethod
    def install_grafana():
        conn = GrafanaShell.connection()

        commands = [
            'add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"',
            'apt update',
            'apt -y install grafana',
            'rm -f /etc/grafana/grafana.ini',
            'mv grafana.ini /etc/grafana/grafana.ini',
            'systemctl daemon-reload',
            'systemctl restart grafana-server'
        ]

        conn.put(config.grafana_ini_file)
        conn.sudo('curl https://packages.grafana.com/gpg.key | sudo apt-key add -', hide=True)

        for command in commands:
            conn.sudo(command)

    @staticmethod
    def install_loki():
        conn = GrafanaShell.connection()

        conn.put(config.loki_yaml_file)
        conn.put(config.loki_service_file)

        commands = [
            "curl -s https://api.github.com/repos/grafana/loki/releases/latest | grep browser_download_url |  cut -d '\"' -f 4 | grep loki-linux-amd64.zip | wget -i -",
            "unzip loki-linux-amd64.zip",
            "rm loki-linux-amd64.zip",
            "mv loki-linux-amd64 /usr/local/bin/loki",
            "mkdir -p /data/loki",
            "mv loki-local-config.yaml /etc/loki-local-config.yaml",
            "mv loki.service /etc/systemd/system/loki.service",
            "systemctl daemon-reload",
            "systemctl start loki.service"
        ]

        for command in commands:
            conn.sudo(command)

    @staticmethod
    def install_promtail():
        conn = GrafanaShell.connection()

        conn.put(config.promtail_yaml_file)
        conn.put(config.promtail_service_file)

        # Installation de Promtail
        commands = [
            "curl -s https://api.github.com/repos/grafana/loki/releases/latest | grep browser_download_url |  cut -d '\"' -f 4 | grep promtail-linux-amd64.zip | wget -i -",
            "unzip promtail-linux-amd64.zip",
            "rm promtail-linux-amd64.zip",
            "mv promtail-linux-amd64 /usr/local/bin/promtail",
            "mv promtail-local-config.yaml /etc/promtail-local-config.yaml",
            "mv promtail.service /etc/systemd/system/promtail.service",
            "systemctl daemon-reload",
            "systemctl start promtail.service"
        ]

        for command in commands:
            conn.sudo(command)


if __name__ == "__main__":
    # GrafanaShell.install_grafana()
    # GrafanaShell.install_loki()
    GrafanaShell.install_promtail()
