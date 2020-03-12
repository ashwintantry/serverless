import os
import subprocess


def execute(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ):
    p = subprocess.Popen(cmds, stdout=stdout, stderr=stderr, env=env)
    stdout_data, stderr_data = p.communicate()
    if p.returncode != 0:
        raise RuntimeError('%s \n %s' % (str(stdout_data), str(stderr_data)))

    return str(stdout_data, 'utf-8') if stdout_data else None


def get_version(pom_file):
    version = execute(['mvn', '-f', pom_file, 'help:evaluate', '-Dexpression=project.version', '-q', '-DforceStdout']).strip()
    version = version.split('-')[0]
    hash = execute(['git', 'rev-parse', '--verify', 'HEAD']).strip()[:8]

    return "%s-%s" % (version, hash)
