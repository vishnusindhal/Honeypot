import time
import shlex
from filesystem import VirtualFileSystem
from logger import HoneypotLogger
from commands import CommandHandler
from deception import DeceptionEngine
from session_recorder import SessionRecorder

class HoneypotSession:
    """
    Core Honeypot Session Manager with:
    - Virtual filesystem
    - Command simulation
    - Behavioral analysis
    - Session recording
    - Dynamic deception
    """
    
    def __init__(self, client_ip, username="admin"):
        self.client_ip = client_ip
        self.username = username
        self.fs = VirtualFileSystem()
        self.cwd = "/home/admin" if username == "admin" else "/root"
        self.logger = HoneypotLogger()
        self.session_id = "session-" + str(id(self))
        self.cmd_handler = CommandHandler(self)
        self.deception_engine = DeceptionEngine()
        self.session_recorder = SessionRecorder(
            session_id=self.session_id,
            client_ip=client_ip,
            username=username
        )
        self.env = {
            "TERM": "xterm-256color",
            "SHELL": "/bin/bash",
            "USER": username,
            "HOME": f"/home/{username}" if username != "root" else "/root",
            "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
        }

    def handle_command(self, cmd_str):
        """Process a command and return the output."""
        if not cmd_str.strip():
            return ""

        # Apply adaptive delay based on attacker skill
        delay = self.deception_engine.get_response_delay()
        time.sleep(delay)

        # Parse command
        try:
            parts = shlex.split(cmd_str)
        except ValueError:
            parts = cmd_str.split()

        if not parts:
            return ""

        base_cmd = parts[0]
        args = parts[1:]
        
        # Analyze behavior
        skill, intent = self.deception_engine.analyze(cmd_str)
        
        output = ""
        
        # Try Advanced Command Handler first
        advanced_output = self.cmd_handler.handle(base_cmd, args)
        if advanced_output is not None:
            output = advanced_output
        # Fallback to internal basic commands
        elif base_cmd == "ls":
            output = self._cmd_ls(args)
        elif base_cmd == "cd":
            output = self._cmd_cd(args)
        elif base_cmd == "pwd":
            output = self.cwd + "\n"
        elif base_cmd == "whoami":
            output = self.username + "\n"
        elif base_cmd == "id":
            uid = 0 if self.username == "root" else 1000
            gid = 0 if self.username == "root" else 1000
            output = f"uid={uid}({self.username}) gid={gid}({self.username}) groups={gid}({self.username})\n"
        elif base_cmd == "cat":
            output = self._cmd_cat(args)
        elif base_cmd == "help":
            output = "bash: help: command not found\n"
        else:
            output = f"bash: {base_cmd}: command not found\n"

        # Inject deception breadcrumbs for advanced attackers
        breadcrumb = self.deception_engine.inject_breadcrumb(cmd_str)
        if breadcrumb:
            output += breadcrumb

        # Log the interaction
        self.logger.log_command(
            session_id=self.session_id,
            source_ip=self.client_ip,
            username=self.username,
            command_str=cmd_str,
            cwd=self.cwd,
            intent=intent,
            skill_level=skill,
            response_type="success" if "command not found" not in output else "failure"
        )
        
        # Record in session transcript
        self.session_recorder.record_interaction(
            command=cmd_str,
            output=output,
            skill_level=skill,
            intent=intent,
            cwd=self.cwd
        )
        
        return output

    def end_session(self):
        """Clean up and save session recording."""
        self.session_recorder.end_session()
        return self.session_recorder.get_live_summary()

    def get_session_stats(self):
        """Get current session statistics."""
        return {
            "session_id": self.session_id,
            "client_ip": self.client_ip,
            "username": self.username,
            "commands_executed": self.session_recorder.command_count,
            "skill_level": self.deception_engine.skill_level,
            "deception_profile": self.deception_engine.get_session_profile()
        }

    # =========================================================================
    # BASIC COMMAND IMPLEMENTATIONS
    # =========================================================================

    def _resolve_path(self, path):
        """Resolve a path relative to cwd."""
        if path.startswith("/"):
            return path
        if path == "~":
            return "/root" if self.username == "root" else "/home/admin"
        if path == ".":
            return self.cwd
        if path == "..":
            if self.cwd == "/": 
                return "/"
            return "/".join(self.cwd.rstrip("/").split("/")[:-1]) or "/"
        return (self.cwd.rstrip("/") + "/" + path).replace("//", "/")

    def _cmd_ls(self, args):
        """List directory contents."""
        target_path = self.cwd
        show_all = False
        long_format = False
        
        for arg in args:
            if arg.startswith("-"):
                if "a" in arg:
                    show_all = True
                if "l" in arg:
                    long_format = True
            else:
                target_path = self._resolve_path(arg)
        
        items = self.fs.list_dir(target_path, show_hidden=show_all)
        if items is None:
            return f"ls: cannot access '{target_path}': No such file or directory\n"
        
        if long_format:
            lines = ["total " + str(len(items) * 4)]
            for item in items:
                perms = "d" if item.is_dir else "-"
                perms += "rwxr-xr-x" if item.is_dir else "rw-r--r--"
                links = "2" if item.is_dir else "1"
                size = str(item.size) if not item.is_dir else "4096"
                from datetime import datetime
                mtime = datetime.fromtimestamp(item.mtime).strftime("%b %d %H:%M")
                lines.append(f"{perms} {links} {item.owner:8} {item.group:8} {size:>8} {mtime} {item.name}")
            return "\n".join(lines) + "\n"
        else:
            out = []
            for item in items:
                name = item.name
                if item.is_dir:
                    name = "\033[1;34m" + name + "\033[0m"
                out.append(name)
            return "  ".join(out) + "\n"

    def _cmd_cd(self, args):
        """Change directory."""
        if not args:
            self.cwd = "/root" if self.username == "root" else "/home/admin"
            return ""
        
        target = self._resolve_path(args[0])
        node = self.fs.get_node(target)
        if node and node.is_dir:
            self.cwd = target.rstrip("/") if target != "/" else "/"
            return ""
        else:
            return f"bash: cd: {args[0]}: No such file or directory\n"

    def _cmd_cat(self, args):
        """Display file contents."""
        if not args:
            return ""
        
        target = self._resolve_path(args[0])
        node = self.fs.get_node(target)
        
        if not node:
            return f"cat: {args[0]}: No such file or directory\n"
        if node.is_dir:
            return f"cat: {args[0]}: Is a directory\n"
        
        # Permission check for sensitive files
        if "shadow" in node.name and self.username != "root":
            return f"cat: {args[0]}: Permission denied\n"

        return node.content
