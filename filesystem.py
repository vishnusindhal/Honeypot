import time
import random
import hashlib
from datetime import datetime, timedelta

# ============================================================================
# FILE CONTENT GENERATOR - AI-Generated Dynamic Content
# ============================================================================

class FileContentGenerator:
    """Generates realistic fake content for various file types."""
    
    # Decoy credentials - tagged internally but look real
    DECOY_API_KEYS = [
        "AKIAIOSFODNN7EXAMPLE",  # AWS-style
        "sk-proj-aBcDeFgHiJkLmNoPqRsTuVwXyZ123456",  # OpenAI-style
        "ghp_1234567890abcdefghijklmnopqrstuvwxyz",  # GitHub-style
    ]
    
    DECOY_DB_CREDENTIALS = [
        {"user": "db_admin", "password": "Pr0d_S3cur3_2024!", "host": "localhost", "db": "production_db"},
        {"user": "backup_user", "password": "B4ckup_R34d0nly#", "host": "10.0.0.5", "db": "users"},
    ]
    
    @staticmethod
    def generate_auth_log(num_entries=20):
        """Generate realistic auth.log entries."""
        log_lines = []
        base_time = datetime.now() - timedelta(days=random.randint(1, 7))
        
        users = ["admin", "root", "devops", "backup"]
        ips = ["192.168.1.50", "10.0.0.15", "172.16.0.100", "192.168.1.101"]
        actions = [
            ("Accepted password for {user} from {ip} port {port} ssh2", "sshd"),
            ("session opened for user {user} by (uid=0)", "systemd-logind"),
            ("pam_unix(sshd:session): session opened for user {user}", "sshd"),
            ("Failed password for invalid user hacker from {ip} port {port} ssh2", "sshd"),
        ]
        
        for i in range(num_entries):
            t = base_time + timedelta(minutes=random.randint(1, 60) * i)
            user = random.choice(users)
            ip = random.choice(ips)
            port = random.randint(40000, 65000)
            action_template, service = random.choice(actions)
            action = action_template.format(user=user, ip=ip, port=port)
            pid = random.randint(1000, 9999)
            log_lines.append(f"{t.strftime('%b %d %H:%M:%S')} prod-db-01 {service}[{pid}]: {action}")
        
        return "\n".join(log_lines) + "\n"
    
    @staticmethod
    def generate_syslog(num_entries=15):
        """Generate realistic syslog entries."""
        log_lines = []
        base_time = datetime.now() - timedelta(hours=random.randint(1, 24))
        
        events = [
            ("systemd[1]", "Started Session {n} of user admin."),
            ("kernel", "[UFW BLOCK] IN=eth0 OUT= SRC=45.33.32.156 DST=10.0.0.5"),
            ("dockerd[542]", "Container {container} started"),
            ("cron[{pid}]", "(root) CMD (/usr/local/bin/backup.sh)"),
            ("mysqld[850]", "InnoDB: Buffer pool(s) dump completed at {time}"),
        ]
        
        for i in range(num_entries):
            t = base_time + timedelta(minutes=random.randint(5, 30) * i)
            event = random.choice(events)
            msg = event[1].format(n=random.randint(1, 100), container=f"web-{random.randint(1,5)}", 
                                   pid=random.randint(1000, 5000), time=t.strftime("%H:%M:%S"))
            log_lines.append(f"{t.strftime('%b %d %H:%M:%S')} prod-db-01 {event[0]}: {msg}")
        
        return "\n".join(log_lines) + "\n"
    
    @staticmethod
    def generate_nginx_conf():
        """Generate realistic nginx.conf."""
        return """user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 768;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    gzip on;

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
"""
    
    @staticmethod
    def generate_mysql_conf():
        """Generate realistic my.cnf."""
        return """[mysqld]
user            = mysql
pid-file        = /var/run/mysqld/mysqld.pid
socket          = /var/run/mysqld/mysqld.sock
port            = 3306
basedir         = /usr
datadir         = /var/lib/mysql
tmpdir          = /tmp
bind-address    = 127.0.0.1

# Logging
log_error       = /var/log/mysql/error.log
slow_query_log  = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2

# InnoDB settings
innodb_buffer_pool_size = 256M
innodb_log_file_size = 64M
innodb_flush_log_at_trx_commit = 1

# Security
local-infile = 0

[mysql]
prompt = \\u@\\h [\\d]>
"""
    
    @staticmethod
    def generate_env_file():
        """Generate a decoy .env file with fake credentials."""
        key = random.choice(FileContentGenerator.DECOY_API_KEYS)
        db = random.choice(FileContentGenerator.DECOY_DB_CREDENTIALS)
        return f"""# Production Environment - DO NOT COMMIT
NODE_ENV=production
PORT=3000

# Database
DB_HOST={db['host']}
DB_USER={db['user']}
DB_PASS={db['password']}
DB_NAME={db['db']}

# API Keys
AWS_ACCESS_KEY_ID={key}
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# Redis
REDIS_URL=redis://127.0.0.1:6379

# JWT
JWT_SECRET=super_secret_jwt_key_2024_prod
"""
    
    @staticmethod
    def generate_bash_history(num_entries=50):
        """Generate realistic bash history."""
        commands = [
            "ls -la", "cd /var/log", "tail -f auth.log", "ps aux | grep mysql",
            "sudo systemctl status nginx", "cat /etc/passwd", "whoami", "id",
            "docker ps", "docker logs web-1", "mysql -u root -p", "vim /etc/nginx/nginx.conf",
            "git pull origin main", "npm run deploy", "./deploy.sh", "crontab -l",
            "netstat -tulpn", "ss -lntp", "df -h", "free -m", "uptime",
            "curl -I https://api.internal.com/health", "wget http://backup.internal/db.sql",
            "scp admin@10.0.0.5:/backup/latest.tar.gz .", "chmod +x deploy.sh",
            "sudo apt update", "sudo apt upgrade -y", "journalctl -xe",
        ]
        return "\n".join(random.choices(commands, k=num_entries)) + "\n"

    @staticmethod
    def generate_ssh_private_key():
        """Generate a fake (but realistic-looking) SSH private key."""
        # This is a FAKE key - not cryptographically valid
        fake_body = "\n".join([
            hashlib.sha256(f"fake_key_line_{i}".encode()).hexdigest()[:64]
            for i in range(25)
        ])
        return f"""-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
{fake_body}
-----END OPENSSH PRIVATE KEY-----
"""

