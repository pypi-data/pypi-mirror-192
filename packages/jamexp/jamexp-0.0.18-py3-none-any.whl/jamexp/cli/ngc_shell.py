import itertools
import json
import os
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

import pandas as pd
import typer
from loguru import logger
from plumbum.commands.processes import ProcessExecutionError
from pyfzf.pyfzf import FzfPrompt

from jamexp.utils.os_shell import run_simple_command


@dataclass(order=True)
class BaseStatus:
    sort_index: int = field(init=False, repr=False)
    created_time: datetime
    queued_time: datetime
    started_time: datetime
    ended_time: datetime

    status: str
    job_id: str
    job_name: str
    device: str
    def __post_init__(self):
        self.sort_index = self.created_time
        if self.status == 'FINISHED_SUCCESS':
            if self.get_run_time() < timedelta(seconds=60):
                self.status = 'SHORT_RUN'

    def get_run_time(self):
        if self.status == 'RUNNING':
            return datetime.now(timezone.utc).replace(tzinfo=None) - self.started_time
        if self.status in ['FINISHED_SUCCESS', 'KILLED_BY_ADMIN']:
            if self.ended_time < datetime.max and self.started_time < datetime.max:
                return self.ended_time - self.started_time
        return timedelta(0)
    def get_queued_time(self):
        if self.status == ['QUEUED', 'RUNNING', 'FINISHED_SUCCESS']:
            return datetime.now(timezone.utc).replace(tzinfo=None) - self.queued_time
        return timedelta(999)

    def get_fzf_kv(self):
        run_time = self.get_run_time()
        base_kv = {
            'id': self.job_id,
            'status': self.status,
            'name': self.job_name,
            'run_time': f"{run_time.days}D{run_time.seconds//3600}H{(run_time.seconds//60)%60}M",
            'device': self.device,
        }
        return base_kv


    def get_ls_kv(self):
        base_kv = {
            'id': self.job_id,
            'name': self.job_name,
            'device': self.device,
        }
        run_time = self.get_run_time()
        if self.status in ['RUNNING','FINISHED_SUCCESS', 'KILLED_BY_ADMIN', 'KILLED_BY_USER']:
            base_kv['run_time'] = f"{run_time.days}D{run_time.seconds//3600}H{(run_time.seconds//60)%60}M"
        if self.status == 'QUEUED':
            queued_time = self.get_queued_time()
            base_kv['queued_time'] = f"{queued_time.days}D{queued_time.seconds//3600}H{(queued_time.seconds//60)%60}M"

        base_kv['created'] = self.created_time.strftime('%m-%d %H:%M')

        return base_kv

def parse_jobs(list_job):
    parsed_jobs = defaultdict(list)
    for job in list_job:
        status = job['jobStatus']['status']
        job_name = job['jobDefinition']['name']
        job_id = job['id']
        device = job['aceResourceInstance']
        created_time = datetime.strptime(job['jobStatus']['createdDate'], '%Y-%m-%dT%H:%M:%S.%fZ')

        # parsing queued time
        if 'queuedAt' in job['jobStatus']:
            queued_time = datetime.strptime(job['jobStatus']['queuedAt'], '%Y-%m-%dT%H:%M:%S.000Z')
        else:
            queued_time = datetime.max
        # paraing started time
        if 'startedAt' in job['jobStatus']:
            started_time = datetime.strptime(job['jobStatus']['startedAt'], '%Y-%m-%dT%H:%M:%S.000Z')
        else:
            started_time = datetime.max
        # parsing ended time
        if 'endedAt' in job['jobStatus']:
            ended_time = datetime.strptime(job['jobStatus']['endedAt'], '%Y-%m-%dT%H:%M:%S.000Z')
        else:
            ended_time = datetime.max

        job = BaseStatus(created_time, queued_time, started_time, ended_time, status, job_id, job_name, device)

        parsed_jobs[job.status].append(job)

    return parsed_jobs

