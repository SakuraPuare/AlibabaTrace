from typing import Any

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# deprecated

class BatchInstance(Base):
    ### batch instance
    # +-----------------------------------------------------------------------------------------------+
    # | instance_name   | String(255)     |       | instance name of the instance                          |
    # | task_name       | String(255)     |       | name of task to which the instance belong              |
    # | job_name        | String(255)     |       | name of job to which the instance belong               |
    # | task_type       | String(255)     |       | task type                                              |
    # | status          | String(255)     |       | instance status                                        |
    # | start_time      | bigint     |       | start time of the instance                             |
    # | end_time        | bigint     |       | end time of the instance                               |
    # | machine_id      | String(255)     |       | uid of host machine of the instance                    |
    # | seq_no          | bigint     |       | sequence number of this instance                       |
    # | total_seq_no    | bigint     |       | total sequence number of this instance                 |
    # | cpu_avg         | double     |       | average cpu used by the instance, 100 is 1 core        |
    # | cpu_max         | double     |       | max cpu used by the instance, 100 is 1 core            |
    # | mem_avg         | double     |       | average memory used by the instance (normalized)       |
    # | mem_max         | double     |       | max memory used by the instance (normalized, [0, 100]) |
    # +-----------------------------------------------------------------------------------------------+
    __tablename__ = 'batch_instance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    instance_name = Column(String(255), nullable=True)
    task_name = Column(String(255), nullable=True)
    job_name = Column(String(255), nullable=True)
    task_type = Column(String(255), nullable=True)
    status = Column(String(255), nullable=True)
    start_time = Column(Integer, nullable=True)
    end_time = Column(Integer, nullable=True)
    machine_id = Column(String(255), nullable=True)
    seq_no = Column(Integer, nullable=True)
    total_seq_no = Column(Integer, nullable=True)
    cpu_avg = Column(Float, nullable=True)
    cpu_max = Column(Float, nullable=True)
    mem_avg = Column(Float, nullable=True)
    mem_max = Column(Float, nullable=True)

    def __init__(self, data: list):
        (self.instance_name, self.task_name, self.job_name, self.task_type, self.status, self.start_time, self.end_time,
         self.machine_id, self.seq_no, self.total_seq_no, self.cpu_avg, self.cpu_max, self.mem_avg, self.mem_max) = data

    def __repr__(self):
        return (f"<BatchInstance(id={self.id}, instance_name={self.instance_name}, task_name={self.task_name}, "
                f"job_name={self.job_name}, task_type={self.task_type}, status={self.status}, "
                f"start_time={self.start_time}, end_time={self.end_time}, machine_id={self.machine_id}, "
                f"seq_no={self.seq_no}, total_seq_no={self.total_seq_no}, cpu_avg={self.cpu_avg}, "
                f"cpu_max={self.cpu_max}, mem_avg={self.mem_avg}, mem_max={self.mem_max})>")


class BatchTask(Base):
    ### batch task
    # +----------------------------------------------------------------------------------------+
    # | task_name       | string     |       | task name. unique within a job                  |
    # | instance_num    | bigint     |       | number of instances                             |
    # | job_name        | string     |       | job name                                        |
    # | task_type       | string     |       | task type                                       |
    # | status          | string     |       | task status                                     |
    # | start_time      | bigint     |       | start time of the task                          |
    # | end_time        | bigint     |       | end of time the task                            |
    # | plan_cpu        | double     |       | number of cpu needed by the task, 100 is 1 core |
    # | plan_mem        | double     |       | normalized memorty size, [0, 100]               |
    # +----------------------------------------------------------------------------------------+
    __tablename__ = 'batch_task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String(255), nullable=True)
    instance_num = Column(Integer, nullable=True)
    job_name = Column(String(255), nullable=True)
    task_type = Column(String(255), nullable=True)
    status = Column(String(255), nullable=True)
    start_time = Column(Integer, nullable=True)
    end_time = Column(Integer, nullable=True)
    plan_cpu = Column(Float, nullable=True)
    plan_mem = Column(Float, nullable=True)

    def __init__(self, data: list, **kw: Any):
        super().__init__(**kw)
        (self.task_name, self.instance_num, self.job_name, self.task_type, self.status, self.start_time, self.end_time,
         self.plan_cpu, self.plan_mem) = data

    def __repr__(self):
        return (f"<BatchTask(id={self.id}, task_name={self.task_name}, instance_num={self.instance_num}, "
                f"job_name={self.job_name}, task_type={self.task_type}, status={self.status}, "
                f"start_time={self.start_time}, end_time={self.end_time}, plan_cpu={self.plan_cpu}, "
                f"plan_mem={self.plan_mem})>")


