from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class BatchInstance(Model):
    id = fields.IntField(pk=True)
    instance_name = fields.CharField(max_length=255, null=True)
    task_name = fields.CharField(max_length=255, null=True)
    job_name = fields.CharField(max_length=255, null=True)
    task_type = fields.CharField(max_length=255, null=True)
    status = fields.CharField(max_length=255, null=True)
    start_time = fields.BigIntField(null=True)
    end_time = fields.BigIntField(null=True)
    machine_id = fields.CharField(max_length=255, null=True)
    seq_no = fields.IntField(null=True)
    total_seq_no = fields.IntField(null=True)
    cpu_avg = fields.FloatField(null=True)
    cpu_max = fields.FloatField(null=True)
    mem_avg = fields.FloatField(null=True)
    mem_max = fields.FloatField(null=True)

    class Meta:
        table = 'batch_instance'


BatchInstance_Pydantic = pydantic_model_creator(BatchInstance, name="BatchInstance")


class BatchTask(Model):
    id = fields.IntField(pk=True)
    task_name = fields.CharField(max_length=255, null=True)
    instance_num = fields.IntField(null=True)
    job_name = fields.CharField(max_length=255, null=True)
    task_type = fields.CharField(max_length=255, null=True)
    status = fields.CharField(max_length=255, null=True)
    start_time = fields.BigIntField(null=True)
    end_time = fields.BigIntField(null=True)
    plan_cpu = fields.FloatField(null=True)
    plan_mem = fields.FloatField(null=True)

    class Meta:
        table = 'batch_task'


BatchTask_Pydantic = pydantic_model_creator(BatchTask, name="BatchTask")


class ContainerUsage(Model):
    id = fields.IntField(pk=True)
    container_id = fields.CharField(max_length=255, null=True)
    machine_id = fields.CharField(max_length=255, null=True)
    time_stamp = fields.IntField(null=True)
    cpu_util_percent = fields.IntField(null=True)
    mem_util_percent = fields.IntField(null=True)
    cpi = fields.FloatField(null=True)
    mem_gps = fields.FloatField(null=True)
    mpki = fields.IntField(null=True)
    net_in = fields.FloatField(null=True)
    net_out = fields.FloatField(null=True)
    disk_io_percent = fields.FloatField(null=True)

    class Meta:
        table = 'container_usage'


ContainerUsage_Pydantic = pydantic_model_creator(ContainerUsage, name="ContainerUsage")


class ContainerMeta(Model):
    id = fields.IntField(pk=True)
    container_id = fields.CharField(max_length=255, null=True)
    machine_id = fields.CharField(max_length=255, null=True)
    time_stamp = fields.IntField(null=True)
    app_du = fields.CharField(max_length=255, null=True)
    status = fields.CharField(max_length=255, null=True)
    cpu_request = fields.IntField(null=True)
    cpu_limit = fields.IntField(null=True)
    mem_size = fields.FloatField(null=True)

    class Meta:
        table = 'container_meta'


ContainerMeta_Pydantic = pydantic_model_creator(ContainerMeta, name="ContainerMeta")


class MachineUsage(Model):
    id = fields.IntField(pk=True)
    machine_id = fields.CharField(max_length=255, null=True)
    time_stamp = fields.IntField(null=True)
    cpu_util_percent = fields.IntField(null=True)
    mem_util_percent = fields.IntField(null=True)
    mem_gps = fields.FloatField(null=True)
    mkpi = fields.IntField(null=True)
    net_in = fields.FloatField(null=True)
    net_out = fields.FloatField(null=True)
    disk_io_percent = fields.FloatField(null=True)

    class Meta:
        table = 'machine_usage'


MachineUsage_Pydantic = pydantic_model_creator(MachineUsage, name="MachineUsage")


class MachineMeta(Model):
    id = fields.IntField(pk=True)
    machine_id = fields.CharField(max_length=255, null=True)
    time_stamp = fields.IntField(null=True)
    failure_domain_1 = fields.IntField(null=True)
    failure_domain_2 = fields.CharField(max_length=255, null=True)
    cpu_num = fields.IntField(null=True)
    mem_size = fields.IntField(null=True)
    status = fields.CharField(max_length=255, null=True)

    class Meta:
        table = 'machine_meta'


MachineMeta_Pydantic = pydantic_model_creator(MachineMeta, name="MachineMeta")


class CallGraph(Model):
    id = fields.IntField(pk=True)
    timestamp = fields.IntField(null=True)
    traceid = fields.CharField(max_length=255, null=True)
    service = fields.CharField(max_length=255, null=True)
    rpc_id = fields.CharField(max_length=255, null=True)
    um = fields.CharField(max_length=255, null=True)
    uminstanceid = fields.CharField(max_length=255, null=True)
    rpctype = fields.CharField(max_length=255, null=True)
    interface = fields.CharField(max_length=255, null=True)
    dm = fields.CharField(max_length=255, null=True)
    dminstanceid = fields.CharField(max_length=255, null=True)
    rt = fields.FloatField(null=True)

    class Meta:
        table = 'call_graph'