def ls_print_jobs(parsed_jobs, selected_status=None):
    sort_keys = {
        'RUNNING': 'run_time',
        'QUEUED': 'queued_time',
        'FINISHED_SUCCESS': 'id',
        'KILLED_BY_ADMIN': 'id',
        'KILLED_BY_USER': 'id',
    }
    # import ipdb; ipdb.set_trace()
    for status, jobs in parsed_jobs.items():
        if selected_status and status.lower() is not selected_status.lower():
            continue
        print("#"*10 + f" {status}  Total {len(jobs):<10}" + "#"*10)
        df = pd.DataFrame([job.get_ls_kv() for job in jobs]).sort_values(
            sort_keys.get(status, 'id'), ascending=False
        )
        print(df.to_string(index=False))

def collect_job(is_dir, key):
    team = 'deep-imagination' if is_dir else 'lpr-imagine'
    stdout, stderr = run_simple_command(f'ngc batch list --format_type json --team {team}')
    if stderr:
        print('ngc batch list error')
        print(stderr)
    else:
        list_job = json.loads(stdout)
        parsed_jobs = parse_jobs(list_job)
        # filter jobs if key is not None and job_name has key
        if key:
            parsed_jobs = {k: [job for job in v if key in job.job_name] for k, v in parsed_jobs.items()}
    return parsed_jobs


def _ngc_list(
    is_dir : bool = typer.Option(False, "-t/-T", help="defualt use lpr-imagine, otherwise use deep-imagination"),
    key : str = typer.Option('ml', help='filter key, only show jobs whose names contain the key'),
    status : str = typer.Option('none', help='filter status, only show jobs whose status is the status'),
):
    status = None if status.lower() == 'none' else status
    parsed_jobs = collect_job(is_dir, key)
    ls_print_jobs(parsed_jobs, status)

def _ngc_result(
    is_dir : bool = typer.Option(False, "-t/-T", help="defualt use lpr-imagine, otherwise use deep-imagination"),
    key : str = typer.Option('ml', help='filter key, only show jobs whose names contain the key'),
    is_fzf : bool = typer.Option(False, "-i/-I", help="use iteractive fzf to select job, default false -> use latest job"),
):
    parsed_jobs = collect_job(is_dir, key)
    # parsed_jobs = {k: v if k in [] for k, v in parsed_jobs.items()}
    if 'QUEUED' in parsed_jobs:
        del parsed_jobs['QUEUED']
    if 'STARTING' in parsed_jobs:
        del parsed_jobs['STARTING']
    all_jobs = list(itertools.chain.from_iterable(parsed_jobs.values()))
    if is_fzf:
        df = pd.DataFrame([job.get_fzf_kv() for job in all_jobs]).sort_values('id', ascending=False)
        fzf_str = df.to_string(index=False).split('\n')
        try:
            fzf = FzfPrompt()
            select_run_str = fzf.prompt(fzf_str)[0]
            selected_id = int(select_run_str.split(' ')[0])
            select_run = [job for job in all_jobs if job.job_id == selected_id][0]
        except ProcessExecutionError:
            exit(1)
        except Exception as error:  # pylint: disable=broad-except
            raise RuntimeError(  # pylint: disable=raise-missing-from
                "FZF error: {}".format(error)
            )
    else:
        latest_job = max(all_jobs, key=lambda x: x.job_id)
        if latest_job:
            select_run = latest_job
        else:
            exit(0)

    logger.warning(f"bash exec {select_run}")
    save_dir = os.path.expanduser("~/ngc_results")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    if os.path.exists(f"{save_dir}/{select_run.job_id}"):
        os.system(f'rm -rf {save_dir}/{select_run.job_id}')
    os.system(f'ngc result download {select_run.job_id} --dest {save_dir}')
    if os.path.exists(f"{save_dir}/{select_run.job_id}/error.txt"):
        logger.info(f"{save_dir}/{select_run.job_id}/error.txt")
        os.system(f'cat {save_dir}/{select_run.job_id}/error.txt')
    if os.path.exists(f"{save_dir}/{select_run.job_id}/joblog.log"):
        logger.info(f"{save_dir}/{select_run.job_id}/joblog.log")
        os.system(f'cat {save_dir}/{select_run.job_id}/joblog.log')

