import datetime
import random
import time

class CommandHandler:
    def __init__(self, session):
        self.session = session

    def handle(self, cmd_name, args):
        method_name = f"cmd_{cmd_name}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(args)
        return None

    # =========================================================================
    # SYSTEM INFO COMMANDS
    # =========================================================================
    
    def cmd_uname(self, args):
        if not args:
            return "Linux\n"
        if "-a" in args or "--all" in args:
            return "Linux prod-db-01 5.4.0-150-generic #167-Ubuntu SMP Mon May 15 17:35:05 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux\n"
        if "-r" in args:
            return "5.4.0-150-generic\n"
        if "-n" in args:
            return "prod-db-01\n"
        if "-m" in args:
            return "x86_64\n"
        return "Linux\n"

    def cmd_hostname(self, args):
        return "prod-db-01\n"

    def cmd_uptime(self, args):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        days = random.randint(10, 120)
        hours = random.randint(0, 23)
        mins = random.randint(0, 59)
        load1 = round(random.uniform(0.01, 0.5), 2)
        load5 = round(random.uniform(0.01, 0.3), 2)
        load15 = round(random.uniform(0.01, 0.2), 2)
        return f" {now} up {days} days, {hours}:{mins:02d},  1 user,  load average: {load1}, {load5}, {load15}\n"

    def cmd_date(self, args):
        return datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y\n")

    def cmd_free(self, args):
        return """              total        used        free      shared  buff/cache   available
Mem:        8167548     2345672     1234567      123456     4587309     5432100
Swap:       2097148           0     2097148
"""

    def cmd_df(self, args):
        return """Filesystem     1K-blocks    Used Available Use% Mounted on
udev             4063604       0   4063604   0% /dev
tmpfs             816756    1232    815524   1% /run
/dev/sda1       51343840 8765432  40234567  18% /
tmpfs            4083780       0   4083780   0% /dev/shm
tmpfs               5120       0      5120   0% /run/lock
/dev/sda15        106858    5329    101529   5% /boot/efi
"""

    # =========================================================================
    # ENVIRONMENT & HISTORY
    # =========================================================================

    def cmd_env(self, args):
        env_vars = {
            "SHELL": "/bin/bash",
            "PWD": self.session.cwd,
            "LOGNAME": self.session.username,
            "HOME": f"/home/{self.session.username}" if self.session.username != "root" else "/root",
            "LANG": "en_US.UTF-8",
            "USER": self.session.username,
            "TERM": "xterm-256color",
            "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
            "SSH_TTY": "/dev/pts/0",
            "SSH_CLIENT": f"{self.session.client_ip} 55432 22",
            "SSH_CONNECTION": f"{self.session.client_ip} 55432 10.0.0.5 22",
            "MAIL": f"/var/mail/{self.session.username}",
        }
        return "\n".join([f"{k}={v}" for k, v in env_vars.items()]) + "\n"

    def cmd_history(self, args):
        # Read from virtual .bash_history if available
        history_path = f"/home/{self.session.username}/.bash_history" if self.session.username != "root" else "/root/.bash_history"
        node = self.session.fs.get_node(history_path)
        if node and not node.is_dir:
            lines = node.content.strip().split("\n")
            output = []
            for i, line in enumerate(lines[-50:], 1):  # Last 50 commands
                output.append(f"  {i}  {line}")
            return "\n".join(output) + "\n"
        return ""

    def cmd_export(self, args):
        # Fake export - commonly used by attackers to unset history
        return ""

    def cmd_unset(self, args):
        # Fake unset - commonly used to disable history
        return ""

    # =========================================================================
    # PROCESS & SYSTEM STATUS
    # =========================================================================

    def cmd_ps(self, args):
        header = "USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\n"
        processes = [
            "root           1  0.0  0.1 168904 12940 ?        Ss   Feb01   0:04 /sbin/init",
            "root           2  0.0  0.0      0     0 ?        S    Feb01   0:00 [kthreadd]",
            "root         215  0.0  0.0      0     0 ?        S<   Feb01   0:00 [kworker/0:1H-kblockd]",
            "root         542  0.0  0.5 1200400 24000 ?       Ssl  Feb01   0:12 /usr/bin/dockerd -H fd://",
            "mysql        850  0.1  8.4 2500000 80000 ?       Ssl  Feb01   5:23 /usr/sbin/mysqld",
            "redis        901  0.0  0.1  50000  4000 ?        Ssl  Feb01   0:45 /usr/bin/redis-server 127.0.0.1:6379",
            "root        1021  0.0  0.1  90000  5000 ?        Ss   Feb01   0:00 /usr/sbin/sshd -D",
            "root        1205  0.0  0.1  70000  3500 ?        Ss   Feb01   0:01 nginx: master process",
            "www-data    1206  0.0  0.1  72000  4000 ?        S    Feb01   0:00 nginx: worker process",
            "root        1300  0.0  0.0  6000  1500 ?         Ss   Feb01   0:00 /usr/sbin/cron -f",
            f"{self.session.username}       {random.randint(3000,4000)}  0.0  0.2  10000  4500 pts/0    Ss   10:00   0:00 -bash",
            f"{self.session.username}       {random.randint(4000,5000)}  0.0  0.1   8000  2000 pts/0    R+   10:00   0:00 ps aux"
        ]
        return header + "\n".join(processes) + "\n"

    def cmd_top(self, args):
        # Static top output (interactive not feasible in this setup)
        now = datetime.datetime.now().strftime("%H:%M:%S")
        days = random.randint(10, 120)
        return f"""top - {now} up {days} days,  3:12,  1 user,  load average: 0.08, 0.05, 0.01
Tasks: 112 total,   1 running, 111 sleeping,   0 stopped,   0 zombie
%Cpu(s):  1.2 us,  0.5 sy,  0.0 ni, 98.1 id,  0.2 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   7976.1 total,   1234.5 free,   2345.6 used,   4396.0 buff/cache
MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   5321.0 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
    850 mysql     20   0 2500000  80000  12000 S   0.3   8.4   5:23.45 mysqld
    542 root      20   0 1200400  24000   8000 S   0.1   0.5   0:12.34 dockerd
   1021 root      20   0   90000   5000   3000 S   0.0   0.1   0:00.12 sshd
   1205 root      20   0   70000   3500   2500 S   0.0   0.1   0:01.00 nginx
"""

    def cmd_dmesg(self, args):
        return """[    0.000000] Linux version 5.4.0-150-generic (buildd@lcy01-amd64-001)
[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-5.4.0-150-generic root=UUID=8d23-4241 ro
[    0.623123] kvm: disabled by bios
[    1.231233] systemd[1]: Detected architecture x86-64.
[    1.456789] systemd[1]: Set hostname to <prod-db-01>.
[    2.345678] EXT4-fs (sda1): mounted filesystem with ordered data mode.
[    3.567890] docker0: port 1(veth123) entered blocking state
"""

    # =========================================================================
    # NETWORK COMMANDS
    # =========================================================================

    def cmd_netstat(self, args):
        return """Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:6379          0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN     
tcp        0      0 10.0.0.5:22             """ + self.session.client_ip + """:55432         ESTABLISHED
tcp6       0      0 :::80                   :::*                    LISTEN     
tcp6       0      0 :::22                   :::*                    LISTEN     
"""

    def cmd_ss(self, args):
        return """State      Recv-Q Send-Q        Local Address:Port          Peer Address:Port Process
LISTEN     0      128               127.0.0.1:3306               0.0.0.0:*     
LISTEN     0      128               127.0.0.1:6379               0.0.0.0:*     
LISTEN     0      128                 0.0.0.0:80                 0.0.0.0:*     users:(("nginx",pid=1205))
LISTEN     0      128                 0.0.0.0:22                 0.0.0.0:*     users:(("sshd",pid=1021))
ESTAB      0      0                  10.0.0.5:22             """ + self.session.client_ip + """:55432     users:(("sshd",pid=3452))
"""

    def cmd_ifconfig(self, args):
        return """eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.0.0.5  netmask 255.255.255.0  broadcast 10.0.0.255
        inet6 fe80::42:acff:fe11:1  prefixlen 64  scopeid 0x20<link>
        ether 02:42:ac:11:00:01  txqueuelen 0  (Ethernet)
        RX packets 123456  bytes 12345678 (11.7 MiB)
        TX packets 654321  bytes 65432100 (62.4 MiB)

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
"""

    def cmd_ip(self, args):
        if args and args[0] == "addr":
            return """1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 state UNKNOWN
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host 
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 state UP
    inet 10.0.0.5/24 brd 10.0.0.255 scope global eth0
    inet6 fe80::42:acff:fe11:1/64 scope link 
"""
        return "Usage: ip [ addr | route | link ]\n"

    # =========================================================================
    # FILE SEARCH COMMANDS
    # =========================================================================

    def cmd_find(self, args):
        # Simplified find - just return some fake results based on common patterns
        if not args:
            return "find: missing argument\n"
        
        path = args[0] if not args[0].startswith("-") else "."
        
        # Check for common patterns
        name_pattern = None
        for i, arg in enumerate(args):
            if arg == "-name" and i + 1 < len(args):
                name_pattern = args[i + 1].replace("*", "")
        
        # Return some fake results based on the pattern
        if name_pattern:
            if "pass" in name_pattern.lower():
                return f"{path}/etc/passwd\n{path}/backup/passwords.txt.bak\n"
            if "config" in name_pattern.lower() or "conf" in name_pattern.lower():
                return f"{path}/etc/nginx/nginx.conf\n{path}/etc/mysql/my.cnf\n{path}/etc/ssh/sshd_config\n"
            if ".env" in name_pattern:
                return f"{path}/home/admin/.env\n{path}/var/www/app/.env\n"
            if ".sh" in name_pattern:
                return f"{path}/home/admin/deploy.sh\n{path}/usr/local/bin/backup.sh\n"
        
        return f"{path}\n"

    def cmd_grep(self, args):
        if len(args) < 2:
            return "Usage: grep [OPTION]... PATTERN [FILE]...\n"
        
        pattern = args[0]
        target = args[1] if len(args) > 1 else None
        
        # Simulate finding patterns in files
        if target and target.endswith("passwd"):
            if "root" in pattern or pattern == ":0:":
                return "root:x:0:0:root:/root:/bin/bash\n"
        
        if "password" in pattern.lower() or "secret" in pattern.lower():
            return """./home/admin/.env:DB_PASS=Pr0d_S3cur3_2024!
./.bash_history:mysql -u root -pOldPassword123
./backup/config.bak:admin_secret=changeme123
"""
        
        return ""

    def cmd_tree(self, args):
        target = args[0] if args else self.session.cwd
        node = self.session.fs.get_node(target)
        
        if not node:
            return f"{target} [error opening dir]\n\n0 directories, 0 files\n"
        
        if not node.is_dir:
            return f"{target}\n\n0 directories, 1 file\n"
        
        def _tree_recursive(n, prefix=""):
            lines = []
            children = list(n.children.values())
            for i, child in enumerate(children):
                is_last = i == len(children) - 1
                connector = "└── " if is_last else "├── "
                lines.append(f"{prefix}{connector}{child.name}")
                if child.is_dir:
                    ext = "    " if is_last else "│   "
                    lines.extend(_tree_recursive(child, prefix + ext))
            return lines
        
        lines = [target] + _tree_recursive(node)
        dir_count = sum(1 for c in node.children.values() if c.is_dir)
        file_count = sum(1 for c in node.children.values() if not c.is_dir)
        return "\n".join(lines) + f"\n\n{dir_count} directories, {file_count} files\n"

    # =========================================================================
    # SERVICE & CRON
    # =========================================================================

    def cmd_systemctl(self, args):
        if not args:
            return "systemctl: missing argument\n"
        
        action = args[0]
        service = args[1] if len(args) > 1 else None
        
        if action == "status":
            if not service:
                return "systemctl status requires a service name\n"
            
            services = {
                "nginx": ("active (running)", 1205, "nginx: master process"),
                "mysql": ("active (running)", 850, "/usr/sbin/mysqld"),
                "sshd": ("active (running)", 1021, "/usr/sbin/sshd -D"),
                "redis": ("active (running)", 901, "/usr/bin/redis-server"),
                "docker": ("active (running)", 542, "/usr/bin/dockerd"),
            }
            
            if service in services or service.replace(".service", "") in services:
                svc = service.replace(".service", "")
                status, pid, cmd = services.get(svc, ("inactive (dead)", 0, ""))
                return f"""● {svc}.service - {svc.upper()} Server
     Loaded: loaded (/lib/systemd/system/{svc}.service; enabled)
     Active: {status} since Mon 2024-02-01 00:00:00 UTC; 30 days ago
   Main PID: {pid} ({cmd.split()[0].split('/')[-1]})
      Tasks: 4
     Memory: 50.0M
     CGroup: /system.slice/{svc}.service
             └─{pid} {cmd}
"""
            return f"Unit {service} could not be found.\n"
        
        if action in ["start", "stop", "restart"]:
            if self.session.username != "root":
                return f"Failed to {action} {service}: Permission denied\n"
            return ""
        
        return f"Unknown operation '{action}'\n"

    def cmd_crontab(self, args):
        if "-l" in args:
            return """# m h  dom mon dow   command
0 3 * * * /usr/local/bin/backup.sh
0 * * * * /usr/bin/certbot renew --quiet
*/5 * * * * /usr/local/bin/health_check.sh
"""
        return ""

    # =========================================================================
    # PRIVILEGE ESCALATION
    # =========================================================================

    def cmd_sudo(self, args):
        if not args:
            return "usage: sudo -h | -K | -k | -V\nusage: sudo -v [-AknS] [-g group] [-h host] [-p prompt] [-u user]\n"
        
        if "-l" in args:
            if self.session.username == "admin":
                return """Matching Defaults entries for admin on prod-db-01:
    env_reset, mail_badpass

User admin may run the following commands on prod-db-01:
    (ALL : ALL) NOPASSWD: ALL
"""
            return f"User {self.session.username} is not allowed to run sudo on prod-db-01.\n"
        
        if self.session.username not in ["admin", "root"]:
            return f"{self.session.username} is not in the sudoers file.  This incident will be reported.\n"
        
        # Execute command as root
        target_cmd = " ".join(args)
        original_user = self.session.username
        self.session.username = "root"
        output = self.session.handle_command(target_cmd)
        self.session.username = original_user
        return output

    def cmd_su(self, args):
        target_user = args[0] if args else "root"
        if target_user == "root" and self.session.username != "admin":
            return "su: Authentication failure\n"
        # For honeypot, we don't actually switch - just acknowledge
        return ""  # Real su would switch session context

    # =========================================================================
    # DOWNLOAD COMMANDS
    # =========================================================================

    def cmd_wget(self, args):
        return self._fake_download(args, "wget")

    def cmd_curl(self, args):
        if "-O" in args or "-o" in args:
            return self._fake_download(args, "curl")
        if args:
            # curl without -O just prints content
            url = args[-1]
            return f"<!DOCTYPE html>\n<html><head><title>Index</title></head><body>Fake content from {url}</body></html>\n"
        return "curl: try 'curl --help' for more information\n"

    def _fake_download(self, args, tool):
        if not args:
            return "missing URL\n"
        url = [a for a in args if a.startswith("http")]
        if not url:
            return "missing URL\n"
        url = url[0]
        time.sleep(0.5)  # Short delay for realism
        host = url.split("//")[-1].split("/")[0]
        filename = url.split("/")[-1] or "index.html"
        return f"""--2024-02-04 10:05:00--  {url}
Resolving {host}... 1.2.3.4
Connecting to {host}:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1234 (1.2K) [text/html]
Saving to: '{filename}'

{filename}          100%[===================>]   1.21K  --.-KB/s    in 0s      

2024-02-04 10:05:01 (100 MB/s) - '{filename}' saved [1234/1234]
"""

    # =========================================================================
    # MISC COMMANDS
    # =========================================================================

    def cmd_echo(self, args):
        return " ".join(args) + "\n"

    def cmd_touch(self, args):
        return ""  # Silent success

    def cmd_mkdir(self, args):
        return ""  # Silent success for honeypot

    def cmd_rm(self, args):
        return ""  # Fake success

    def cmd_cp(self, args):
        return ""

    def cmd_mv(self, args):
        return ""

    def cmd_chmod(self, args):
        return ""

    def cmd_chown(self, args):
        if self.session.username != "root":
            return "chown: changing ownership: Operation not permitted\n"
        return ""

    def cmd_clear(self, args):
        return "\033[2J\033[H"  # ANSI clear screen

    def cmd_exit(self, args):
        return "logout\n"

    def cmd_which(self, args):
        if not args:
            return ""
        cmd = args[0]
        known = ["ls", "cat", "grep", "find", "wget", "curl", "python", "python3", "bash", "sh"]
        if cmd in known:
            return f"/usr/bin/{cmd}\n"
        return ""

    def cmd_file(self, args):
        if not args:
            return "Usage: file [FILE]...\n"
        return f"{args[0]}: ASCII text\n"

    def cmd_head(self, args):
        if not args:
            return ""
        target = self.session._resolve_path(args[-1])
        node = self.session.fs.get_node(target)
        if node and not node.is_dir:
            lines = node.content.split("\n")[:10]
            return "\n".join(lines) + "\n"
        return f"head: cannot open '{args[-1]}' for reading: No such file or directory\n"

    def cmd_tail(self, args):
        if not args:
            return ""
        target = self.session._resolve_path(args[-1])
        node = self.session.fs.get_node(target)
        if node and not node.is_dir:
            lines = node.content.split("\n")[-10:]
            return "\n".join(lines) + "\n"
        return f"tail: cannot open '{args[-1]}' for reading: No such file or directory\n"

    def cmd_wc(self, args):
        if not args:
            return ""
        target = self.session._resolve_path(args[-1])
        node = self.session.fs.get_node(target)
        if node and not node.is_dir:
            lines = len(node.content.split("\n"))
            words = len(node.content.split())
            chars = len(node.content)
            return f"  {lines}   {words}  {chars} {args[-1]}\n"
        return f"wc: {args[-1]}: No such file or directory\n"