CallGraph_Pydantic = pydantic_model_creator(CallGraph, name="CallGraph")


class MSResource(Model):
    id = fields.IntField(pk=True)
    timestamp = fields.IntField(null=True)
    msname = fields.CharField(max_length=255, null=True)
    msinstanceid = fields.CharField(max_length=255, null=True)
    nodeid = fields.CharField(max_length=255, null=True)
    providerrpc_rt = fields.FloatField(null=True)
    providerrpc_mcr = fields.FloatField(null=True)
    consumerrpc_rt = fields.FloatField(null=True)
    consumerrpc_mcr = fields.FloatField(null=True)
    writemc_rt = fields.FloatField(null=True)
    writemc_mcr = fields.FloatField(null=True)
    readmc_rt = fields.FloatField(null=True)
    readmc_mcr = fields.FloatField(null=True)
    writedb_rt = fields.FloatField(null=True)
    writedb_mcr = fields.FloatField(null=True)
    readdb_rt = fields.FloatField(null=True)
    readdb_mcr = fields.FloatField(null=True)
    consumermq_rt = fields.FloatField(null=True)
    consumermq_mcr = fields.FloatField(null=True)
    providermq_rt = fields.FloatField(null=True)
    providermq_mcr = fields.FloatField(null=True)
    http_mcr = fields.FloatField(null=True)
    http_rt = fields.FloatField(null=True)

    class Meta:
        table = 'ms_resource'


MSResource_Pydantic = pydantic_model_creator(MSResource, name="MSResource")


class MSMetrics(Model):
    id = fields.IntField(pk=True)
    timestamp = fields.IntField(null=True)
    msname = fields.CharField(max_length=255, null=True)
    msinstanceid = fields.CharField(max_length=255, null=True)
    nodeid = fields.CharField(max_length=255, null=True)
    cpu_utilization = fields.FloatField(null=True)
    memory_utilization = fields.FloatField(null=True)

    class Meta:
        table = 'ms_metrics'


MSMetrics_Pydantic = pydantic_model_creator(MSMetrics, name="MSMetrics")


class Node(Model):
    id = fields.IntField(pk=True)
    timestamp = fields.IntField(null=True)
    nodeid = fields.CharField(max_length=255, null=True)
    cpu_utilization = fields.FloatField(null=True)
    memory_utilization = fields.FloatField(null=True)

    class Meta:
        table = 'node'


Node_Pydantic = pydantic_model_creator(Node, name="Node")


class Core(Model):
    id = fields.IntField(pk=True)
    ts = fields.BigIntField(null=True)
    node_id = fields.CharField(max_length=255, null=True)
    container_id = fields.CharField(max_length=255, null=True)
    cpu = fields.IntField(null=True)
    core_id = fields.IntField(null=True)
    socket_id = fields.IntField(null=True)
    instructions = fields.BigIntField(null=True)
    cycles = fields.BigIntField(null=True)
    ref_cycles = fields.BigIntField(null=True)
    llc_misses = fields.BigIntField(null=True)

    class Meta:
        table = 'core'


Core_Pydantic = pydantic_model_creator(Core, name="Core")


class UnCore(Model):
    id = fields.IntField(pk=True)
    ts = fields.IntField(null=True)
    node_id = fields.CharField(max_length=255, null=True)
    socket_id = fields.IntField(null=True)
    channel_id = fields.CharField(max_length=255, null=True)
    read_bw = fields.FloatField(null=True)
    write_bw = fields.FloatField(null=True)
    latency = fields.FloatField(null=True)

    class Meta:
        table = 'uncore'


UnCore_Pydantic = pydantic_model_creator(UnCore, name="UnCore")


class Container(Model):
    id = fields.IntField(pk=True)
    node_id = fields.CharField(max_length=255, null=True)
    container_id = fields.CharField(max_length=255, null=True)
    pod_id = fields.CharField(max_length=255, null=True)
    cpu_mode = fields.CharField(max_length=255, null=True)
    app_name = fields.CharField(max_length=255, null=True)
    deploy_group = fields.CharField(max_length=255, null=True)
    container_type = fields.CharField(max_length=255, null=True)
    container_cpu_spec = fields.FloatField(null=True)
    container_mem_spec = fields.FloatField(null=True)
    pod_cpu_spec = fields.FloatField(null=True)
    pod_mem_spec = fields.FloatField(null=True)

    class Meta:
        table = 'container'


Container_Pydantic = pydantic_model_creator(Container, name="Container")


class HostMeta(Model):
    id = fields.IntField(pk=True)
    node_id = fields.CharField(max_length=255, null=True)
    cpu_num = fields.IntField(null=True)
    machine_model = fields.CharField(max_length=255, null=True)
    cpu_model = fields.CharField(max_length=255, null=True)
    ref_freq_Ghz = fields.FloatField(null=True)
    dimms_per_channel = fields.IntField(null=True)

    class Meta:
        table = 'host_meta'


HostMeta_Pydantic = pydantic_model_creator(HostMeta, name="HostMeta")