def get_job_info(team, key):
    team = 'lpr-imagine' if team else 'deep-imagination'

    stdout, stderr = run_simple_command(f'ngc batch list --format_type json --team {team}')
    jobs_info = defaultdict(list)
    latest_run, latest_td = None, timedelta(365)
    if stderr:
        print('ngc batch list error')
        print(stderr)
    else:
        list_job = json.loads(stdout)
        for job in list_job:
            status = job['jobStatus']['status']
            name = job['jobDefinition']['name']
            job_id = job['id']
            if key in name:
                if status in ['STARTING', 'RUNNING', 'QUEUED']:
                    if status == 'RUNNING':
                        s_t = datetime.strptime(job['jobStatus']['startedAt'], '%Y-%m-%dT%H:%M:%S.000Z')
                        cur_t = datetime.now(timezone.utc).replace(tzinfo=None)
                        td = (cur_t - s_t)
                        _info = f"{job_id:<15} {name:<35} {status:<10} {td.days}D {td.seconds//3600}H {(td.seconds//60)%60}M"
                        jobs_info[status].append(_info)
                        if td < latest_td:
                            latest_run = _info
                            latest_td = td
                    elif status == 'QUEUED':
                        s_t = datetime.strptime(job['jobStatus']['queuedAt'], '%Y-%m-%dT%H:%M:%S.000Z')
                        cur_t = datetime.now(timezone.utc).replace(tzinfo=None)
                        td = (cur_t - s_t)
                        jobs_info[status].append(f"{job_id:<15} {name:<35} {status:<10} {td.days}D {td.seconds//3600}H {(td.seconds//60)%60}M")
                    else:
                        jobs_info[status].append(f"{job_id:<15} {name:<35} {status:<10}")
    return jobs_info, latest_run

def _ngcbash(
    team : bool = typer.Option(True, "-t/-T", help="defualt use lpr-imagine, otherwise use deep-imagination"),
    latest : bool = typer.Option(True, "-l/-L", help="defualt exec latest job bash, otherwise use fzf"),
    key : str = typer.Argument('ml', help='filter key, only show jobs whose names contain the key'),
):
    jobs_info,latest_run = get_job_info(team, key)
    if latest:
        if latest_run:
            select_run = latest_run
        else:
            exit(0)
    else:
        try:
            fzf = FzfPrompt()
            select_run = fzf.prompt(jobs_info['RUNNING'])[0]
        except ProcessExecutionError:
            exit(1)
        except Exception as error:  # pylint: disable=broad-except
            raise RuntimeError(  # pylint: disable=raise-missing-from
                "FZF error: {}".format(error)
            )

    logger.warning(f"bash exec {select_run}")
    job_id = select_run[:7]
    os.system(f'ngc batch exec {job_id}')

def _ngckill(
    team : bool = typer.Option(True, "-t/-T", help="defualt use lpr-imagine, otherwise use deep-imagination"),
    live : bool = typer.Option(False, "-l/-L", help="live run or dryrun, default dryrun"),
    kill_all : bool = typer.Option(False, "-a/-A", help="kill all jobs or not, default not"),
    key : str = typer.Argument('ml', help='filter key, only show jobs whose names contain the key')
):
    jobs_info = get_job_info(team, key)[0]

    _keys = []
    for k,v in jobs_info.items():
        _keys.extend([f'{k:<10}{_v}' for _v in v])

    if kill_all:
        for cur_line in _keys:
            _job_id = cur_line[10:10+7]
            run_simple_command(f"ngc batch kill {_job_id}")
            logger.warning(f"KILL   {cur_line}")
    elif live:
        try:
            fzf = FzfPrompt()
            select = fzf.prompt(_keys, "-m")
        except ProcessExecutionError:
            exit(1)
        except Exception as error:  # pylint: disable=broad-except
            raise RuntimeError(  # pylint: disable=raise-missing-from
                "FZF error: {}".format(error)
            )
        for cur_line in select:
            _job_id = cur_line[10:10+7]
            run_simple_command(f"ngc batch kill {_job_id}")
            logger.warning(f"KILL   {cur_line}")

    if not live:
        for k,v in jobs_info.items():
            print("#"*10 + f" {team}  {k}  Total {len(v):<10}" + "#"*10)
            for item in v:
                print(item)

def ngc_list():
    typer.run(_ngc_list)

def ngc_result():
    typer.run(_ngc_result)

def ngc_kill():
    typer.run(_ngckill)

def ngc_bash():
    typer.run(_ngcbash)