class ContainerUsage(Base):
    ### container usage
    # +-----------------------------------------------------------------------------------------+
    # | container_id     | string     |       | uid of a container                              |
    # | machine_id       | string     |       | uid of container's host machine                 |
    # | time_stamp       | double     |       | time stamp, in second                           |
    # | cpu_util_percent | bigint     |       |                                                 |
    # | mem_util_percent | bigint     |       |                                                 |
    # | cpi              | double     |       |                                                 |
    # | mem_gps          | double     |       | normalized memory bandwidth, [0, 100]           |
    # | mpki             | bigint     |       |                                                 |
    # | net_in           | double     |       | normarlized in coming network traffic, [0, 100] |
    # | net_out          | double     |       | normarlized out going network traffic, [0, 100] |
    # | disk_io_percent  | double     |       | [0, 100], abnormal values are of -1 or 101      |
    # +-----------------------------------------------------------------------------------------+
    __tablename__ = 'container_usage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    container_id = Column(String(255), nullable=True)
    machine_id = Column(String(255), nullable=True)
    time_stamp = Column(Integer, nullable=True)
    cpu_util_percent = Column(Integer, nullable=True)
    mem_util_percent = Column(Integer, nullable=True)
    cpi = Column(Float, nullable=True)
    mem_gps = Column(Float, nullable=True)
    mpki = Column(Integer, nullable=True)
    net_in = Column(Float, nullable=True)
    net_out = Column(Float, nullable=True)
    disk_io_percent = Column(Float, nullable=True)

    def __init__(self, data: list, **kw: Any):
        super().__init__(**kw)
        (self.container_id, self.machine_id, self.time_stamp, self.cpu_util_percent, self.mem_util_percent, self.cpi,
         self.mem_gps, self.mpki, self.net_in, self.net_out, self.disk_io_percent) = data

    def __repr__(self):
        return (f"<ContainerUsage(id={self.id}, container_id={self.container_id}, machine_id={self.machine_id}, "
                f"time_stamp={self.time_stamp}, cpu_util_percent={self.cpu_util_percent}, "
                f"mem_util_percent={self.mem_util_percent}, cpi={self.cpi}, mem_gps={self.mem_gps}, "
                f"mpki={self.mpki}, net_in={self.net_in}, net_out={self.net_out}, "
                f"disk_io_percent={self.disk_io_percent})>")


class ContainerMeta(Base):
    ### container meta
    # +-----------------------------------------------------------------------------------------------------+
    # | Field           | Type       | Label | Comment                                                      |
    # +-----------------------------------------------------------------------------------------------------+
    # | container_id    | string     |       | uid of a container                                           |
    # | machine_id      | string     |       | uid of container's host machine                              |
    # | time_stamp      | bigint     |       |                                                              |
    # | app_du          | string     |       | containers with same app_du belong to same application group |
    # | status          | string     |       |                                                              |
    # | cpu_request     | bigint     |       | 100 is 1 core                                                |
    # | cpu_limit       | bigint     |       | 100 is 1 core                                                |
    # | mem_size        | double     |       | normarlized memory, [0, 100]                                 |
    # +-----------------------------------------------------------------------------------------------------+
    __tablename__ = 'container_meta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    container_id = Column(String(255), nullable=True)
    machine_id = Column(String(255), nullable=True)
    time_stamp = Column(Integer, nullable=True)
    app_du = Column(String(255), nullable=True)
    status = Column(String(255), nullable=True)
    cpu_request = Column(Integer, nullable=True)
    cpu_limit = Column(Integer, nullable=True)
    mem_size = Column(Float, nullable=True)

    def __init__(self, data: list, **kw: Any):
        super().__init__(**kw)
        (self.container_id, self.machine_id, self.time_stamp, self.app_du, self.status, self.cpu_request,
         self.cpu_limit, self.mem_size) = data

    def __repr__(self):
        return (f"<ContainerMeta(id={self.id}, container_id={self.container_id}, machine_id={self.machine_id}, "
                f"time_stamp={self.time_stamp}, app_du={self.app_du}, status={self.status}, "
                f"cpu_request={self.cpu_request}, cpu_limit={self.cpu_limit}, mem_size={self.mem_size})>")


