"""The arm: open() inside a program becomes a file object over read_file and write_file."""

import re

SHIM = '''class _ToolFile:
    def __init__(self, path, mode="r", *args, **kwargs):
        self.path, self.mode, self.closed, self.pos = path, mode, False, 0
        if "b" in mode:
            raise PermissionError(f"{path}: binary mode is not available here; read_file and write_file handle text")
        self.text = ""
        got = read_file(path)
        if isinstance(got, str) and got.startswith("ERROR: "):
            if "no such file" not in got:
                raise PermissionError(got[7:])
            if "r" in mode:
                raise FileNotFoundError(f"[Errno 2] No such file or directory: {path!r}")
        else:
            self.text = got
        if "w" in mode or "x" in mode:
            self.text = ""
        self.writing = any(m in mode for m in "wax+")
        if "a" in mode:
            self.pos = len(self.text)
    def read(self, n=-1):
        end = len(self.text) if n is None or n < 0 else self.pos + n
        out, self.pos = self.text[self.pos:end], min(end, len(self.text))
        return out
    def readline(self, n=-1):
        nl = self.text.find("\\n", self.pos)
        end = len(self.text) if nl < 0 else nl + 1
        if n is not None and n >= 0:
            end = min(end, self.pos + n)
        out, self.pos = self.text[self.pos:end], end
        return out
    def readlines(self, hint=-1):
        return list(self)
    def __iter__(self):
        while True:
            line = self.readline()
            if not line:
                return
            yield line
    def write(self, s):
        self.text = self.text[:self.pos] + s + self.text[self.pos + len(s):]
        self.pos += len(s)
        return len(s)
    def writelines(self, lines):
        for line in lines:
            self.write(line)
    def seek(self, pos, whence=0):
        self.pos = pos if whence == 0 else (self.pos + pos if whence == 1 else len(self.text) + pos)
        return self.pos
    def tell(self):
        return self.pos
    def flush(self):
        pass
    def close(self):
        if not self.closed and self.writing:
            got = write_file(self.path, self.text)
            if isinstance(got, str) and got.startswith("ERROR: "):
                self.closed = True
                raise PermissionError(got[7:])
        self.closed = True
    def __enter__(self):
        return self
    def __exit__(self, *exc):
        self.close()
        return False
    def __del__(self):
        try:
            self.close()
        except Exception:
            pass
open = _ToolFile
'''
SHIM_LINES = SHIM.count("\n")
_FRAME = re.compile(r'File "<program>", line (\d+)')


def install():
    """Let programs call open(); everything still goes through the game tools."""
    from maestro.codegen.pyexec import runner

    saved = (runner.run, runner.check, runner.BANNED_CALLS)
    original_run, original_check = runner.run, runner.check

    def check(code):
        return original_check(code[len(SHIM):] if code.startswith(SHIM) else code)

    def run(code, tools, timeout=runner.TIMEOUT_SECONDS):
        refusal = original_check(code)
        if refusal:
            return runner.Outcome(stdout="", refused=refusal)
        out = original_run(SHIM + code, tools, timeout)
        out.stdout = _shift(out.stdout)
        return out

    runner.BANNED_CALLS = runner.BANNED_CALLS - {"open"}
    runner.check, runner.run = check, run
    return saved


def restore(saved) -> None:
    from maestro.codegen.pyexec import runner
    runner.run, runner.check, runner.BANNED_CALLS = saved


def _shift(stdout: str) -> str:
    kept = []
    for line in stdout.splitlines(keepends=True):
        m = _FRAME.search(line)
        if m and int(m.group(1)) <= SHIM_LINES:
            continue
        if m:
            line = line[:m.start(1)] + str(int(m.group(1)) - SHIM_LINES) + line[m.end(1):]
        kept.append(line)
    return "".join(kept)
