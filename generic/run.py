#!/usr/bin/python3
import pystache
import yaml
import os
import sys
import click
import tempfile
import docker
import subprocess
import colorama
import re

colorama.init()

def ensure_path(path):
    path = os.path.expanduser(path)
    path = os.path.realpath(path)
    path = os.path.abspath(path)
    dir_name = os.path.dirname(path)
    try:
        os.makedirs(dir_name)
    except FileExistsError:
        pass


@click.command()
@click.option('--gpu/--cpu', default=True, help='Enable or disable GPU support and things that rely on it')
@click.option('--stage', type=click.Choice(['bootstrap', 'main'], case_sensitive=False), default='bootstrap', help='Target stage')
@click.option('--generate-only', default=False, help='Do not build launch the container, just generate the Dockerfile and the launcher script')
def run(gpu, stage, generate_only):
    script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    script_path = os.path.realpath(sys.argv[0])
    exosuit_dir = os.path.abspath(os.path.expanduser(os.path.join(script_dir, '../')))
    home_dir = os.path.expanduser('~')

    userid = int(subprocess.run('id -u ${USER}', shell=True, stdout=subprocess.PIPE).stdout)
    username = subprocess.run('getent group "$(id -g ${USER})" | cut -d: -f1', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1]

    with open(os.path.join(script_dir, 'requirements.yaml'), 'r') as f:
        requirements = yaml.load(f.read(), Loader=yaml.SafeLoader)

    gpu_str = 'gpu' if gpu else 'cpu'
    container_name = f'{stage}-{gpu_str}'
    image_tag = f'exosuit-{stage}-{gpu_str}'
    target_dir = os.path.join(exosuit_dir, container_name)

    if stage == 'bootstrap':
        container_command = f'python3 {script_path} --{gpu_str} --stage=main'
    else:
        container_command = '/bin/bash'

    dockerfile_render_args = {
        'gpu': gpu,
        'apt_get_deps': [
            {'package': package}
            for package, info in requirements['apt'].items()
            if stage in info['stages']
        ],
        'python_deps': [
            {
                'package': package,
                'version': info['version'],
            } for package, info in requirements['python'].items() 
            if stage in info['stages']
        ],
        'stage': stage,
    }

    with open(os.path.join(script_dir, 'Dockerfile.template'), 'r') as f:
        template_dockerfile = f.read()
    rendered_dockerfile = pystache.render(template_dockerfile, dockerfile_render_args)
    rendered_dockerfile = re.sub('\n\n+', '\n\n', rendered_dockerfile)

    dockerfile_path = os.path.join(target_dir, 'Dockerfile')
    ensure_path(dockerfile_path)
    with open(dockerfile_path, 'w') as f:
        f.write(rendered_dockerfile)

    run_script_render_args = {
        'container_name': container_name,
        'image_tag': image_tag,
        'command': container_command,
        'gpus': '--gpus all' if gpu else '',
    }

    with open(os.path.join(script_dir, 'run.template'), 'r') as f:
        template_run_script = f.read()
    rendered_run_script = pystache.render(template_run_script, run_script_render_args)
    rendered_run_script = re.sub('\n\n+', '\n\n', rendered_run_script)

    run_script_path = os.path.join(target_dir, 'run.sh')
    ensure_path(run_script_path)
    with open(run_script_path, 'w') as f:
        f.write(rendered_run_script)

    os.system(f'sudo chmod +x {run_script_path}')
    if not generate_only:
        os.system(f'{run_script_path}')


if __name__ == '__main__':
    run()