class MachineUsage(Base):
    ### machine usage
    # +--------------------------------------------------------------------------------------------+
    # | Field            | Type       | Label | Comment                                            |
    # +--------------------------------------------------------------------------------------------+
    # | machine_id       | string     |       | uid of machine                                     |
    # | time_stamp       | double     |       | time stamp, in second                              |
    # | cpu_util_percent | bigint     |       | [0, 100]                                           |
    # | mem_util_percent | bigint     |       | [0, 100]                                           |
    # | mem_gps          | double     |       | normalized memory bandwidth, [0, 100]              |
    # | mkpi             | bigint     |       | cache miss per thousand instruction                |
    # | net_in           | double     |       | normarlized in coming network traffic, [0, 100]    |
    # | net_out          | double     |       | normarlized out going network traffic, [0, 100]    |
    # | disk_io_percent  | double     |       | [0, 100], abnormal values are of -1 or 101         |
    # +--------------------------------------------------------------------------------------------+
    __tablename__ = 'machine_usage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    machine_id = Column(String(255), nullable=True)
    time_stamp = Column(Integer, nullable=True)
    cpu_util_percent = Column(Integer, nullable=True)
    mem_util_percent = Column(Integer, nullable=True)
    mem_gps = Column(Float, nullable=True)
    mkpi = Column(Integer, nullable=True)
    net_in = Column(Float, nullable=True)
    net_out = Column(Float, nullable=True)
    disk_io_percent = Column(Float, nullable=True)

    def __init__(self, data: list, **kw: Any):
        super().__init__(**kw)
        (self.machine_id, self.time_stamp, self.cpu_util_percent, self.mem_util_percent, self.mem_gps, self.mkpi,
         self.net_in, self.net_out, self.disk_io_percent) = data

    def __repr__(self):
        return (f"<MachineUsage(id={self.id}, machine_id={self.machine_id}, time_stamp={self.time_stamp}, "
                f"cpu_util_percent={self.cpu_util_percent}, mem_util_percent={self.mem_util_percent}, "
                f"mem_gps={self.mem_gps}, mkpi={self.mkpi}, net_in={self.net_in}, net_out={self.net_out}, "
                f"disk_io_percent={self.disk_io_percent})>")


class MachineMeta(Base):
    ### machine meta
    # +-------------------------------------------------------------------------------------+
    # | Field            | Type       | Label | Comment                                     |
    # +-------------------------------------------------------------------------------------+
    # | machine_id       | string     |       | uid of machine                              |
    # | time_stamp       | bigint     |       | time stamp, in second                       |
    # | failure_domain_1 | bigint     |       | one level of container failure domain       |
    # | failure_domain_2 | string     |       | another level of container failure domain   |
    # | cpu_num          | bigint     |       | number of cpu on a machine                  |
    # | mem_size         | bigint     |       | normalized memory size. [0, 100]            |
    # | status           | string     |       | status of a machine                         |
    # +-------------------------------------------------------------------------------------+
    __tablename__ = 'machine_meta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    machine_id = Column(String(255), nullable=True)
    time_stamp = Column(Integer, nullable=True)
    failure_domain_1 = Column(Integer, nullable=True)
    failure_domain_2 = Column(String(255), nullable=True)
    cpu_num = Column(Integer, nullable=True)
    mem_size = Column(Integer, nullable=True)
    status = Column(String(255), nullable=True)

    def __init__(self, data: list, **kw: Any):
        super().__init__(**kw)
        (self.machine_id, self.time_stamp, self.failure_domain_1, self.failure_domain_2, self.cpu_num, self.mem_size,
         self.status) = data

    def __repr__(self):
        return (f"<MachineMeta(id={self.id}, machine_id={self.machine_id}, time_stamp={self.time_stamp}, "
                f"failure_domain_1={self.failure_domain_1}, failure_domain_2={self.failure_domain_2}, "
                f"cpu_num={self.cpu_num}, mem_size={self.mem_size}, status={self.status})>")