# ============================================================================
# VIRTUAL FILE SYSTEM
# ============================================================================

class VirtualFile:
    def __init__(self, name, content="", is_dir=False, owner="root", group="root", permissions="644", size=0, mtime=None):
        self.name = name
        self.content = content
        self.is_dir = is_dir
        self.owner = owner
        self.group = group
        self.permissions = permissions
        self.children = {}
        self.parent = None
        # Randomize mtime for realism (within last 30 days)
        if mtime:
            self.mtime = mtime
        else:
            self.mtime = time.time() - random.randint(0, 30 * 24 * 60 * 60)
        self.size = size if size > 0 else len(content)

    def add_child(self, child):
        if not self.is_dir:
            raise ValueError(f"Cannot add child to non-directory {self.name}")
        child.parent = self
        self.children[child.name] = child

    def get_path(self):
        if self.parent is None:
            return ""
        if self.parent.parent is None:
            return "/" + self.name
        return self.parent.get_path() + "/" + self.name
    
    def get_full_path(self):
        if self.name == "/": return "/"
        return self.get_path()


class VirtualFileSystem:
    def __init__(self):
        self.root = VirtualFile("/", is_dir=True, permissions="755")
        self.generator = FileContentGenerator()
        self._build_initial_structure()

    def _build_initial_structure(self):
        def mkdir_p(path, owner="root", group="root", perms="755"):
            parts = path.strip("/").split("/")
            current = self.root
            for part in parts:
                if not part: continue
                if part not in current.children:
                    new_dir = VirtualFile(part, is_dir=True, owner=owner, group=group, permissions=perms)
                    current.add_child(new_dir)
                current = current.children[part]
            return current

        def touch(path, content="", owner="root", group="root", perms="644", size=0):
            parent_path = "/".join(path.strip("/").split("/")[:-1])
            filename = path.strip("/").split("/")[-1]
            parent = self.get_node("/" + parent_path) if parent_path else self.root
            if parent:
                f = VirtualFile(filename, content=content, is_dir=False, owner=owner, group=group, permissions=perms, size=size)
                parent.add_child(f)

        # /etc - System Config
        mkdir_p("/etc")
        touch("/etc/passwd", 
              "root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\nadmin:x:1000:1000:Admin User:/home/admin:/bin/bash\npostgres:x:1001:1001::/var/lib/postgresql:/bin/bash\nmysql:x:27:27:MySQL Server:/var/lib/mysql:/bin/false\nnginx:x:33:33:nginx:/nonexistent:/bin/false\n")
        touch("/etc/shadow", "root:$6$rounds=656000$saltsalt$hashhashhashhashhashhashhashhashhashhashhashhashhashhashhashhashhashhashhashhash::0:99999:7:::\nadmin:$6$rounds=656000$abc$xyz...::0:99999:7:::\n", perms="000", owner="root")
        touch("/etc/crontab", "# /etc/crontab: system-wide crontab\nSHELL=/bin/sh\nPATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin\n\n# m h dom mon dow user  command\n17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly\n25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )\n0  3    * * *   root    /usr/local/bin/backup.sh\n")
        touch("/etc/hostname", "prod-db-01\n")
        touch("/etc/hosts", "127.0.0.1   localhost\n127.0.1.1   prod-db-01\n10.0.0.5    db-replica.internal\n10.0.0.10   redis.internal\n")

        # /etc/nginx - AI Generated
        mkdir_p("/etc/nginx")
        touch("/etc/nginx/nginx.conf", self.generator.generate_nginx_conf())

        # /etc/mysql - AI Generated
        mkdir_p("/etc/mysql")
        touch("/etc/mysql/my.cnf", self.generator.generate_mysql_conf())

        # /etc/ssh
        mkdir_p("/etc/ssh")
        touch("/etc/ssh/sshd_config", "Port 22\nPermitRootLogin no\nPasswordAuthentication yes\nPubkeyAuthentication yes\nAuthorizedKeysFile .ssh/authorized_keys\nChallengeResponseAuthentication no\nUsePAM yes\nX11Forwarding no\nPrintMotd no\nAcceptEnv LANG LC_*\nSubsystem sftp /usr/lib/openssh/sftp-server\n")

        # /var/log - AI Generated Logs
        mkdir_p("/var/log")
        touch("/var/log/auth.log", self.generator.generate_auth_log(30))
        touch("/var/log/syslog", self.generator.generate_syslog(25))
        mkdir_p("/var/log/nginx")
        touch("/var/log/nginx/access.log", '192.168.1.50 - - [04/Feb/2026:10:00:00 +0000] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0"\n')
        touch("/var/log/nginx/error.log", "")
        mkdir_p("/var/log/mysql")
        touch("/var/log/mysql/error.log", f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 0 [Note] InnoDB: Buffer pool(s) load completed\n")

        # /var/lib/mysql
        mkdir_p("/var/lib/mysql")
        touch("/var/lib/mysql/users.ibd", "\x00\x00\x00", size=10240, owner="mysql", group="mysql")
        touch("/var/lib/mysql/ib_logfile0", "\x00", size=50331648, owner="mysql", group="mysql")

        # /var/backups
        mkdir_p("/var/backups")
        touch("/var/backups/db_backup_2024.sql.gz", "<binary>", size=5242880)
        touch("/var/backups/db_backup_2025.sql.gz", "<binary>", size=6100000)

        # /home/admin - User home with decoy secrets
        mkdir_p("/home/admin", owner="admin", group="admin")
        touch("/home/admin/notes.txt", "TODO:\n- Rotate API keys for AWS (URGENT!)\n- Check backup integrity\n- Update SSL certs before March\n- Move DB credentials to vault\n", owner="admin", group="admin")
        touch("/home/admin/deploy.sh", "#!/bin/bash\nset -e\necho 'Deploying to production...'\ncd /var/www/app\ngit pull origin main\nnpm install --production\npm2 reload all\necho 'Deployment complete!'\n", owner="admin", group="admin", perms="744")
        touch("/home/admin/backup.sql", "-- MySQL dump\n-- Host: localhost\nINSERT INTO users (id, name, email) VALUES (1, 'admin', 'admin@company.com');\nINSERT INTO users (id, name, email) VALUES (2, 'john', 'john@company.com');\n", owner="admin", group="admin")
        touch("/home/admin/.env", self.generator.generate_env_file(), owner="admin", group="admin", perms="600")
        touch("/home/admin/.bash_history", self.generator.generate_bash_history(40), owner="admin", group="admin", perms="600")
        
        mkdir_p("/home/admin/.ssh", owner="admin", group="admin", perms="700")
        touch("/home/admin/.ssh/id_rsa", self.generator.generate_ssh_private_key(), owner="admin", group="admin", perms="600")
        touch("/home/admin/.ssh/authorized_keys", "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ... admin@workstation\n", owner="admin", group="admin", perms="600")

        # /root
        mkdir_p("/root", owner="root", group="root", perms="700")
        touch("/root/.bash_history", self.generator.generate_bash_history(20), owner="root", group="root", perms="600")

        # System directories
        mkdir_p("/bin")
        mkdir_p("/usr/bin")
        mkdir_p("/usr/local/bin")
        mkdir_p("/tmp", perms="1777")
        mkdir_p("/proc")
        mkdir_p("/var/www/app")

    def get_node(self, path):
        if path == "/":
            return self.root
        parts = path.strip("/").split("/")
        current = self.root
        for part in parts:
            if not part: continue
            if part in current.children:
                current = current.children[part]
            else:
                return None
        return current

    def list_dir(self, path, show_hidden=False):
        node = self.get_node(path)
        if not node:
            return None
        if not node.is_dir:
            return None
        items = []
        for name, child in node.children.items():
            if not show_hidden and name.startswith("."):
                continue
            items.append(child)
        return items