class CallGraph(Base):
    """
    | columns      |  Example Entry  |
    | ------------ | :--------------: |
    | timestamp    |      115352      |
    | traceid      |  T_11560863075  |
    | service      |   S_153587416   |
    | rpc_id       |       0.1       |
    | um           |     MS_58845     |
    | uminstanceid |  MS_58845_POD_0  |
    | rpctype      |       rpc       |
    | interface    |    xOuy6-80Vt    |
    | dm           |     MS_71712     |
    | dminstanceid | MS_71712_POD_244 |
    | rt           |       2.0       |
    """
    __tablename__ = 'call_graph'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(Integer, nullable=True)
    traceid = Column(String(255), nullable=True)
    service = Column(String(255), nullable=True)
    rpc_id = Column(String(255), nullable=True)
    um = Column(String(255), nullable=True)
    uminstanceid = Column(String(255), nullable=True)
    rpctype = Column(String(255), nullable=True)
    interface = Column(String(255), nullable=True)
    dm = Column(String(255), nullable=True)
    dminstanceid = Column(String(255), nullable=True)
    rt = Column(Float, nullable=True)

    def __init__(self, data: list, **kw: Any):
        super().__init__(**kw)
        (self.timestamp, self.traceid, self.service, self.rpc_id, self.um, self.uminstanceid, self.rpctype,
         self.interface, self.dm, self.dminstanceid, self.rt) = data
        self.rt = None if self.rt == 'None' else self.rt

    def __repr__(self):
        return (f"<CallGraph(id={self.id}, timestamp={self.timestamp}, traceid={self.traceid}, service={self.service}, "
                f"rpc_id={self.rpc_id}, um={self.um}, uminstanceid={self.uminstanceid}, rpctype={self.rpctype}, "
                f"interface={self.interface}, dm={self.dm}, dminstanceid={self.dminstanceid}, rt={self.rt})>")


class MSResource(Base):
    """
| columns         |     Example Entry     |
| --------------- | :--------------------: |
| timestamp       |         60000         |
| msname          |        MS_73317        |
| msinstanceid    |   MS_73317_POD_1797   |
| nodeid          |       NODE_3619       |
| providerrpc_rt  |   10.119451170298627   |
| providerrpc_mcr | 1.216773932801612e-05 |
| consumerrpc_rt  |   9.996974281391829   |
| consumerrpc_mcr | 7.169679436055699e-12 |
| writemc_rt      |          0.0          |
| writemc_mcr     |          0.0          |
| readmc_rt       |        0.40625        |
| readmc_mcr      | 3.142596113773332e-07 |
| writedb_rt      |          0.0          |
| writedb_mcr     |          0.0          |
| readdb_rt       |   0.9693548387096775   |
| readdb_mcr      | 6.088779970435831e-06 |
| consumermq_rt   |          0.0          |
| consumermq_mcr  |          0.0          |
| providermq_rt   |    24.4218009478673    |
| providermq_mcr  | 2.0721493125192907e-06 |
| http_mcr        |          0.0          |
| http_rt         |          0.0          |

- timestamp: Mentioned in Node. The recording interval is the 60s (60 * 1000).
- msname: Mentioned in MSResource.
- msinstanceid: Mentioned in MSResource.
- nodeid: Mentioned in Node.
- Other columns: The value of corresponding RT and calls rate with different communication paradigms. For example, the value of metric providerRPC_MCR and providerRPC_RT characterize the number of calls per second and the average of response time respectively. Here, the response time is measured by millisecond (ms) and the MCR is **normalized** through max-min in range from 0 to 1. The value of metrics for an MS is an aggregation of all its DMs and UMs. To distinguish whether an MS is DM or UM, the Metrics are recorded with a prefix before communication paradigms. For example, RPC is named consumerRPC and providerRPC, meaning an MS as the consumer calling its DM and as the provider being called by its UM respectively. Correspondingly, MQ could be classified into two groups from an MS's point of view, namely, providerMQ, and consumerMQ. For the former, MQ is a provider that sends messages to the third party whereas, the latter is a consumer that fetches messages from the third party. As MSs in this table are all stateless services, they are only UMs to read or write stateful services.
  In summary, these metrics include consumerRPC_MCR, providerRPC_MCR, HTTP_MCR, providerMQ_MCR, consumerMQ_MCR, consumerRPC_RT, providerRPC_RT, HTTP_RT, providerMQ_RT, and consumerMQ_RT.
"""
    __tablename__ = 'ms_resource'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(Integer, nullable=True)
    msname = Column(String(255), nullable=True)
    msinstanceid = Column(String(255), nullable=True)
    nodeid = Column(String(255), nullable=True)
    providerrpc_rt = Column(Float, nullable=True)
    providerrpc_mcr = Column(Float, nullable=True)
    consumerrpc_rt = Column(Float, nullable=True)
    consumerrpc_mcr = Column(Float, nullable=True)
    writemc_rt = Column(Float, nullable=True)
    writemc_mcr = Column(Float, nullable=True)
    readmc_rt = Column(Float, nullable=True)
    readmc_mcr = Column(Float, nullable=True)
    writedb_rt = Column(Float, nullable=True)
    writedb_mcr = Column(Float, nullable=True)
    readdb_rt = Column(Float, nullable=True)
    readdb_mcr = Column(Float, nullable=True)
    consumermq_rt = Column(Float, nullable=True)
    consumermq_mcr = Column(Float, nullable=True)
    providermq_rt = Column(Float, nullable=True)
    providermq_mcr = Column(Float, nullable=True)
    http_mcr = Column(Float, nullable=True)
    http_rt = Column(Float, nullable=True)

    def __init__(self, data: list, **kw: Any):
        super().__init__(**kw)
        (self.timestamp, self.msname, self.msinstanceid, self.nodeid, self.providerrpc_rt, self.providerrpc_mcr,
         self.consumerrpc_rt, self.consumerrpc_mcr, self.writemc_rt, self.writemc_mcr, self.readmc_rt, self.readmc_mcr,
         self.writedb_rt, self.writedb_mcr, self.readdb_rt, self.readdb_mcr, self.consumermq_rt, self.consumermq_mcr,
         self.providermq_rt, self.providermq_mcr, self.http_mcr, self.http_rt) = data

    def __repr__(self):
        return (f"<MSResource(id={self.id}, timestamp={self.timestamp}, msname={self.msname}, "
                f"msinstanceid={self.msinstanceid}, nodeid={self.nodeid}, providerrpc_rt={self.providerrpc_rt}, "
                f"providerrpc_mcr={self.providerrpc_mcr}, consumerrpc_rt={self.consumerrpc_rt}, "
                f"consumerrpc_mcr={self.consumerrpc_mcr}, writemc_rt={self.writemc_rt}, "
                f"writemc_mcr={self.writemc_mcr}, readmc_rt={self.readmc_rt}, readmc_mcr={self.readmc_mcr}, "
                f"writedb_rt={self.writedb_rt}, writedb_mcr={self.writedb_mcr}, readdb_rt={self.readdb_rt}, "
                f"readdb_mcr={self.readdb_mcr}, consumermq_rt={self.consumermq_rt}, "
                f"consumermq_mcr={self.consumermq_mcr}, providermq_rt={self.providermq_rt}, "
                f"providermq_mcr={self.providermq_mcr}, http_mcr={self.http_mcr}, http_rt={self.http_rt})>")


class MSMetrics(Base):
    """
      | columns | Example
      Entry |
      | ------------------ |: -----------------: |
      | timestamp | 180000 |
      | msname | MS_21881 |
      | msinstanceid | MS_21881_POD_0 |
      | nodeid | NODE_11517 |
      | cpu_utilization | 0.21995999999530616 |
      | memory_utilization | 0.833001454671224 |
      """
    __tablename__ = 'ms_metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(Integer, nullable=True)
    msname = Column(String(255), nullable=True)
    msinstanceid = Column(String(255), nullable=True)
    nodeid = Column(String(255), nullable=True)
    cpu_utilization = Column(Float, nullable=True)
    memory_utilization = Column(Float, nullable=True)

    def __init__(self, data: list, **kw: Any):
        super().__init__(**kw)
        (self.timestamp, self.msname, self.msinstanceid, self.nodeid, self.cpu_utilization,
         self.memory_utilization) = data

    def __repr__(self):
        return (f"<MSMetrics(id={self.id}, timestamp={self.timestamp}, msname={self.msname}, "
                f"msinstanceid={self.msinstanceid}, nodeid={self.nodeid}, cpu_utilization={self.cpu_utilization}, "
                f"memory_utilization={self.memory_utilization})>")


class Node(Base):
    """
    | columns | Example Entry |
    | ------------------ |: ---------------: |
    | timestamp | 60000 |
    | nodeid | NODE_10632 |
    | cpu_utilization | 0.266488095525847 |
    | memory_utilization | 0.159064258887333 |"""
    __tablename__ = 'node'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(Integer, nullable=True)
    nodeid = Column(String(255), nullable=True)
    cpu_utilization = Column(Float, nullable=True)
    memory_utilization = Column(Float, nullable=True)

    def __init__(self, data: list, **kw: Any):
        super().__init__(**kw)
        (self.timestamp, self.nodeid, self.cpu_utilization, self.memory_utilization) = data

    def __repr__(self):
        return (f"<Node(id={self.id}, timestamp={self.timestamp}, nodeid={self.nodeid}, "
                f"cpu_utilization={self.cpu_utilization}, memory_utilization={self.memory_utilization})>")


class Core(Base):
    """
    ## core_pmu_metrics
    | Columns    | Description     | Type    |Example Entry            |
    |:-----------|:----------------|:--------|:---------------------------|
    | ts         | Timestamp, the number of seconds from the start      |Long |46309 |
    | node_id    | ID of the node  |String   |e7a66b9189940e9d6102 |
    | container_id|ID of the container|String|213aff2b3dbec1f7c212|
    | cpu           |logic cpu id|Int    | 23|
    | core_id       |core id |Int | 23|
    |socket_id      |socket id|Int | 0|
    |instructions   |number of instructions happened on the `logic cpu`|Long | 694470820|
    |cycles         |number of cycles happened on the `logic cpu`|Long   |1391935375|
    |ref_cycles|number of reference cycles happened on the `logic cpu` |Long|1284610800|
    |llc_misses |number of LLC cache misses happened on the `logic cpu` |Long|6667696|
    """
    __tablename__ = 'core'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ts = Column(BIGINT, nullable=True)
    node_id = Column(String(255), nullable=True)
    container_id = Column(String(255), nullable=True)
    cpu = Column(Integer, nullable=True)
    core_id = Column(Integer, nullable=True)
    socket_id = Column(Integer, nullable=True)
    instructions = Column(BIGINT, nullable=True)
    cycles = Column(BIGINT, nullable=True)
    ref_cycles = Column(BIGINT, nullable=True)
    llc_misses = Column(BIGINT, nullable=True)

    def __init__(self, data: list, **kw: Any):
        super().__init__(**kw)
        (self.ts, self.node_id, self.container_id, self.cpu, self.core_id, self.socket_id, self.instructions,
         self.cycles, self.ref_cycles, self.llc_misses) = data

    def __repr__(self):
        return (f"<Core(id={self.id}, ts={self.ts}, node_id={self.node_id}, container_id={self.container_id}, "
                f"cpu={self.cpu}, core_id={self.core_id}, socket_id={self.socket_id}, instructions={self.instructions}, "
                f"cycles={self.cycles}, ref_cycles={self.ref_cycles}, llc_misses={self.llc_misses})>")


class UnCore(Base):
    """
    ## uncore_pmu_metrics
    | Columns    | Description     | Type    |Example Entry            |
    |:-----------|:----------------|:--------|:---------------------------|
    |ts         | Timestamp, the number of seconds from the start|Long   |2787 |
    |node_id |ID of the node | String| 68451b8967ad23a10681|
    |socket_id| socket id|Int| 0|
    |channel_id| ID of the memory channel| String | 4|
    |read_bw|read bandwidth (MiB/s)| Double| 2540.7185|
    |write_bw| write bandwidth (MiB/s)| Double| 1493.8240|
    |latency| memory read latency (ns)| Double| 16.7503|
    """
    __tablename__ = 'uncore'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ts = Column(Integer, nullable=True)
    node_id = Column(String(255), nullable=True)
    socket_id = Column(Integer, nullable=True)
    channel_id = Column(String(255), nullable=True)
    read_bw = Column(Float, nullable=True)
    write_bw = Column(Float, nullable=True)
    latency = Column(Float, nullable=True)

    def __init__(self, data: list, **kw: Any):
        super().__init__(**kw)
        (self.ts, self.node_id, self.socket_id, self.channel_id, self.read_bw, self.write_bw, self.latency) = data

    def __repr__(self):
        return (f"<Uncore(id={self.id}, ts={self.ts}, node_id={self.node_id}, socket_id={self.socket_id}, "
                f"channel_id={self.channel_id}, read_bw={self.read_bw}, write_bw={self.write_bw}, latency={self.latency})>")


class Container(Base):
    """
## container
| Columns    | Description     | Type    |Example Entry            |
|:-----------|:----------------|:--------|:---------------------------|
|node_id|ID of the node|String|dd070834956a25c0c531|
|container_id|ID of the container|String| a40de288d9455ba121db|
|pod_id|ID of the Pod|String|bf74c065cd443d178474|
|cpu_mode|cpu allocation mode|String| CPUShare|
|app_name|the name of applicaton,Batch jobs are all "Batch"| String| Batch|
|deploy_group| Deployment group, one application may have multiple deployment group| String| Batch|
|container_type|container type | String| Batch-ops|
|container_cpu_spec| **Deprecated** Ratio of logic CPUs requested by the container to the number of logic CPUs of the node (0-1)| Double| 0.04|
|container_mem_spec| **Deprecated** Ratio of memory requested by the container to the memory of the node (0-1)|Double|0.003|
|pod_cpu_spec|Ratio of logic CPUs requested by the Pod to the number of logic CPUs of the node (0-1)|Double|0.04|
|pod_mem_spec|Ratio of memory requested by the Pod to the memory of the node (0-1)|Double|0.003|
"""
    __tablename__ = 'container'

    id = Column(Integer, primary_key=True, autoincrement=True)
    node_id = Column(String(255), nullable=True)
    container_id = Column(String(255), nullable=True)
    pod_id = Column(String(255), nullable=True)
    cpu_mode = Column(String(255), nullable=True)
    app_name = Column(String(255), nullable=True)
    deploy_group = Column(String(255), nullable=True)
    container_type = Column(String(255), nullable=True)
    container_cpu_spec = Column(Float, nullable=True)
    container_mem_spec = Column(Float, nullable=True)
    pod_cpu_spec = Column(Float, nullable=True)
    pod_mem_spec = Column(Float, nullable=True)

    def __init__(self, data: list, **kw: Any):
        super().__init__(**kw)
        (self.node_id, self.container_id, self.pod_id, self.cpu_mode, self.app_name, self.deploy_group,
         self.container_type, self.container_cpu_spec, self.container_mem_spec, self.pod_cpu_spec,
         self.pod_mem_spec) = data

    def __repr__(self):
        return (f"<ContainerMeta(id={self.id}, node_id={self.node_id}, container_id={self.container_id}, "
                f"pod_id={self.pod_id}, cpu_mode={self.cpu_mode}, app_name={self.app_name}, deploy_group={self.deploy_group}, "
                f"container_type={self.container_type}, container_cpu_spec={self.container_cpu_spec}, "
                f"container_mem_spec={self.container_mem_spec}, pod_cpu_spec={self.pod_cpu_spec}, "
                f"pod_mem_spec={self.pod_mem_spec})>")


class HostMeta(Base):
    """
    ## host_meta

    | Columns    | Description     | Type    |Example Entry            |
    |:-----------|:----------------|:--------|:---------------------------|
    |node_id|ID of the node|String| 3201ea36ad240dc51d6c|
    |cpu_num|The number of logic CPUs of the node|Int| 96 |
    |machine_model|The model of the node, one model is one kind of specification|String| machine-1|
    |cpu_model|The model of the CPU|String | skylake|
    |ref_freq_Ghz|The frequency of the CPU(Ghz)|Int|2.5|
    |dimms_per_channel|The number of DIMMs of every memory channel|Int|2|
    """
    __tablename__ = 'host_meta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    node_id = Column(String(255), nullable=True)
    cpu_num = Column(Integer, nullable=True)
    machine_model = Column(String(255), nullable=True)
    cpu_model = Column(String(255), nullable=True)
    ref_freq_Ghz = Column(Float, nullable=True)
    dimms_per_channel = Column(Integer, nullable=True)

    def __init__(self, data: list, **kw: Any):
        super().__init__(**kw)
        (self.node_id, self.cpu_num, self.machine_model, self.cpu_model, self.ref_freq_Ghz,
         self.dimms_per_channel) = data

    def __repr__(self):
        return (f"<HostMeta(id={self.id}, node_id={self.node_id}, cpu_num={self.cpu_num}, "
                f"machine_model={self.machine_model}, cpu_model={self.cpu_model}, ref_freq_Ghz={self.ref_freq_Ghz}, "
                f"dimms_per_channel={self.dimms_per_channel})>")
